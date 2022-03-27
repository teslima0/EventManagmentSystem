
from asyncio import events
from datetime import datetime
from pickle import FALSE
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
#from numpy import append
import csv
from .models import Member, Event, Venue
from .forms import MemberForm, VenueForm, EventForm, EventFormAdmin
from django.contrib import messages
# Create your views here
from django.http import FileResponse
import io
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
import calendar
from calendar import HTMLCalendar, month_name



def home(request,yyyy=datetime.now().year,mm=datetime.now().strftime('%B')):
    name='Tamarcom'
    #converting first letter of the month  to uppercase
    #mm=mm.title()
    #converting every single letter of the month  to uppercase
    mm=mm.capitalize()
    #convert month to number
    month_number=list(calendar.month_name).index(mm)
    #convert month no to integer
    month_number=int(month_number)
    #create a calender
    cal=HTMLCalendar().formatmonth(yyyy,month_number)
    #get current time
    now=datetime.now()
    current_year=now.year
    #get current time
    time=now.strftime('%I:%M %p')
    #query the event model for dates
    event_list= Event.objects.filter(
        event_date__year=datetime.now().year,
        event_date__month=month_number
    )
    return render(request,'index.html',{'yyyy':yyyy,'mm':mm,
    'month_number':month_number, 'cal':cal,
    'current_year':current_year,'time':time,'name':name,
    'event_list':event_list})


def my_events(request,*args,**kwargs):
    if request.user.is_authenticated:
        
        me=request.user.id
        events=Event.objects.filter(attendees=me)
        return render(request, 'my_events.html', {'events':events} )
    else:
        messages.success(request,('you are not authorised to view this page'))
        return redirect('homepage')

def venue_text(request):
    response=HttpResponse( content_type='text/plain')
    response['Content-Disposition']= 'attachment; filename=venues.txt'
    # to write manually
    #lines=['This is line 1\n'
    #'This is line 2\n'
    #'This is line3']
    #response.writelines(lines)
    #return response
    #from database
    venues=Venue.objects.all()
    #create blank list
    lines=[]
    #loop thru and output
    for venue in venues:
        lines.append(f'{venue.name}\n {venue.address}\n {venue.pnone}\n {venue.zip_code}\n {venue.email_address}\n {venue.web}\n\n\n')

    response.writelines(lines)
    return response

def venue_csv(request):
    response=HttpResponse( content_type='text/csv')
    response['Content-Disposition']= 'attachment; filename=venues.csv'
    #create a csv writer
    writer=csv.writer(response)
    #database designate
    venues=Venue.objects.all()
    #add heading to csv colomn
    writer.writerow(['Venue Name','Venue Address','Venue Zip Code','Venue Phone No','Venue Web Address','Venue Email'])
    
    #loop thru and output
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.pnone, venue.zip_code, venue.email_address, venue.web])
    return response

def Search_member(request):
    if request.method == "POST":
        searched = request.POST['searched']
        members=Member.objects.filter(lname__contains=searched)

        return render(request, 'search_member.html', {'searched':searched,'members':members})
    else:
        return render(request, 'search_member.html', {})


