from django.db import models
from django.conf import settings

# Create your models here.

class Contacts(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    contact_info=models.CharField(max_length=255)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    class Meta:
        unique_together=('name','user')

    def __str__(self) :
        return f'{self.user}:{self.name}'

class Groups(models.Model):
    group_name=models.CharField(max_length=255)
    people=models.ManyToManyField(Contacts)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='event_groups')

    def __str__(self):
        return f'{self.user}:{self.group_name}'

    class Meta:
        unique_together=('group_name','user')

class Organizer(models.Model):
    organizer_name=models.CharField(max_length=255)
    contact_info=models.CharField(max_length=255,blank=True)
    email=models.EmailField(unique=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    class Meta:
        unique_together=('organizer_name','user')

    def __str__(self):
        return f'{self.user}:{self.organizer_name}'

class Venue(models.Model):
    venue_name=models.CharField(max_length=255)
    venue_location=models.CharField(max_length=255)
    capacity=models.IntegerField()
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}:{self.venue_name}'
    class Meta:
        unique_together=('venue_name','user')
        
class Guest(models.Model):
    guest_name=models.CharField(max_length=255)
    email=models.EmailField()
    phone=models.CharField(max_length=255)
    invited_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str___(self):
        return f'{self.invited_by}-{self.guest_name}'

class Event(models.Model):
    event_name=models.CharField(max_length=255)
    event_descritption=models.TextField(blank=True)
    date=models.DateField()
    time=models.TimeField()
    organizer=models.ForeignKey(Organizer,on_delete=models.SET_NULL,null=True)
    venue=models.ForeignKey(Venue,on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    budget=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    contacts_invited=models.ManyToManyField(Contacts,blank=True)
    groups_invited=models.ManyToManyField(Groups,blank=True)
    guests_invited=models.ManyToManyField(Guest,blank=True)
    
    def __str__(self):
        return f'{self.user}:{self.event_name}'
    
    def total_expenses(self):
        return sum(expense.amount for expense in self.expsenses_set.all())
    
    def remaining_budget(self):
        return self.budget-self.total_expenses()
    
    class Meta:
        unique_together=('event_name','user')

class Expenses(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name="expenses")
    description=models.CharField(max_length=200)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.event}-Expense{self.pk}"



class RSVP(models.Model):
    status_choices={
        "attending":"Attending",
        "pending":"Pending",
        "not attending":"Not Attending"
    }
    guest=models.ForeignKey(Guest,on_delete=models.CASCADE)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    status=models.CharField(choices=status_choices,max_length=255)
    dietary_preferences=models.TextField(blank=True,null=True)

class Vendor(models.Model):
    name=models.CharField(max_length=100)
    address=models.TextField()
    contact_info=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    def __str__(self):
        return self.name





