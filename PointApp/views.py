# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from .models import BusOrganisation, Route, Bus, Schedule, Ticket, Hotels, Room, Booking
from datetime import datetime, date
from .forms import TicketForm, SignUpForm, BookingForm
import uuid
import phonenumbers
import random

def index(request):
   return render(request,'catalog/index.html')
   
def flights(request):
   return render(request,'catalog/flights.html') 
   
def holidays(request):
   return render(request,'catalog/holidays.html') 

def searchtravals(request):
   return render(request,'catalog/searchtraval.html') 

def searchhotels(request):
   return render(request,'catalog/searchhotels.html') 

def contact(request):
   return render(request,'catalog/contact.html') 

def errors(request):
   return render(request,'catalog/error.html') 

def allbuss(request):
    #    title = 'Result'
       # all_schedule = Schedule.get_schedules()
    #return render(request, 'catalog/allbus.html', {'title':title,  'buses':all_schedule})
    title = 'All Buss'
    all_schedule = Schedule.get_schedules()
    return render(request,'catalog/allbus.html', {'title':title,  'buses':all_schedule}) 

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'catalog/signup.html', {'form': form})


def search_results(request):
    '''
    View function to get the the requested departure and arrival locations from the database and display to the user
    '''
    try:
        title = 'Result'

        if ('depature-location' in request.GET and request.GET['depature-location']) and ('arrival-location' in request.GET and request.GET['arrival-location']) and ('travel-date' in request.GET and request.GET['travel-date']):

            # Get the input departure
            search_departure_location = request.GET.get('depature-location').title()

            # Get the input arrival location
            search_arrival_location = request.GET.get('arrival-location').title()

            # Get the input date
            travel_date = request.GET.get('travel-date')

            # Convert string input to date type
            convert_to_date = datetime.strptime(travel_date, '%Y-%m-%d').date()

            # Get the route 
            result_route = Route.get_search_route(search_departure_location,search_arrival_location)
            print(result_route)

            # Check if route exists found
            if result_route != None :
                
                # Schedule with the same depature date
                schedule_with_depature_date = Schedule.get_departure_buses(convert_to_date, result_route.id)

                if len(schedule_with_depature_date) > 0:

                    for schedule in schedule_with_depature_date:

                        estimation_duration = Schedule.get_travel_estimation(schedule.id)

                    return render(request, 'catalog/search.html', {'title':title, 'search_departure_location':search_departure_location, 'search_arrival_location':search_arrival_location, 'convert_to_date':convert_to_date, 'buses':schedule_with_depature_date, 'estimation_duration':estimation_duration})

                else:
                    print('no scheduled buses')
                    no_scheduled_bus_message = 'No scheduled buses'

                    return render(request, 'catalog/search.html', {'title':title, 'no_scheduled_bus_message':no_scheduled_bus_message, 'search_departure_location':search_departure_location, 'search_arrival_location':search_arrival_location, 'convert_to_date':convert_to_date})

            # Otherwise
            else:
                
                no_route_message = 'Bus route not found'

                return render(request, 'catalog/search.html', {'title':title, 'no_route_message':no_route_message, 'search_departure_location':search_departure_location, 'search_arrival_location':search_arrival_location, 'convert_to_date':convert_to_date})
        
    except ObjectDoesNotExist:

        return redirect(Http404)

def bus_details(request, bus_schedule_id):
    '''
    View function to display a form for the user to fill to get a ticket
    '''
    try:
        # args = {}

        selected_bus = Schedule.get_single_schedule(bus_schedule_id)

        title = '{selected_bus.bus.bus_organisation} Schedule Details'

        estimation_duration = Schedule.get_travel_estimation(bus_schedule_id)

        if request.method == 'POST':
            
            form = TicketForm(request.POST)

            if form.is_valid():
                
                ticket = form.save(commit=False)

                ticket.schedule = selected_bus

                ticket.ticket_number = uuid.uuid4()

                ticket.save()

                ticket_id = ticket.id

                return redirect(mobile_payment, ticket_id)

        else:

            form = TicketForm()

        # args['form'] = form

        return render(request, 'catalog/bus_details.html', {'title':title, 'form':form, 'selected_bus':selected_bus, 'estimation_duration':estimation_duration})

    except ObjectDoesNotExist:

         return redirect(Http404)

