/* The purpose of this file is to have some values already present for testing purposes */

-- Insert statements for Users
INSERT INTO "Users" ("username", "password", "email", "user_type") VALUES 
('JenniferLawrenceLover', 'black flash', 'yuji.itadori@gmail.com', 'member'),
('ash', 'pokemon', 'ash.ketchum@gmail.com', 'member'),
('jojo', 'bizarre', 'jojo@gmail.com', 'member'),
('Gojo Sensei', 'purple', 'satoru@hotmail.com', 'trainer'),
('brock', 'rock', 'brock@gmail.com', 'trainer'),
('admin', 'pass420', 'admin@gmail.com', 'admin');

-- Insert statements for MemberDetails
INSERT INTO "Members" ("user_id", "first_name", "last_name", "fitness_goals", "exercise_routine", "fitness_achievements", "billing_info", "loyalty_points") VALUES 
(1, 'Itadori', 'Yuji', 'Bench 300 lbs',  'strength training', 'Maxed out all machines', 0.00, 100),
(2, 'Ash', 'Ketchum', 'Run a full marathon', 'Cardio 1 hour', 'Ran 69km', 20.99, 10),
(3, 'Joseph', 'Joestar', 'Lose 10 pounds', 'Squats and kicks', 'High jump of 10 metres', 10.05, 69);

-- HealthMetrics, weight in kg, height in inches
INSERT INTO "HealthMetrics" ("member_id", "blood_pressure", "weight", "height") VALUES
(1, '120/80', 60, 180.7),
(2, 'Normal', 50.0, 90),
(3, '130/85', 100, 150);

-- Insert statements for TrainerDetails
INSERT INTO "Trainers" ("user_id", "first_name", "last_name") VALUES 
(4, 'Satoru', 'Gojo'),
(5, 'Brock', 'The Rock');

-- Insert statements for Dates
INSERT INTO "Dates" ("availability", "trainer_id") VALUES 
('2024-05-11 12:00:00', 1),
('2024-11-07 12:00:00', 1),
('2024-12-26 09:00:00', 2);

-- Insert statements for Rooms
INSERT INTO "Rooms" ("room_type", "equipment_status") VALUES 
('Suite', 'All equipment are available and safe.'),
('Gym', '3 dumbbells are missing'),
('Swimming Pool', 'Broken diving board');

-- Inserting into Sessions table
INSERT INTO "Sessions" ("member_id", "trainer_id", "room_id", "session_date", "session_details")
VALUES 
(1, 2, 3, '2024-04-30 14:00', 'Strength Training'),
(2, 1, 1, '2024-05-01 10:00', 'Pokemon Training');

-- Insert statements for GroupEvents
INSERT INTO "GroupEvents" ("event_name", "event_date", "event_description", "trainer_id", "room_id") VALUES 
('Boxing Class', '2024-05-20 12:30:00', 'Battle with Trainer GoJo', 1, 2);
