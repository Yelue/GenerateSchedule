CREATE TABLE faculty (
    faculty_id INTEGER PRIMARY KEY,
    faculty_short_name VARCHAR(20) NOT NULL,
    faculty_long_name VARCHAR(100) NOT NULL
);

CREATE TABLE department (
    department_id INTEGER PRIMARY KEY,
    department_short_name VARCHAR(20) NOT NULL,
    department_long_name VARCHAR(100) NOT NULL,
    faculty_id INTEGER NOT NULL REFERENCES faculty (faculty_id)
);

CREATE TABLE groups (
    group_id INTEGER PRIMARY KEY,
    group_name VARCHAR(10) NOT NULL,
    group_course INTEGER NOT NULL,
    department_id INTEGER NOT NULL REFERENCES department (department_id)
);

CREATE TABLE teacher (
    teacher_id INTEGER PRIMARY KEY,
    teacher_short_name VARCHAR(100) NOT NULL,
    teacher_long_name VARCHAR(100) NOT NULL,
    teacher_degree VARCHAR(100) NOT NULL
);

CREATE TABLE lesson (
    lesson_id INTEGER PRIMARY KEY,
    lesson_short_name VARCHAR(100) NOT NULL,
    lesson_long_name VARCHAR(100) NOT NULL,
    lesson_type VARCHAR(30) NOT NULL
);

CREATE TABLE room (
    room_id INTEGER PRIMARY KEY ,
    room_number INTEGER NOT NULL,
    room_type VARCHAR(100) NOT NULL
);

CREATE TABLE class (
    class_id INTEGER PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES groups (group_id),
    teacher_id INTEGER NOT NULL REFERENCES teacher (teacher_id),
    lesson_id INTEGER NOT NULL REFERENCES lesson (lesson_id),
    room_id INTEGER NOT NULL REFERENCES room (room_id),
    time DATE NOT NULL
);