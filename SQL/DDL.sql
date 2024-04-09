-- Clean up
DROP TABLE IF EXISTS "Users" CASCADE;
DROP TABLE IF EXISTS "Admins" CASCADE;
DROP TABLE IF EXISTS "Trainers" CASCADE;
DROP TABLE IF EXISTS "Members" CASCADE;
DROP TABLE IF EXISTS "HealthMetrics" CASCADE;
DROP TABLE IF EXISTS "Rooms" CASCADE;
DROP TABLE IF EXISTS "Sessions" CASCADE;
DROP TABLE IF EXISTS "MemberGroupEvent" CASCADE;
DROP TABLE IF EXISTS "GroupEvents" CASCADE;

-- Users table creation
CREATE TABLE "Users" (
  "user_id" SERIAL PRIMARY KEY,
  "username" VARCHAR(255) NOT NULL UNIQUE,
  "password" VARCHAR(255) NOT NULL,
  "email" VARCHAR(255) NOT NULL UNIQUE,
  "user_type" VARCHAR(255) NOT NULL
);

-- Members table creation
CREATE TABLE "Members" (
  "user_id" INTEGER,
  "member_id" SERIAL PRIMARY KEY,
  "first_name" VARCHAR(255) NOT NULL,
  "last_name" VARCHAR(255) NOT NULL,
  "fitness_goals" TEXT,
  "exercise_routine" TEXT,
  "fitness_achievements" TEXT,
  "billing_info" TEXT,
  "loyalty_points" INTEGER,
  FOREIGN KEY ("user_id") REFERENCES "Users"("user_id")
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
  "first_name" VARCHAR(255) NOT NULL,
  "last_name" VARCHAR(255) NOT NULL,
  "training_schedule" TEXT,
  "progress_notes" TEXT,
  FOREIGN KEY ("user_id") REFERENCES "Users"("user_id")
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
  "name" TEXT NOT NULL,
  "equipment_status" TEXT
);

-- Sessions (with Trainers) table creation
CREATE TABLE "Sessions" (
  "session_id" SERIAL PRIMARY KEY,
  "member_id" INTEGER,
  "trainer_id" INTEGER,
  "room_id" INTEGER,
  "session_date" DATE,
  "session_time" TIME (0) NOT NULL,
  "session_status" TEXT,
  FOREIGN KEY ("member_id") REFERENCES "Members"("member_id"),
  FOREIGN KEY ("trainer_id") REFERENCES "Trainers"("trainer_id"),
  FOREIGN KEY ("room_id") REFERENCES "Rooms"("room_id")
);

-- GroupEvents table creation
CREATE TABLE "GroupEvents" (
  "event_id" SERIAL PRIMARY KEY,
  "event_name" TEXT,
  "event_date" DATE,
  "event_time" TIME (0) NOT NULL,
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
