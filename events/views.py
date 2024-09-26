from django.shortcuts import render
from rest_framework import permissions,status
from .serializers import EventSerializer,VenueSerializer,GuestSerializer,RSVPSerializer,ExpensesSerializer,VendorSerializer
from rest_framework.views import APIView
from .models import Event,Venue,Guest,RSVP,Expenses,Vendor
from rest_framework.response import Response
# Create your views here.

class EventListCreateView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        events=Event.objects.filter(user=request.user)
        serializer=EventSerializer(events,many=True)
        return Response(serializer.data)
    def post(self, request):        
        venue_details = request.data.get('venue_details')
        
        if venue_details:
            venue_name = venue_details.get('venue_name')
            venue_details['user'] = request.user
            
            # Use the correct format for get_or_create
            venue, created = Venue.objects.get_or_create(
                venue_name=venue_name, 
                defaults=venue_details
            )
            
            # Update request data to include venue ID
            request.data['venue'] = venue.id
        else:
            return Response({"error": "Venue details are required."}, status=status.HTTP_400_BAD_REQUEST)

        request.data['user'] = request.user.id
        serializer = EventSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetailView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self,pk,user):
        try:
            return Event.objects.get(pk=pk,user=user)
        except Event.DoesNotExist:
            return None
        return

    def get(self,request,pk):
        event=self.get_object(pk,request.user)
        if event:
            serializer=EventSerializer(event)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"error":"Event not found"},status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        event = self.get_object(pk, request.user)
        
        if not event:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        venue_details = request.data.get('venue_details')
        
        if venue_details:
            venue_name = venue_details.get('venue_name')
            venue_details['user'] = request.user.id  # Correctly set user ID
            
            # Use the correct format for get_or_create
            venue, created = Venue.objects.get_or_create(
                name=venue_name, 
                defaults=venue_details
            )
            
            # Update request data to include venue ID
            request.data['venue'] = venue.id
        
        # Now process the event update
        serializer = EventSerializer(event, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self,request,pk):
        event=self.get_object(pk,request.user)
        if event:
            try:
                guests=Guest.objects.get(id=event.id)
                event.delete()
                return Response({"detail":"Event deleted successfully"},status=status.HTTP_204_NO_CONTENT)
            except:
                return 
        return Response({"error":"Event not found"},status=status.HTTP_404_NOT_FOUND)
    
class VenueListCreateView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(self,request):
        serializer=VenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
    def get(self,request):
        venues=Venue.objects.filter(user=request.user)
        serializer=VenueSerializer(venues,many=True)
        return Response(serializer.data)

class VenueDetailsView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get_object(self,user,pk):
        try:
            venue=Venue.objects.get(user=user,pk=pk)
            return venue
        except Venue.DoesNotExist:
            return None         
        
    def get(self,request, pk):
        user=request.user
        venue = self.get_object(user,pk)
        if venue:
            serializer = VenueSerializer(venue)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Venue not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,pk):
        venue=Venue.objects.get(user=request.user,pk=pk)
        if not venue:
            return Response({"error":"venue not found"},status=status.HTTP_404_NOT_FOUND)  
        serializer=VenueSerializer(venue,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)


