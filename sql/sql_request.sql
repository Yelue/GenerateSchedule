CREATE TABLE faculty (
    faculty_id SERIAL PRIMARY KEY,
    faculty_short_name VARCHAR(20) NOT NULL,
    faculty_long_name VARCHAR(100) NOT NULL
);

CREATE TABLE department (
    department_id SERIAL PRIMARY KEY,
    department_short_name VARCHAR(20) NOT NULL,
    department_long_name VARCHAR(100) NOT NULL,
    faculty_id SERIAL NOT NULL REFERENCES faculty (faculty_id)
);

CREATE TABLE groups (
    group_id SERIAL PRIMARY KEY,
    group_name VARCHAR(10) NOT NULL,
    group_course INTEGER NOT NULL,
    department_id SERIAL NOT NULL REFERENCES department (department_id)
);

CREATE TABLE teacher (
    teacher_id SERIAL PRIMARY KEY,
    teacher_short_name VARCHAR(100) NOT NULL,
    teacher_long_name VARCHAR(100) NOT NULL,
    teacher_degree VARCHAR(100) NOT NULL
);

CREATE TABLE lesson (
    lesson_id SERIAL PRIMARY KEY,
    lesson_short_name VARCHAR(100) NOT NULL,
    lesson_long_name VARCHAR(100) NOT NULL,
    lesson_type VARCHAR(30) NOT NULL
);

CREATE TABLE room (
    room_id SERIAL PRIMARY KEY,
    room_number INTEGER NOT NULL,
    room_type VARCHAR(100) NOT NULL
);

CREATE TABLE study_days (
    days_id SERIAL PRIMARY KEY ,
    name_day VARCHAR(100) NOT NULL
);

CREATE TABLE pairs (
    pairs_id SERIAL PRIMARY KEY,
    time_table VARCHAR(100) NOT NULL
);

CREATE TABLE card  (
    card_id SERIAL NOT NULL,
    group_id INTEGER PRIMARY KEY REFERENCES groups (group_id),
    teacher_id INTEGER PRIMARY KEY REFERENCES teacher (teacher_id),
    lesson_id INTEGER PRIMARY KEY REFERENCES lesson (lesson_id),
    amount_time INTEGER NOT NULL
);

CREATE TABLE class (
    class_id SERIAL PRIMARY KEY,
    card_id SERIAL NOT NULL REFERENCES card (card_id),
    days_id SERIAL NOT NULL REFERENCES study_days (days_id),
    pairs_id SERIAL NOT NULL REFERENCES pairs (pairs_id)
);

CREATE TABLE verif_student (
	st_email VARCHAR(100) PRIMARY KEY,
	st_secret_key VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE verif_teacher (
	tchr_email VARCHAR(100) PRIMARY KEY,
	tchr_secret_key VARCHAR(100) NOT NULL UNIQUE, 
	teacher_id INTEGER NOT NULL REFERENCES teacher (teacher_id)
);

CREATE TABLE student_wish_schedule (
	st_schedule_id SERIAL PRIMARY KEY,
	st_secret_key VARCHAR(100) NOT NULL REFERENCES verif_student (st_secret_key),
	card_id INTEGER NOT NULL REFERENCES card (card_id),
	days_id INTEGER NOT NULL REFERENCES study_days (days_id),
	pairs_id INTEGER NOT NULL REFERENCES pairs (pairs_id)
);

CREATE TABLE teacher_wish_schedule (
	tchr_schedule_id SERIAL PRIMARY KEY,
	tchr_secret_key VARCHAR(100) NOT NULL REFERENCES verif_teacher (tchr_secret_key),
	card_id INTEGER NOT NULL REFERENCES card (card_id),
	days_id INTEGER NOT NULL REFERENCES study_days (days_id),
	pairs_id INTEGER NOT NULL REFERENCES pairs (pairs_id)
);



