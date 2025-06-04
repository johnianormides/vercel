# Pawffect Backend

A Flask-based backend API with Supabase integration for the Pawffect pet adoption application.

## Setup Instructions

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment variables:
   - Copy the `.env` file and fill in your Supabase credentials:
     - `SUPABASE_URL`: Your Supabase project URL
     - `SUPABASE_KEY`: Your Supabase service role key (not the anon key)

3. Create your Supabase database tables:
   - Use the SQL scripts provided below to create the necessary tables in your Supabase SQL editor

4. Run the Flask application:
```bash
python app.py
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login a user

### Users
- `GET /api/users` - Get all users
- `GET /api/users/<user_id>` - Get a specific user
- `PUT /api/users/<user_id>` - Update a user

### Pets
- `GET /api/pets` - Get all pets
- `GET /api/pets/<pet_id>` - Get a specific pet with its photos
- `POST /api/pets` - Create a new pet
- `PUT /api/pets/<pet_id>` - Update a pet
- `DELETE /api/pets/<pet_id>` - Delete a pet

### Applications
- `GET /api/applications` - Get all applications
- `GET /api/applications/<application_id>` - Get a specific application
- `POST /api/applications` - Create a new application
- `PUT /api/applications/<application_id>` - Update an application

### Appointments
- `GET /api/appointments` - Get all appointments
- `GET /api/appointments/<appointment_id>` - Get a specific appointment
- `POST /api/appointments` - Create a new appointment
- `PUT /api/appointments/<appointment_id>` - Update an appointment
- `DELETE /api/appointments/<appointment_id>` - Delete an appointment

### File Uploads
- `POST /api/upload` - Upload a file to Supabase storage

## Database Schema

The database includes the following tables:
- `users` - User accounts and profiles
- `pets` - Pet information
- `pet_photos` - Multiple photos for each pet
- `applications` - Adoption applications
- `appointments` - Appointment scheduling
