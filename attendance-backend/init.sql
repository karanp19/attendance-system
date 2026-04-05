-- Attendance System Database Initialization
-- Create tables and sample data

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    image_hash VARCHAR(255) NOT NULL,
    enrolled_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Attendance table
CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    teacher_id INTEGER NOT NULL REFERENCES users(id),
    date TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL,
    confidence FLOAT,
    camera_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample users (teacher/admin)
INSERT INTO users (username, email, password_hash, is_active) VALUES
('admin', 'admin@attendance.com', '$2b$10$dummy_hash_for_demo', TRUE),
('teacher1', 'teacher1@attendance.com', '$2b$10$dummy_hash_for_demo', TRUE);

-- Insert sample students with placeholder hashes
INSERT INTO students (username, email, password_hash, image_hash) VALUES
('student1', 'student1@attendance.com', '$2b$10$dummy_hash_for_demo', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
('student2', 'student2@attendance.com', '$2b$10$dummy_hash_for_demo', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),
('student3', 'student3@attendance.com', '$2b$10$dummy_hash_for_demo', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855');

-- Create indexes
CREATE INDEX idx_attendance_student_id ON attendance(student_id);
CREATE INDEX idx_attendance_teacher_id ON attendance(teacher_id);
CREATE INDEX idx_attendance_date ON attendance(date);
CREATE INDEX idx_attendance_status ON attendance(status);

-- Grant access
GRANT ALL PRIVILEGES ON users TO attendance;
GRANT ALL PRIVILEGES ON students TO attendance;
GRANT ALL PRIVILEGES ON attendance TO attendance;
