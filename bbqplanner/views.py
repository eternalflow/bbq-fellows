from datetime import datetime
from functools import reduce
from operator import add
from collections import Counter

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse
from django import forms
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce
from .models import BBQEvent, BBQEventVisitor

from bootstrap_datepicker.widgets import DatePicker


def get_event(uuid):
    try:
        event = BBQEvent.objects.get(uuid=uuid)
    except BBQEvent.DoesNotExist:
        event = None
    return event


def get_event_summary(request, event):
    if not event:
        return None
    user_is_host = False
    if request.user.is_authenticated and event.organizer == request.user:
        user_is_host = True

    return {
        'hosted_by': event.organizer.username,
        'date': event.date,
        'user_is_host': user_is_host,
        'available_products': event.available_products.all(),
        'link': request.build_absolute_uri(reverse('event', kwargs={'uuid': event.uuid})),
        'sum_guests': event.visitors.aggregate(sum_guests=Coalesce(Sum(F('guests_count') + Value(1)), 0))['sum_guests'],
        'guest_list': list(event.visitors.values_list('name', flat=True)),
        'product_summary': dict(Counter(
            reduce(add, map(list, (v.desired_products.values_list('name', flat=True) for v in event.visitors.all())), [])))
    }


class EventForm(forms.ModelForm):
    class Meta:
        model = BBQEvent
        fields = ['date', 'available_products']
        widgets = {
            'date': DatePicker(
                attrs={"class": "form-control"},
                options={
                    'format': "yyyy-mm-dd",
                }),
            'available_products': forms.CheckboxSelectMultiple(attrs={"class":"form-control"}),
        }


class EventVisitorForm(forms.ModelForm):
    class Meta:
        model = BBQEventVisitor
        fields = ['name', 'guests_count', 'desired_products']
        widgets = {
            'desired_products': forms.CheckboxSelectMultiple()
        }


class Event(generic.View):

    @staticmethod
    def make_application_form(event, *args, **kwargs):
        form = EventVisitorForm(*args, **kwargs)
        form.fields['desired_products'].queryset = event['available_products']
        return form

    def get(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        db_event = get_event(uuid)
        event = get_event_summary(request, db_event)
        form = None
        if event and not event['user_is_host']:
            form = self.make_application_form(event)
        return render(request, 'bbqplanner/event_detail.html', {'event': event, 'form': form})

    def post(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        db_event = get_event(uuid)
        event = get_event_summary(request, db_event)
        form = None
        if event:
            form = self.make_application_form(event, request.POST)
        if form and form.is_valid():
            visitor = form.save(commit=False)
            visitor.event = db_event
            visitor.save()
            form.save_m2m()
            return redirect('event_register_success')
        return render(request, 'bbqplanner/event_detail.html', {'event': event, 'form': form})

class CreateEvent(LoginRequiredMixin, generic.View):

    def get(self, request):
        form = EventForm()
        return render(request, 'bbqplanner/event_create.html', {'form': form})

    def post(self, request):
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            form.save_m2m()
            return redirect('event', uuid=event.uuid)
        return render(request, 'bbqplanner/event_create.html', {'form': form})


class ListEvents(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    template_name = 'bbqplanner/events.html'
    context_object_name = 'upcoming_events'

    def get_queryset(self):
        events = [get_event_summary(self.request, e) for e in (
            BBQEvent.objects
                .filter(organizer=self.request.user, date__gte=datetime.now().date())
                .prefetch_related('available_products', 'visitors', 'visitors__desired_products')
        )]
        return events


class EventRegistrationSuccess(generic.TemplateView):
    template_name = 'bbqplanner/event_register_success.html'

def index(request):
    return render(request, 'index.html')
