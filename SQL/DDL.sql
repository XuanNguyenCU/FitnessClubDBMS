-- Clean up
DROP TABLE IF EXISTS "Users" CASCADE;
DROP TABLE IF EXISTS "Admins" CASCADE;
DROP TABLE IF EXISTS "Trainers" CASCADE;
DROP TABLE IF EXISTS "TrainerDetails" CASCADE;
DROP TABLE IF EXISTS "Members" CASCADE;
DROP TABLE IF EXISTS "HealthMetrics" CASCADE;
DROP TABLE IF EXISTS "MemberDetails" CASCADE;
DROP TABLE IF EXISTS "Rooms" CASCADE;
DROP TABLE IF EXISTS "Session" CASCADE;
DROP TABLE IF EXISTS "SessionDetails" CASCADE;
DROP TABLE IF EXISTS "MemberGroupEvent" CASCADE;
DROP TABLE IF EXISTS "GroupEvents" CASCADE;

-- Users table creation
CREATE TABLE "Users" (
  "user_id" SERIAL PRIMARY KEY,
  "username" TEXT NOT NULL UNIQUE,
  "password" TEXT NOT NULL,
  "email" TEXT NOT NULL UNIQUE,
  "user_type" TEXT NOT NULL
);

-- Members table creation
CREATE TABLE "Members" (
  "user_id" INTEGER,
  "member_id" SERIAL PRIMARY KEY,
  FOREIGN KEY ("user_id") REFERENCES "Users"("user_id")
);

-- MemberDetails table creation
CREATE TABLE "MemberDetails" (
  "member_id" INTEGER,
  "first_name" TEXT,
  "last_name" TEXT,
  "fitness_goals" TEXT,
  "health_metrics" TEXT,
  "exercise_routine" TEXT,
  "fitness_achievements" TEXT,
  "billing_info" TEXT,
  "loyalty_points" INTEGER,
  FOREIGN KEY ("member_id") REFERENCES "Members"("member_id")
);

-- HealthMetrics table creation
CREATE TABLE "HealthMetrics" (
  "metric_id" SERIAL PRIMARY KEY,
  "member_id" INTEGER,
  "blood_pressure" TEXT,
  "weight" NUMERIC,
  "height" NUMERIC,
  FOREIGN KEY ("member_id") REFERENCES "Members"("member_id")
);

-- Trainers table creation
CREATE TABLE "Trainers" (
  "user_id" INTEGER,
  "trainer_id" SERIAL PRIMARY KEY,
  FOREIGN KEY ("user_id") REFERENCES "Users"("user_id")
);

-- TrainerDetails table creation
CREATE TABLE "TrainerDetails" (
  "trainer_id" INTEGER,
  "training_schedule" TEXT,
  "progress_notes" TEXT,
  FOREIGN KEY ("trainer_id") REFERENCES "Trainers"("trainer_id")
);

-- Admins table creation
CREATE TABLE "Admins" (
  "user_id" INTEGER,
  "admin_id" SERIAL PRIMARY KEY,
  FOREIGN KEY ("user_id") REFERENCES "Users"("user_id")
);

-- Rooms table creation
CREATE TABLE "Rooms" (
  "room_id" SERIAL PRIMARY KEY,
  "name" TEXT,
  "equipment_status" TEXT
);

-- Session table creation
CREATE TABLE "Session" (
  "session_id" SERIAL PRIMARY KEY,
  "member_id" INTEGER,
  "trainer_id" INTEGER,
  "room_id" INTEGER,
  FOREIGN KEY ("member_id") REFERENCES "Members"("member_id"),
  FOREIGN KEY ("trainer_id") REFERENCES "Trainers"("trainer_id"),
  FOREIGN KEY ("room_id") REFERENCES "Rooms"("room_id")
);

-- SessionDetails table creation
CREATE TABLE "SessionDetails" (
  "session_id" INTEGER,
  "session_date" TEXT,
  "session_time" TEXT,
  "session_status" TEXT,
  FOREIGN KEY ("session_id") REFERENCES "Session"("session_id")
);

-- GroupEvents table creation
CREATE TABLE "GroupEvents" (
  "event_id" SERIAL PRIMARY KEY,
  "event_name" TEXT,
  "event_date" TEXT,
  "event_description" TEXT,
  "trainer_id" INTEGER,
  "room_id" INTEGER,
  FOREIGN KEY ("trainer_id") REFERENCES "Trainers"("trainer_id"),
  FOREIGN KEY ("room_id") REFERENCES "Rooms"("room_id")
);

-- MemberGroupEvent table creation
CREATE TABLE "MemberGroupEvent" (
  "member_id" INTEGER,
  "event_id" INTEGER,
  UNIQUE ("member_id", "event_id"),
  FOREIGN KEY ("member_id") REFERENCES "Members"("member_id"),
  FOREIGN KEY ("event_id") REFERENCES "GroupEvents"("event_id")
);
