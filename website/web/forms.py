from logging import PlaceHolder
from multiprocessing import Event

from django import forms

from .models import Member, Venue, Event

from django.forms import ModelForm

class MemberForm(forms.ModelForm):
    class Meta:
        model=Member
        fields= ['fname','mdname','lname','age','email','passwd','phone','address']
'''
class VenueForm(ModelForm):
    class Meta:
        model=Venue
        fields="__all__"
'''
class VenueForm(ModelForm):
    class Meta:
        model=Venue

        fields = ('name', 'address','zip_code','pnone','web','email_address', 'venue_image')
        labels = {
            'name' : '',
            'address' : '',
            'zip_code' : '',
            'pnone' : '',
            'web' : '',
            'email_address' : '',
            'venue_image' :'',
        }

        widgets = {
                
                'name' :forms.TextInput(attrs={'class': 'form-control','placeholder':' name'}),
                'address' : forms.TextInput(attrs={'class': 'form-control','placeholder':'address'}),
                'zip_code' : forms.TextInput(attrs={'class': 'form-control','placeholder':'zip code'}),
                'pnone' : forms.TextInput(attrs={'class': 'form-control','placeholder':'phone number'}),
                'web' : forms.URLInput(attrs={'class': 'form-control','placeholder':'website'}),
                'email_address' : forms.EmailInput(attrs={'class': 'form-control','placeholder':'email'}),
        }
#admin superuser form
class EventFormAdmin(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date','Venue','manager','attendees','description')
        labels = {
            'name' : ' name',
            'event_date' : 'YYYY-MM-DD',
            'Venue' : ' Venue',
            'manager' : 'manager ',
            'attendees' : ' attendees',
            'description' : 'description ',
            
        }

        widgets = {
                
                'name' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Event name'}),
                'event_date' : forms.TextInput(attrs={'class': 'form-control','placeholder': 'Event Date'}),
                'Venue' : forms.Select(attrs={'class': 'form-select', 'placeholder': 'venue'}),
                'manager' : forms.Select(attrs={'class': 'form-select', 'placeholder': 'manager'}),
                'attendees' : forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'attendees'}),
                'description' : forms.Textarea(attrs={'class': 'form-control', 'placeholder':'description'}),
        }

# for none admin user 

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date','Venue','attendees','description')
        labels = {
            'name' : ' name',
            'event_date' : 'YYYY-MM-DD',
            'Venue' : ' Venue',
            'attendees' : ' attendees',
            'description' : 'description ',
        }

        widgets = {
                
                'name' : forms.TextInput(attrs={'class': 'form-control','placeholder':'Event name'}),
                'event_date' : forms.TextInput(attrs={'class': 'form-control','placeholder': 'Event Date'}),
                'Venue' : forms.Select(attrs={'class': 'form-select', 'placeholder': 'venue'}),
                'attendees' : forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'attendees'}),
                'description' : forms.Textarea(attrs={'class': 'form-control', 'placeholder':'description'}),
        }
