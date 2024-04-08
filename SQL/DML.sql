/* The purpose of the populateDB.sql file is to have some values already present for testing purposes */


-- Insert statements for Users
INSERT INTO "Users" ("username", "password", "email", "user_type") VALUES 
('jpen', 'pass', 'JustinePenny@gmail.com', 'member'),
('XPlaneX', 'g0wter', 'planexo@gmail.com', 'member'),
('HowardBerns', 'burnsH0t', 'BernsH@gmail.com', 'member'),
('gojo', 'pass', 'chunder@gmail.com', 'trainer'),
('EmilyCarp10', 'p@ssc0de', 'emCarp@gmail.com', 'trainer'),
('admin', 'adminpass', 'morganChu@gmail.com', 'admin');

-- Insert statements for Members
INSERT INTO "Members" ("user_id") VALUES 
(1),
(2),
(3);

-- Insert statements for MemberDetails
INSERT INTO "MemberDetails" ("member_id", "first_name", "last_name", "fitness_goals", "health_metrics", "exercise_routine", "fitness_achievements", "billing_info", "loyalty_points") VALUES 
(1, 'Justine', 'Penny', 'Run a half-marathon', '', '30 min treadmill', 'Ran 5k', 'All fees paid', 14),
(2, 'Ash', 'Ketchum', 'Bench 150lbs', '', 'Routine2', 'Achievement2', 'Owes $40 from group session', 5),
(3, 'Jojo', 'Joestar', 'Lose 15 pounds', '', 'Routine3', 'Achievement3', 'Billing3', 228);

-- Insert statements for HealthMetrics
INSERT INTO "HealthMetrics" ("member_id", "blood_pressure", "weight", "height") VALUES
(1, '120/80', 150, 67), -- For 5 foot 7 inches, using inches for height measurement
(2, 'Normal', 160, 70), -- For 5 foot 10 inches, using inches
(3, '130/85', 190, 69); -- For 5 foot 9 inches, using inches

-- Insert statements for Trainers
INSERT INTO "Trainers" ("user_id") VALUES 
(4),
(5);

-- Insert statements for TrainerDetails
INSERT INTO "TrainerDetails" ("trainer_id", "training_schedule", "progress_notes") VALUES 
(1, 'Monday spin class, weightlifting on Tuesday private', 'Howard is showing progress'),
(2, 'Wednesday pilates class, Thursday Yoga workshop', 'Class did well with downwards dog last week');

-- Insert statements for Rooms
INSERT INTO "Rooms" ("name", "equipment_status") VALUES 
('Suite 1', 'All equipment good'),
('Suite 2', '15lbs dumbbell missing'),
('Gym', 'Broken butterfly machine');

-- Insert statements for GroupEvents
INSERT INTO "GroupEvents" ("event_name", "event_date", "event_description", "trainer_id", "room_id") VALUES 
('Yoga', 'Tuesday', 'A yoga class with a trainer', 1, 2);

-- Insert statements for Session and SessionDetails
INSERT INTO "Session" ("member_id", "trainer_id", "room_id") VALUES 
(1, 2, 3);

INSERT INTO "SessionDetails" ("session_id", "session_date", "session_time", "session_status") VALUES 
(1, 'Friday', '2pm', 'Scheduled');

INSERT INTO "Session" ("member_id", "trainer_id", "room_id") VALUES 
(1, 1, 1);

INSERT INTO "SessionDetails" ("session_id", "session_date", "session_time", "session_status") VALUES 
(2, 'Saturday', '10am', 'Cancelled');