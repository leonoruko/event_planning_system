from rest_framework import serializers
from .models import Event,Venue,RSVP,Guest,Expenses,Vendor

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields='__all__'

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model=Venue
        fields='__all__'

class RSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model=RSVP
        fields='__all__'

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Guest
        fields='__all__'

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expenses
        fields='__all__'

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields="__all__"

