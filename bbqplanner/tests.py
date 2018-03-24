import pytest

from datetime import date

from django.core.management import call_command
from django.urls import reverse
from bbqproducts.models import BBQProduct
from bbqplanner.models import BBQEvent, BBQEventVisitor
from bbqplanner.views import get_event_summary


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'fixtures/products.json')


@pytest.fixture()
def event(django_db_blocker, django_user_model):
    u = django_user_model.objects.create(username="me", password="123")
    with django_db_blocker.unblock():
        event = BBQEvent.objects.create(
            date=date(2018, 3, 31), 
            organizer=u, 
        )
        event.save()
        event.available_products.set(BBQProduct.objects.all())
        return event


@pytest.fixture()
def two_events(event):
    # nice hack to clone model instances
    event.pk = None
    event.save()
    event.available_products.set(BBQProduct.objects.all())
    return BBQEvent.objects.all()


def test_create_event(admin_client):
    date_expected = date(2018, 3, 31)
    available_products_pk_expected = [1, 2]
    data = {
        'date': date_expected.strftime('%Y-%m-%d'),
        'available_products': available_products_pk_expected
    }
    count_events = BBQEvent.objects.count()
    admin_client.post(reverse('event_create'), data)
    assert count_events + 1 == BBQEvent.objects.count()

    event = BBQEvent.objects.all()[0]
    
    date_actual = event.date
    available_products_pk_actual = list(event.available_products.values_list('id', flat=True))

    for pk in available_products_pk_expected:
        assert pk in available_products_pk_actual
    assert date_expected == date_actual


def test_register_event(client, event):
    name_expected = 'tim'
    guests_count_expected = 100
    desired_products_pk_expected = [2, 3]
    data = {
        'name': name_expected,
        'guests_count': guests_count_expected,
        'desired_products': desired_products_pk_expected,
    }

    count_visitors = BBQEventVisitor.objects.count()
    client.post(reverse('event', kwargs={'uuid': event.uuid}), data)
    assert count_visitors + 1 == BBQEventVisitor.objects.count()

    visitor = BBQEventVisitor.objects.all()[0]

    name_actual = visitor.name
    guests_count_actual = visitor.guests_count
    desired_products_pk_actual = list(visitor.desired_products.values_list('id', flat=True))
    
    assert name_expected == name_actual
    assert guests_count_expected == guests_count_actual
    for pk in desired_products_pk_expected:
        assert pk in desired_products_pk_actual


def test_event_summary(two_events, client, mocker):
    empty_event = two_events[0]
    event_with_guests = two_events[1]

    request = mocker.Mock()
    request.user = empty_event.organizer
    empty_summary = get_event_summary(request, empty_event)

    assert empty_summary['user_is_host'] == True
    assert empty_summary['sum_guests'] == 0 
    assert empty_summary['guest_list'] == []
    assert empty_summary['product_summary'] == {}
    
    test_register_event(client, event_with_guests)
    test_register_event(client, event_with_guests)
    request = mocker.Mock()
    summary_with_guests = get_event_summary(request, event_with_guests)

    assert summary_with_guests['sum_guests'] == 202
    assert summary_with_guests['guest_list'] == ['tim', 'tim']
    assert summary_with_guests['product_summary'] == {'Beef': 2, 'Chicken': 2}
