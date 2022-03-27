from django.urls import path
from .views import *
from .import views 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    #path converter
    #1. int: for number
    #2 str: for string
    #3 path: whole urls/
    #4. slug: hyphen- and_underscore_stuff
    #5  UUID: universally unique identifier
    
    path('', home, name = 'homepage'),
    path('<int:yyyy>/<str:mm>', home, name='homepage'),
    path('join', joinFormView, name = 'Regpage'),
    path('view-event', EventView, name = 'eventpage'),
    path('update_member', Edit_member, name = 'edit_member'),
    path('view-members', MembersView, name = 'ViewMembers'),
    path('add-venue', VenueFormView, name = 'venueReg'),
    path('add-event', EventFormView, name = 'eventReg'),
    path('view-venue', VenueView, name = 'venueView'),
    path('search-venues', SearchView, name = 'search_venue'),
    path('Show_venue/<venue_id>', ShowVenue, name = 'ShowVenueView'),
    path('Update_venue/<venue_id>', UpdateVenue, name = 'UpdateVenueView'),
    path('Update_event/<event_id>', UpdateEvent, name = 'Update-event'),
    path('Update_member/<member_id>', Update_member, name = 'Update-member'),
    path('delete_event/<event_id>', DeleteEvent , name = 'delete-event'),
    path('delete_venue/<venue_id>', DeleteVenue , name = 'delete-venue'),
    path('delete_member/<member_id>', Delete_member , name = 'delete-member'),
    path('venue_text', venue_text, name = 'venue_text'),
    path('venue_csv', venue_csv, name = 'venue_csv'),
    path('my_events', my_events, name = 'my_events'),
    path('search_events', Search_events, name = 'search_events'),
    path('admin_approval', admin_approval, name = 'admin_approval'),
    path('venue_event/<venue_id>', Venue_event, name = 'venue_event'),
    path('Show_event/<event_id>', Show_event, name = 'Show_event'),
    path('search_members', Search_member, name = 'search_member'),
    path('Show_member/<member_id>', Show_member, name = 'Show_member'),


]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

                    