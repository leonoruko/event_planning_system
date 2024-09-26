from django.urls import path
from .views import EventDetailView,EventListCreateView,VenueDetailsView,VenueListCreateView,RSPVListCreateView,RSVPUpdateView,GuestListCreateView,GuestDetailsView
urlpatterns=[
    path("",EventListCreateView.as_view(),name="event-list-create"),
    path("<int:pk>/",EventDetailView.as_view(),name="event-details"),
    path("venues/",VenueListCreateView.as_view(),name="venue-list-create"),
    path("venue/<int:pk>/",VenueDetailsView.as_view(),name="venue-details"),
    path('<int:event_id>/rsvps/', RSPVListCreateView.as_view(), name='rsvp-list-create'),
    path("rsvp/<int:pk>/",RSVPUpdateView.as_view(),name="rsvp-update"),         
    path("guests/",GuestListCreateView.as_view(),name="guests"),
    path("guests/<int:pk>/",GuestDetailsView.as_view(),name="guest-details-view")
]