def SearchView(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues=Venue.objects.filter(name__contains=searched)

        return render(request, 'search_venue.html', {'searched':searched,'venues':venues})
    else:
        return render(request, 'search_venue.html', {})

def Search_events(request):
    if request.method == "POST":
        searched = request.POST['searched']
        events=Event.objects.filter(description__contains=searched)

        return render(request, 'search_events.html', {'searched':searched,'events':events})
    else:
        return render(request, 'search_events.html', {})

def ShowVenue(request, venue_id):
    
    venue= Venue.objects.get(pk=venue_id)
    venue_owner=User.objects.get(pk=venue.owner)
    #grab event from that venue
    events=venue.event_set.all()
    return render(request, 'Show_venue.html', {'venue': venue,'venue_owner':venue_owner,'events':events})

def UpdateVenue(request, venue_id):
    venue= Venue.objects.get(pk=venue_id)
    name=venue.name
    address=venue.address
    zip_code=venue.zip_code
    phone=venue.pnone
    web=venue.web
    email=venue.email_address
    form=VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('venueView')
    return render(request, 'update_venue.html', {'venue': venue, "form":form, 'name':name,
    'address':address, 'zip_code':zip_code,'phone':phone, 'web':web, 'email':email})

def Update_member(request, member_id):
    member= Member.objects.get(pk=member_id)
    fname=member.fname
    mdname=member.mdname
    lname=member.lname
    age=member.age
    phone=member.phone
    email=member.email
    passwd=member.passwd
    address=member.address
    form=MemberForm(request.POST or None, request.FILES or None, instance=member)
    if form.is_valid():
        form.save()
        return redirect('ViewMembers')
    return render(request, 'update_member.html', {'fname': fname, "form":form, 'mdname':mdname,

    'passwd':passwd, 'address':address, 'lname':lname,'phone':phone, 'age':age, 'email':email})



def UpdateEvent(request, event_id):
    event= Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form=EventFormAdmin(request.POST or None, instance=event)
    else:
        form=EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()  
        return redirect('eventpage')
    return render(request,'update_event.html',{'event':event, 'form':form })

def DeleteEvent(request, event_id):
    event= Event.objects.get(pk=event_id)
    if request.user==event.manager:
        event.delete()
        messages.success(request,('event deleted'))
        return redirect('eventpage')
    else:
        messages.success(request,('you are not authorised to delete this event'))
    
        return redirect('eventpage')
    

def DeleteVenue(request, venue_id):
    venue= Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('venueView')

def Delete_member(request, member_id):
    member= Member.objects.get(pk=member_id)
    member.delete()
    return redirect('ViewMembers')
'''
def VenueFormView(request):
    if request.method == "POST":
        form= VenueForm(request.POST)
        if form.is_valid():
           venue = form.save(commit=False) #temporay save the form in venue
           venue.owner=request.user.id
           venue.save()
           #form.save()
           
        else:
            name= request.POST['name']
            address= request.POST['address']
            zip_code= request.POST['zip_code']
            pnone= request.POST['pnone']
            web= request.POST['web']
            email_address= request.POST['email_address']
            messages.success(request, ('something went wrong'))
            return render(request,'venue.html',{'name':name,
            'address':address, 'zip_code':zip_code, 'pnone':pnone,
             'web':web, 'email_address':email_address
            }) 
        messages.success(request, ("Your Form Has Been Submitted"))

        return redirect('venueView')
    else:

        return render(request, 'venue.html', {})
'''         
def VenueFormView(request):
    submitted= False
    if request.method == "POST":
        
        form= VenueForm(request.POST, request.FILES )
        if form.is_valid():
            
            venue = form.save(commit=False) #temporay save the form in venue
            venue.owner=request.user.id
            venue.save()
            #form.save()
           
            return HttpResponseRedirect('/add-venue?submitted=True')
    else:
        form=VenueForm
        if 'submitted' in request.GET:
                submitted=True
    return render(request,'venue.html',{'form':form, 'submitted':submitted })


def EventFormView(request):
    submitted= False
    #submiting form
    if request.method == "POST":
        if request.user.is_superuser:
            form= EventFormAdmin(request.POST )
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add-event?submitted=True')
        else:
            form= EventFormAdmin(request.POST )
            if form.is_valid():
                event = form.save(commit=False) #temporay save the form in venue
                event.manager=request.user #assign user as manager
                event.save()
                return HttpResponseRedirect('/add-event?submitted=True')
    else:
        #just going to the page, not submitting
        if request.user.is_superuser:
            form= EventFormAdmin
        else:  
            form=EventForm
        if 'submitted' in request.GET:
                submitted=True
    return render(request,'event_reg.html',{'form':form, 'submitted':submitted })


def joinFormView(request):
    if request.method == "POST":
        form= MemberForm(request.POST or None)
        if form.is_valid():
            form.save()
        else:
            fname= request.POST['fname']
            mdname= request.POST['mdname']
            lname= request.POST['lname']
            age= request.POST['age']
            email= request.POST['email']
            passwd= request.POST['passwd']
            phone= request.POST['phone']
            address= request.POST['address']
            messages.success(request, ('something went wrong'))
            #return redirect('RegPage')
            return render(request,'registration.html',{'fname':fname,
            'mdname':mdname, 'lname':lname, 'age':age,
            'email':email, 'passwd':passwd, 'phone': phone, 'address':address
            })

        messages.success(request, ("Your Form Has Been Submitted"))

        return redirect('homepage')
    else:

        return render(request, 'registration.html', {})


def EventView(request):
    all_event= Event.objects.all().order_by('-event_date')
    
    return render(request, 'event_list.html', {'all_event':all_event})


def Edit_member(request):
    members= Member.objects.all().order_by('lname')
    
    p=Paginator(Member.objects.all(), 5)
    page=request.GET.get('page')
    members=p.get_page(page)
    nums= 'a' * members.paginator.num_pages
    
    
    return render(request, 'edit_member.html', {'members':members,'nums':nums})
#show event

def Show_event(request, event_id):
    event = Event.objects.all().get(id=event_id)
    return render(request, 'show_event.html', {'event':event})


def Show_member(request,member_id):
    member = Member.objects.all().get(id=member_id)
    return render(request, 'show_member.html', {'member':member})


#show event in a venue
def Venue_event(request, venue_id):
    #grab the venue
    venue = Venue.objects.all().get(id=venue_id)
    #grab the events associated  to that venue
    events=venue.event_set.all()
    if events:
        return render(request, 'venue_event.html', {'events':events})
    else:
        messages.success(request, ('The Venue has no event yet'))
        return redirect('admin_approval')

def admin_approval(request):
    #get venue list
    venue_list=Venue.objects.all()
    #get count
    event_count=Event.objects.all().count()
    venue_count= Venue.objects.all().count()
    user_count=User.objects.all().count()
    event_list=Event.objects.all().order_by('-event_date')
    
    if request.user.is_superuser:
        if request.method=='POST':
            id_list=request.POST.getlist('boxes')
            #uncheck all events
            event_list.update(approved=False)
            #update the database
            for x in id_list :
                Event.objects.filter(pk=int(x)).update(approved=True)

            messages.success(request, ('The event has been updated successfully'))
            return redirect('eventpage')
        else:

             return render(request, 'admin_approval.html', {'event_list':event_list, 'event_count':event_count,
             'venue_count':venue_count, 'user_count':user_count,'venue_list':venue_list})
    else:
        
        messages.success(request, ('You are not authorize to view this page'))
        return redirect('homepage')

    
    return render(request, 'admin_approval.html', {})


def MembersView(request):
    
    all_mebers= Member.objects.all()
    p=Paginator(Member.objects.all(), 5)
    page=request.GET.get('page')
    members=p.get_page(page)
    nums= 'a' * members.paginator.num_pages
    
    
    return render(request, 'list_member.html', { 'all': all_mebers, 'members':members, 'nums':nums })


def VenueView(request):
    #all_venue= Venue.objects.all().order_by('?') # random oder (r) from the the dabase 
    all_venue= Venue.objects.all()
    #set pagination i.e next1 -> page2
    p=Paginator(Venue.objects.all(), 4)
    page=request.GET.get('page')
    venues=p.get_page(page)
    nums= 'a' * venues.paginator.num_pages
    return render(request, 'list_venue.html', { "all_venue":all_venue, 'venues':venues,'nums':nums  })