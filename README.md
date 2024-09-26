# Event Planning System

A web-based application built with Django that allows users to create, manage, and track events, invite guests, and handle RSVP status. The system integrates email notifications for guest invitations, event cancellations, reminders, and group-based invitations.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [API Endpoints](#api-endpoints)
6. [Running Tests](#running-tests)
7. [Postman Collection](#postman-collection)
8. [Contributing](#contributing)
9. [License](#license)

## Project Overview
This project serves as an event planning platform that helps users manage and invite guests or groups to events. The system sends notifications such as invitations, cancellations, and reminders to users through email.

## Features
- Create, update, and delete events.
- Invite individual contacts or groups of contacts.
- RSVP tracking for guests.
- Send email notifications for event invitations, reminders, and cancellations.
- Manage guest lists and group invitations.
- Secure with authentication (JWT).
  
## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Django 4.x
- PostgreSQL (or any other supported database)
- Postman (for API testing)

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/event_planning_system.git
    cd event_planning_system
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # for Linux/macOS
    venv\Scripts\activate      # for Windows
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the environment variables in a `.env` file:
    ```bash
    SECRET_KEY=your_secret_key
    DEBUG=True
    DATABASE_URL=your_database_url
    DEFAULT_FROM_EMAIL=your_email
    EMAIL_HOST=your_smtp_server
    EMAIL_HOST_USER=your_email_user
    EMAIL_HOST_PASSWORD=your_email_password
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    ```

5. Apply the migrations:
    ```bash
    python manage.py migrate
    ```

6. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

7. Run the development server:
    ```bash
    python manage.py runserver
    ```

8. Open your browser and visit `http://127.0.0.1:8000/admin` to log in as the superuser.

## Usage
1. **Create an Event**: 
   Use the admin panel or APIs to create an event.
2. **Invite Guests**: 
   Add individual contacts or groups and send event invitations.
3. **Check RSVPs**: 
   Track RSVP status for invited guests.
4. **Cancel Events**: 
   Cancel events and notify the guests via email.

## API Endpoints

### Authentication
- **Login**: `POST /api/login/`
- **Register**: `POST /api/register/`

### Event Management
- **Create Event**: `POST /api/events/`
- **Get Event Details**: `GET /api/events/{id}/`
- **Update Event**: `PUT /api/events/{id}/`
- **Delete Event**: `DELETE /api/events/{id}/`

### RSVP and Guests
- **RSVP for Event**: `POST /api/events/{id}/rsvp/`
- **Get RSVPs**: `GET /api/events/{id}/rsvps/`
- **Invite Guests**: `POST /api/events/{id}/invite/`

### Notifications
- **Send Invitations**: Automatically triggered after event creation.
- **Send Cancellations**: Triggered by event cancellation.
- **Send Reminders**: Automatically sent hours before the event.

## Running Tests
To run tests, use:
```bash
python manage.py test