class GuestListCreateView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        guests=Guest.objects.filter(invited_by=request.user)
        serializer=GuestSerializer(guests,many=True)                        
        return  Response(serializer.data)
    
    def post(self,request):
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class GuestDetailsView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get_object(self,user,pk):        
        try:
            guest=Guest.objects.get(invited_by=user,pk=pk)
            return guest
        except:
            return None

    def get(self,request,pk):
        guest=self.get_object(request.user,pk)
        if guest:
            serializer=GuestSerializer(guest)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"error":"Guest not found"},status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk):
        guest=self.get_object(request.user,pk)
        if guest:
            serializer=GuestSerializer(guest,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        
        return Response({"error":"guest not found"},status=status.HTTP_400_BAD_REQUEST)
    
class RSPVListCreateView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request,event_id):        
        try:
            event=Event.objects.get(id=event_id)
            rsvps=RSVP.objects.filter(event=event)
            serializer=RSVPSerializer(rsvps,many=True)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response({"error":"Event Does not exist"},status=status.HTTP_404_NOT_FOUND)
    def get_object(self,guest_id,event_id):
        try:
            rsvp=RSVP.objects.get(guest_id=guest_id,event__id=event_id)
            return rsvp
        except RSVP.DoesNotExist:
            return None
    def post(self,request,event_id,guest_id):
        try:
            event=Event.objects.get(event_id=event_id)
            guest=Guest.objects.get(guest_id=guest_id)
        except Event.DoesNotExist:
            return Response({"error":"Event not found"},status=status.HTTP_404_NOT_FOUND)
        except Guest.DoesNotExist:
            return Response({"error":"Guest not found"},status=status.HTTP_404_NOT_FOUND) 
        rsvp=self.get_object(guest_id,event_id)         
        if not rsvp:            
            data=request.data.copy()  
            data["event"]=event.id
            data["guest"]=guest.id
            serializer=RSVPSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"You've already done this"},status=status.HTTP_302_FOUND)
class RSVPUpdateView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,pk):
        try:
            rsvp=RSVP.objects.get(pk=pk)
            serializer=RSVPSerializer(rsvp)
            return Response(serializer.data,status=status.HTTP_200_OK)            
        except:
            return Response({"error":"RSVP not found"},status=status.HTTP_404_NOT_FOUND)

    def put(self,request,rsvp_id):
        try:
            rsvp=RSVP.objects.get(id=rsvp_id)
        except RSVP.DoesNotExist:
            return Response({"error":"RSVP not found"},status=status.HTTP_404_NOT_FOUND)
        
        serializer=RSVPSerializer(rsvp,data=request.data)
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ExepenseListCreateView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request,event_id):
        try:
            expenses=Expenses.objects.filter(event__id=event_id)
            serializer=ExpensesSerializer(expenses,many=True)            
            return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({"error":"Event not found"},status=status.HTTP_404_NOT_FOUND)        
    
    def post(self,request,event_id):
        try:
            event=Event.objects.get(event_id=event_id)
            data=request.data.copy()
            data["event"]=event.id
            serializer=ExpensesSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist:
            return Response({"error":"Event Does not exist"},status=status.HTTP_404_NOT_FOUND)
class ExpenseDetailsView(APIView):
    def get(self,request,pk):
        try:
            expense=Expenses.objects.get(pk=pk)
            serializer=ExpensesSerializer(expense)
            if serializer.is_valid():
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Expenses.DoesNotExist:
            return Response({"error":"Expense Does not exist"},status=status.HTTP_404_NOT_FOUND)

    def put(self,request,pk):
        try:
            expense=Expenses.objects.get(pk=pk)
            serializer=ExpensesSerializer(expense,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.erros,status=status.HTTP_400_BAD_REQUEST)
        except Expenses.DoesNotExist:
            return Response({"error":"Expense not found"},status=status.HTTP_404_NOT_FOUND)

class VendorListCreateView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        vendors=Vendor.objects.all()
        serializer=VendorSerializer(vendors,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class VendorDetailsView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,pk):
        try:
            vendor=Vendor.objects.get(pk=pk)
            serializer=VendorSerializer(vendor)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({"error":"Vendor not found"},status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,pk):
        try:
            vendor=Vendor.objects.get(pk=pk)
            serializer=VendorSerializer(vendor,request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)                
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Vendor.DoesNotExist:
            return Response({"error":"vendor not found"},status=status.HTTP_404_NOT_FOUND)
        
    def delete(self,request,pk):
        try:
            vendor=Vendor.objects.get(pk=pk)
            vendor.delete()
            return Response({"":""},status=status.HTTP_202_ACCEPTED)
        except Vendor.DoesNotExist:
            return Response({"error":"vendor not found"},status=status.HTTP_404_NOT_FOUND)
       
