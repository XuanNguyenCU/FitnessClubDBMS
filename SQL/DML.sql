/* The purpose of this file is to have some values already present for testing purposes */

-- Insert statements for Users
INSERT INTO "Users" ("username", "password", "email", "user_type") VALUES 
('yuji69', 'pass', 'yuji.itadori@gmail.com', 'member'),
('ash', 'pokemon', 'ash.ketchum@gmail.com', 'member'),
('jojo', 'bizarre', 'jojo@gmail.com', 'member'),
('gojo', 'purple', 'satoru@hotmail.com', 'trainer'),
('brock', 'rock', 'brock@gmail.com', 'trainer'),
('admin', '12345', 'admin@gmail.com', 'admin');

-- Insert statements for Members
INSERT INTO "Members" ("user_id") VALUES 
(1),
(2),
(3);

-- Insert statements for MemberDetails
INSERT INTO "MemberDetails" ("member_id", "first_name", "last_name", "fitness_goals", "exercise_routine", "fitness_achievements", "billing_info", "loyalty_points") VALUES 
(1, 'Itadori', 'Yuji', 'Bench 300 lbs',  'strength training', 'Maxed out all machines', 'All fees paid', 100),
(2, 'Ash', 'Ketchum', 'Run a full marathon', 'Cardio 1 hour', 'Ran 69km', 'Owes $50 from group session', 10),
(3, 'Joseph', 'Joestar', 'Lose 10 pounds', 'Squats and kicks', 'High jump of 10 metres', 'All fees paid', 69);

-- HealthMetrics, weight in kg, height in inches
INSERT INTO "HealthMetrics" ("member_id", "blood_pressure", "weight", "height") VALUES
(1, '120/80', 60, 70),
(2, 'Normal', 50, 75),
(3, '130/85', 100, 80);

-- Insert statements for Trainers
INSERT INTO "Trainers" ("user_id") VALUES 
(4),
(5);

-- Insert statements for TrainerDetails
INSERT INTO "TrainerDetails" ("trainer_id", "first_name", "last_name", "training_schedule", "progress_notes") VALUES 
(1, 'Satoru', 'Gojo', 'Wednesday Spin Class, weightlifting on Tuesday private', 'Ash is showing progress'),
(2, 'Brock', 'The Rock', 'Friday Pilates class, Thursday Yoga workshop', 'Class did terrible last week');

-- Insert statements for Rooms
INSERT INTO "Rooms" ("name", "equipment_status") VALUES 
('Suite', 'All equipment are safe.'),
('Gym', 'Three dumbbells missing'),
('Swimming Pool', 'Broken diving board');

-- Insert statements for GroupEvents
INSERT INTO "GroupEvents" ("event_name", "event_date", "event_time", "event_description", "trainer_id", "room_id") VALUES 
('Boxing Class', '2024-05-20', '12:00:00', 'Battle with Trainer GoJo', 1, 2);

-- Insert statements for Session and SessionDetails
INSERT INTO "Session" ("member_id", "trainer_id", "room_id") VALUES 
(1, 2, 3),
(2, 1, 1);

INSERT INTO "SessionDetails" ("session_id", "session_date", "session_time", "session_status") VALUES 
(1, '2024-04-22', '14:30:00', 'Scheduled'),
(2, '2024-05-01', '10:10:00', 'Cancelled');