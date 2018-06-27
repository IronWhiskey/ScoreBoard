# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Admin, Player, Record, Game, Message, Comment, League


# Register your models here.
admin.site.register(Admin)
admin.site.register(Player)
admin.site.register(Record)
admin.site.register(Game)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(League)