def mobile_payment(request, ticket_id):
    '''
    Function that carries out the payment process 

    '''
    # Get ticket with a given id 
    ticket = Ticket.get_single_ticket(ticket_id)

    # Get the route and convert to string
    bus_route = str((ticket.schedule.bus.bus_organisation.name))
    print(type(bus_route))

    # Get the phone number
    phone_number = ticket.phone_number
    print(type(phone_number))

    # Get the ticket price and convert Decimal to int
    ticket_price = float(ticket.schedule.price)
    print(type(ticket_price))
        
    ticket.transaction_code = random.randint(1000,1000000) 
    ticket.save()

    print(ticket.transaction_code)

    return render(request, 'catalog/ticketdetail.html', {'ticket':ticket, 'ticket_id':ticket_id})


def search_hotel_results(request):    
    try:
        title = 'Hotel Result'

        if ('depature-location' in request.GET and request.GET['depature-location']) and ('check-in-date' in request.GET and request.GET['check-in-date']) and ('check-out-date' in request.GET and request.GET['check-out-date']):

            # Get the input departure
            search_departure_location = request.GET.get('depature-location').title()

            # Get the input arrival location
            check_in_date = request.GET.get('check-in-date')

            # Get the input date
            check_out_date = request.GET.get('check-out-date')

            # Convert string input to date type
            convert_to_check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            convert_to_check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()

            if convert_to_check_in_date < datetime.now().date():
                print('Invalid CheckIn Date')
                no_scheduled_bus_message = 'Invalid CheckIn Date'

                return render(request, 'catalog/searchResult.html', {'title':title, 'no_scheduled_bus_message':no_scheduled_bus_message, 'search_departure_location':search_departure_location, 'convert_to_check_in_date':convert_to_check_in_date, 'convert_to_check_out_date':convert_to_check_out_date})

            # Get the route 
            result_hotel = Hotels.get_search_hotels(search_departure_location)
            print(result_hotel)

            # Check if route exists found
            if result_hotel != None :
                #convert_to_check_in_date, convert_to_check_out_date,
                avaialbleRoom = Room.get_hotel_rooms(result_hotel.id)

                if len(avaialbleRoom) > 0:
                    for roomObj in avaialbleRoom:
                        result_booking = Booking.get_book_hotel_room(roomObj.id, convert_to_check_in_date, convert_to_check_out_date)
                        print(result_booking)
                    # if result_booking != None:
                    #     print(result_booking.room.id)
                    #     print('Hotel Room was booked')
                    #     no_scheduled_bus_message = 'Hotel Room is already booked'

                    #     return render(request, 'catalog/searchResult.html', {'title':title, 'no_scheduled_bus_message':no_scheduled_bus_message, 'search_departure_location':search_departure_location, 'convert_to_check_in_date':convert_to_check_in_date, 'convert_to_check_out_date':convert_to_check_out_date})

                    # else:

                        return render(request, 'catalog/searchResult.html', {'title':title, 'search_departure_location':search_departure_location, 'convert_to_check_in_date':convert_to_check_in_date, 'convert_to_check_out_date':convert_to_check_out_date, 'avaialbleRoom':avaialbleRoom, 'result_booking':result_booking})

                else:
                    print('no hotels available')
                    no_scheduled_bus_message = 'No Hotels Available'

                    return render(request, 'catalog/searchResult.html', {'title':title, 'no_scheduled_bus_message':no_scheduled_bus_message, 'search_departure_location':search_departure_location, 'convert_to_check_in_date':convert_to_check_in_date, 'convert_to_check_out_date':convert_to_check_out_date})

            # Otherwise
            else:
                
                no_route_message = 'Hotels not found'

                return render(request, 'catalog/searchResult.html', {'title':title, 'no_route_message':no_route_message, 'search_departure_location':search_departure_location, 'convert_to_check_in_date':convert_to_check_in_date, 'convert_to_check_out_date':convert_to_check_out_date})
        
    except ObjectDoesNotExist:

        return redirect(Http404)



def room_details(request, room_id, check_in_date, check_out_date):

    try:

        selected_room = Room.get_single_room(room_id)

        title = '{selected_room.hotels.name} Details'        

        if request.method == 'POST':
            
            form = BookingForm(request.POST)

            if form.is_valid():
                
                Booking = form.save(commit=False)

                Booking.room = selected_room
                Booking.check_in = check_in_date
                Booking.check_out = check_out_date
                Booking.price = selected_room.price

                Booking.save()     

            return redirect(room_booked)

        else:

            form = BookingForm()
            return render(request, 'catalog/room_details.html', { 'title':title, 'form':form ,'selected_room':selected_room, 'check_in_date':check_in_date,'check_out_date':check_out_date})

    except ObjectDoesNotExist:

         return redirect(Http404)


def room_booked(request):
   return render(request,'catalog/roombooked.html')