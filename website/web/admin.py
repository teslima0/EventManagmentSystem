from django.contrib import admin
from .models import Member, Event, Venue
# Register your models here.
from django.contrib.auth.models import Group

admin.site.register(Member)
admin.site.unregister(Group)
#admin.site.register(Event)
#admin.site.register(Venue)
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display=('name','address','pnone')
    ordering=('name',)
    search_fields= ('name', 'address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields= (('name', 'Venue'), 'event_date', 'description', 'manager',  'approved')
    list_filter=('event_date', 'Venue' )
    ordering=('event_date',)

#configure Admin Title
admin.site.site_header= "My Club Administration Page"
admin.site.site_title= "Browser Title"
admin.site.index_title= "Mr president Key note address"