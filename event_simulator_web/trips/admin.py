# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.contrib import admin, messages

from trips.models import DummyTrip
from simulator.trip import fire_trip_simulation_event


def start_trip_simulation(modeladmin, request, queryset):
    status_mapping = {
        'success': [],
        'fail': []
    }
    for obj in queryset:
        fired = fire_trip_simulation_event(
            obj.operator_name,
            obj.shuttle_identifier,
            obj.polyline
        )
        if fired:
            status_mapping['success'].append(obj.shuttle_identifier)
        else:
            status_mapping['fail'].append(obj.shuttle_identifier)

    success = status_mapping['success']
    if success:
        msg = 'Simulations started for: {}'.format(','.join(success))
        modeladmin.message_user(request, msg, messages.SUCCESS)
    fail = status_mapping['fail']
    if fail:
        msg = 'Simulations could not be started for: {}'.format(
            ','.join(success)
        )
        modeladmin.message_user(request, msg, messages.ERROR)

start_trip_simulation.short_description = 'Start simulation'


class DummyTripAdmin(admin.ModelAdmin):
    list_display = (
        'operator_name',
        'shuttle_identifier',
    )
    exclude = ('shuttle_identifier', )
    list_filter = ('operator_name', )
    search_fields = (
        'operator_name',
    )
    actions = [start_trip_simulation]

    def save_model(self, request, obj, form, change):
        now = datetime.now()
        operator_name = obj.operator_name.title()
        operator_name_args = operator_name.split(' ')
        operator_name_shortcut = ''.join(
            [arg[0].title() for arg in operator_name_args]
        )
        shuttle_identifier = '{}-{}'.format(
            operator_name_shortcut,
            now.strftime('%Y%m%d%H%M%S')
        )
        obj.shuttle_identifier = shuttle_identifier
        obj.operator_name = operator_name
        super(DummyTripAdmin, self).save_model(request, obj, form, change)


admin.site.register(DummyTrip, DummyTripAdmin)
