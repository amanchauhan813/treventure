from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm
from PointApp.models import Ticket, Booking
import phonenumbers


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=False, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    class Meta:
        model = User
        fields = ('username',  'name', 'birth_date', 'email', 'password1', 'password2' )

class TicketForm(forms.ModelForm):
  '''
  Class to create a form for a user to get a ticket
  '''
  # phone_number = forms.CharField(max_length = 255)

  class Meta:
    model = Ticket

    fields = ('first_name', 'last_name', 'email', 'phone_number')

  def clean(self):
    
    cleaned_data = super(TicketForm, self).clean()

    gotten_phone_number = cleaned_data.get('phone_number')

    if len(gotten_phone_number) != 10:
    
        raise forms.ValidationError('The phone number is not a valid')

    return cleaned_data
        

class BookingForm(forms.ModelForm):
  
  class Meta:
    model = Booking

    fields = ('name', 'phone_number')

  def clean(self):
    
    cleaned_data = super(BookingForm, self).clean()

    gotten_phone_number = cleaned_data.get('phone_number')

    if len(gotten_phone_number) != 10:
    
        raise forms.ValidationError('The phone number is not a valid')

    return cleaned_data
  