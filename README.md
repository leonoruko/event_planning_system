Event Planning System
A web-based application built with Django that allows users to create, manage, and track events, invite guests, and handle RSVP status. The system integrates email notifications for guest invitations, event cancellations, reminders, and group-based invitations.

Table of Contents
Project Overview
Features
Installation
Usage
API Endpoints
Running Tests
Postman Collection
Contributing
License
Project Overview
This project serves as an event planning platform that helps users manage and invite guests or groups to events. The system sends notifications such as invitations, cancellations, and reminders to users through email.

Features
Create, update, and delete events.
Invite individual contacts or groups of contacts.
RSVP tracking for guests.
Send email notifications for event invitations, reminders, and cancellations.
Manage guest lists and group invitations.
Secure with authentication (JWT).
Installation
Prerequisites
Ensure you have the following installed:

Python 3.x
Django 4.x
PostgreSQL (or any other supported database)
Postman (for API testing)
Steps
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/event_planning_system.git
cd event_planning_system
Create a virtual environment and activate it:

bash
Copy code
python3 -m venv venv
source venv/bin/activate   # for Linux/macOS
venv\Scripts\activate      # for Windows
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the environment variables in a .env file:

bash
Copy code
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
DEFAULT_FROM_EMAIL=your_email
EMAIL_HOST=your_smtp_server
EMAIL_HOST_USER=your_email_user
EMAIL_HOST_PASSWORD=your_email_password
EMAIL_PORT=587
EMAIL_USE_TLS=True
Apply the migrations:

bash
Copy code
python manage.py migrate
Create a superuser:

bash
Copy code
python manage.py createsuperuser
Run the development server:

bash
Copy code
python manage.py runserver
Open your browser and visit http://127.0.0.1:8000/admin to log in as the superuser.

Usage
Create an Event: Use the admin panel or APIs to create an event.
Invite Guests: Add individual contacts or groups and send event invitations.
Check RSVPs: Track RSVP status for invited guests.
Cancel Events: Cancel events and notify the guests via email.
API Endpoints
Authentication
Login: POST /api/login/
Register: POST /api/register/
Event Management
Create Event: POST /api/events/
Get Event Details: GET /api/events/{id}/
Update Event: PUT /api/events/{id}/
Delete Event: DELETE /api/events/{id}/
RSVP and Guests
RSVP for Event: POST /api/events/{id}/rsvp/
Get RSVPs: GET /api/events/{id}/rsvps/
Invite Guests: POST /api/events/{id}/invite/
Notifications
Send Invitations: Automatically triggered after event creation.
Send Cancellations: Triggered by event cancellation.
Send Reminders: Automatically sent hours before the event.
Running Tests
To run tests, use:

bash
Copy code
python manage.py test
Postman Collection
To test the API, you can import the Postman collection:

Import Steps:
Open Postman.
Click on Import at the top left.
Select File and upload the event_planning_system.postman_collection.json file located in the project directory.
Once imported, you can use the pre-configured requests for various API endpoints.
Testing with Postman
The Postman collection includes tests for:

Event creation and management.
Guest invitations and RSVP responses.
Email notification checks.
Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request. Please ensure your changes are well-tested.

License
This project is licensed under the MIT License. See the LICENSE file for more details.
