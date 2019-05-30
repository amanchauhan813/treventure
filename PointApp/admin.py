# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(BusOrganisation)
admin.site.register(Route)
admin.site.register(Bus)
admin.site.register(Schedule)
admin.site.register(Ticket)

admin.site.register(Hotels)
admin.site.register(Room)
admin.site.register(Booking)
