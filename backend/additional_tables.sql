-- ADOPTION PROCESS STEPS TABLE
CREATE TABLE adoption_steps (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  step_number int NOT NULL,
  title varchar NOT NULL,
  description text NOT NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- SHELTER INFORMATION TABLE
CREATE TABLE shelter_info (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  name varchar NOT NULL,
  description text,
  address text NOT NULL,
  hours text NOT NULL,
  contact varchar NOT NULL,
  map_url text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Insert adoption steps data
INSERT INTO adoption_steps (step_number, title, description)
VALUES 
  (1, 'Browse Available Pets', 'View our gallery of pets looking for their forever homes.'),
  (2, 'Submit Application', 'Fill out our adoption application form online.'),
  (3, 'Meet & Greet', 'Schedule a visit to meet your potential new pet.'),
  (4, 'Home Check', 'We ensure your home is a safe environment for the pet.'),
  (5, 'Finalize Adoption', 'Complete paperwork and welcome your new family member!');

-- Insert shelter info
INSERT INTO shelter_info (name, description, address, hours, contact, map_url)
VALUES (
  'Angeles Pet Care',
  'Visit our shelter to meet our lovely pets in person!',
  'Angeles City, Pampanga, Philippines',
  'Monday - Sunday, 9:00 AM - 6:00 PM',
  '(123) 456-7890',
  'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3856.9007861381824!2d120.27661631367312!3d14.830825354692275!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3396711bd51280cb%3A0x9807796767f2153d!2sAngeles%20Pet%20Care!5e0!3m2!1sen!2sph!4v1747207650130!5m2!1sen!2sph'
);

-- Drop existing pets table if it exists
DROP TABLE IF EXISTS pets CASCADE;

-- Create pets table with all required fields
CREATE TABLE pets (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  name varchar NOT NULL,
  species varchar NOT NULL,
  breed varchar NOT NULL,
  age numeric NOT NULL,
  gender varchar NOT NULL,
  description text,
  photo_url varchar, -- Main photo URL from Supabase storage
  status varchar NOT NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create pet_photos table for additional photos
CREATE TABLE pet_photos (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  pet_id uuid REFERENCES pets(id) ON DELETE CASCADE,
  photo_url varchar NOT NULL,
  is_main boolean DEFAULT false,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Add index for better performance
CREATE INDEX idx_pets_status ON pets(status);

-- Add RLS policies for pets table
ALTER TABLE pets ENABLE ROW LEVEL SECURITY;

-- Allow public read access to pets
CREATE POLICY "Allow public read access to pets"
    ON pets FOR SELECT
    USING (true);

-- Allow authenticated users to insert pets
CREATE POLICY "Allow authenticated users to insert pets"
    ON pets FOR INSERT
    TO authenticated
    WITH CHECK (true);

-- Allow authenticated users to update pets
CREATE POLICY "Allow authenticated users to update pets"
    ON pets FOR UPDATE
    TO authenticated
    USING (true)
    WITH CHECK (true);

-- Allow authenticated users to delete pets
CREATE POLICY "Allow authenticated users to delete pets"
    ON pets FOR DELETE
    TO authenticated
    USING (true);
