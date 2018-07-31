DROP TABLE if exists user;
DROP TABLE if exists student;
DROP TABLE if exists class;
DROP TABLE if exists test;

CREATE TABLE user (
    id int(16) AUTO_INCREMENT NOT NULL,
    name varchar(64) NOT NULL,
    email varchar(64),
    password varchar(16) NOT NULL,
    primary key(id)
);

CREATE TABLE student (
    id int(16) AUTO_INCREMENT NOT NULL,
    student_name varchar(64) NOT NULL,
    gender varchar(10),
    id_card_num int(30) NOT NULL,
    phone_num int(20),
    job_title varchar(64),
    enter_time int(20),
    class_id int(10),
    class_name varchar(64),
    theoty_result int(3),
    practise_result int(3),
    primary key(id)
);

CREATE TABLE class (
    id int(16) AUTO_INCREMENT NOT NULL,
    class_name varchar(64) NOT NULL,
    begin_time int(20),
    end_time int(20),
    begin_address varchar(128),
    create_time int(20),
    primary key(id)
);

CREATE TABLE test (
    id int(16) AUTO_INCREMENT NOT NULL,
    test_name varchar(64) NOT NULL,
    test_type varchar(20),
    test_work_type varchar(20),
    target_name varchar(128),
    target_id varchar(128),
    duration int(5),
    start_time int(20),
    end_time int(20),
    test_times int(3),
    test_status varchar(10),
    primary key(id)
);