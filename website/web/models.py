from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User 
from datetime import date
# Create your models here.
class Member(models.Model):
    fname = models.CharField(max_length=50)
    mdname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    age = models.IntegerField()
    email= models.EmailField(max_length=50)
    passwd = models.CharField(max_length=50)
    phone= models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    

    def __str__(self):
        return self.fname + ' ' + self.lname
class Venue(models.Model):
    name= models.CharField('Venue Name', max_length=120)
    address = models.CharField( max_length=300)
    zip_code =models.CharField('Zip Code', max_length=15)
    pnone = models.CharField('Contact Phone', max_length=11)
    web= models.URLField('Web Address')
    email_address= models.EmailField('Email Address')
    owner= models.IntegerField('venue owner', blank=False,default=1)
    venue_image=models.ImageField(null=True,blank=True, upload_to='images/')
    def __str__(self):
        return self.name 
        
class Event(models.Model):
    name= models.CharField('Event Name', max_length=120)
    event_date=models.DateField('Event Date')
    Venue= models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    #venue= models.CharField(max_length=120)
    manager =models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    #manager =models.CharField('Manager', max_length=120)
    description=models.TextField(blank=True)
    attendees= models.ManyToManyField(Member, blank=True)
    approved= models.BooleanField("Approved", default=False)

    def __str__(self):
        return self.name 

    @property
    def Days_till(self):
        today=date.today()
        days_till=self.event_date - today
        days_till_stripped=str(days_till).split(",", 1)[0]
        
        return days_till_stripped

    @property
    def Is_past(self):
        today=date.today()
        if self.event_date < today:
            thing= "Event ended"
        else:
            thing='Event will commence in '
        return thing



