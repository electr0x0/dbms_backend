-- users and subtypes
create table hhms_user ( 
    user_id int auto_increment primary key,
    f_name varchar(10) not null,
    l_name varchar(10) not null,
    contact_number varchar(10) not null,
    city varchar(10) not null,
    district varchar(10) not null,
    division varchar(10) not null,
    date_of_birth datetime not null,
    type enum('doctor', 'patient', 'admin', 'manager') not null,
    user_status varchar(4)
);

-- doctor user

create table hhms_user_doctor (
    doc_id int,
    department varchar(15),
    years_of_experience int,
    daily_hours int,
    room_number int,
    primary key (doc_id),
    foreign key (doc_id) references hhms_user(user_id)
);


create table hhms_user_doctor_specialization (
    doc_id int,
    specialization varchar(10),
    primary key (doc_id),
    foreign key (doc_id) references hhms_user(user_id)
);

-- doctor user end

-- patient user start
create table hhms_user_patient (
    pat_id int,
    foreign key (pat_id) references hhms_user(user_id)
);

create table hhms_user_patient_health_record (
    record_id int auto_increment primary key,
    blood_type varchar(3),
    bmi float,
    height float,
    weight float,
    blood_pressure varchar(7),
    heart_rate int,
    cholesterol_level float,
    sugar_level float,
    patient_user_id int,
    record_date datetime,
    foreign key (patient_user_id) references hhms_user(user_id)
);



-- patient-doctor review, appointment record

create table hhms_user_patient_doctor_review_record (
    doctor_id int,
    patient_id int,
    rating int,
    review varchar(255),
    primary key(doctor_id),
    foreign key (doctor_id) references hhms_user(user_id),
    foreign key (patient_id) references hhms_user(user_id)
);

create table hhms_user_patient_doctor_appointment (
    doctor_id int,
    patient_id int,
    ap_date int,
    ap_start_time varchar(255),
    ap_end_time varchar(255),
    ap_type enum('online','offline'),
    primary key(doctor_id,patient_id,ap_date,ap_start_time),
    foreign key (doctor_id) references hhms_user(user_id),
    foreign key (patient_id) references hhms_user(user_id)
);


-- end of patient-doctor review, appointment record

-- patient user end

-- end of users and subtypes


-- diet related tables
create table diet (
    diet_id int auto_increment primary key,
    calorie_intake int,
    description varchar(100),
    diet_type varchar(10)
);

create table exercise (
    exercise_id int auto_increment primary key,
    name varchar(25),
    sets varchar(100),
    rep varchar(10)
);

create table diet_exercise_record (
    exercise_frequency int,
    de_diet_id int,
    de_exercise_id int,
    primary key (de_diet_id, de_exercise_id, exercise_frequency),
    foreign key (de_diet_id) references diet(diet_id),
    foreign key (de_exercise_id) references exercise(exercise_id)
);

-- end of diet related tables




-- create facility supertype
create table facility (
    facility_id int auto_increment primary key,
    f_type varchar(7),
    f_website varchar(100),
    f_address varchar(100)
);

create table facility_contact_number (
    facility_id int,
    contact_number varchar(15),
    primary key (facility_id, contact_number),
    foreign key (facility_id) references facility(facility_id)
);
-- end

-- hospital info
create table facility_hospital (
    h_facility_id int,
    total_bed int,
    number_of_icu int,
    number_of_abulance int,
    manager_id int,
    primary key (h_facility_id),
    foreign key (h_facility_id) references facility(facility_id),
    foreign key (manager_id) references hhms_user(user_id)
);

create table facility_hospital_doctor (
    h_facility_id int,
    h_doctor_id int,
    primary key(h_facility_id,h_doctor_id),
    starttime datetime,
    endtime datetime,
    dutyhours float,
    foreign key (h_facility_id) references facility(facility_id),
    foreign key (h_doctor_id) references hhms_user(user_id)
);


create table service (
    service_id int auto_increment primary key,
    servicename varchar(50),
    description varchar(255),
    availability varchar(50)
);

create table facility_hospital_service(
    service_id int,
    h_facility_id int,
    cost int,
    servicehours int,
    capacity int,
    primary key(h_facility_id, service_id, servicehours),
    foreign key (h_facility_id) references facility(facility_id)
);



create table facility_hospital_service_ambulance (
    ambulance_service_id int,
    primary key(ambulance_service_id),
    drivername varchar(50),
    drivercontact varchar(15),
    vehicletype varchar(20), 
    isavailable boolean,
    foreign key (ambulance_service_id) references service(service_id)
);


create table facility_hospital_service_icu (
    icu_service_id int,
    primary key(icu_service_id),
    wardnumber varchar(5),
    capacity int,
    doctorhours int,
    foreign key (icu_service_id) references service(service_id)
);

create table facility_hospital_service_bed_service (
    bed_service_id int,
    room_number varchar(5),
    bedtype varchar(20),
    lastoccupieddate datetime,
    primary key (bed_service_id),
    foreign key (bed_service_id) references service(service_id)
);


create table facility_diagnostic_center (
    diag_facility_id int,
    license_number varchar(20),
    primary key(diag_facility_id),
    foreign key (diag_facility_id) references facility(facility_id)
);

create table test(
    test_id int auto_increment primary key,
    testname varchar(20),
    testdate datetime,
    testdescription varchar(255)
);

create table facility_diagnostic_center_test(
    diag_facility_id int,
    test_id int,
    cost int,
    equipmentused varchar(20),
    primary key(diag_facility_id, test_id, equipmentused),
    foreign key (diag_facility_id) references facility(facility_id),
    foreign key (test_id) references test(test_id)
);

create table facility_pharmacy (
    facility_pharmacy_id int,
    license_number varchar(20),
    primary key(facility_pharmacy_id),
    foreign key (facility_pharmacy_id) references facility(facility_id)
);


-- end of facility



-- medcine related tables

create table medicine (
    medicine_id int auto_increment primary key,
    name varchar(50),
    manufacturer varchar(50),
    expiry_date datetime,
    manufacture_date datetime,
    prescription_id int
);

create table medicine_inventory (
    inventory_medicine_id int ,
    inventory_pharmacy_facility_id int,
    quantity int,
    cost_per_unit float,
    batch_no varchar(15),
    primary key(inventory_medicine_id, inventory_pharmacy_facility_id),
    foreign key (inventory_medicine_id) references medicine(medicine_id),
    foreign key (inventory_pharmacy_facility_id) references facility(facility_id)
);

-- end of medcine related tables


create table prescription (
    doctor_user_id int,
    patient_user_id int,
    diet_id int,
    prescriptiondate datetime,
    prescriptiondescription varchar(255),
    prescription_id int auto_increment primary key,
    foreign key (doctor_user_id) references hhms_user(user_id),
    foreign key (patient_user_id) references hhms_user(user_id),
    foreign key (diet_id) references diet(diet_id)
);



create table prescription_medicine_record(
  medicine_record_prescription_id int,
  quantity float,
  frequency int,
  medicine_record_medicine_id int,
  dosage int,
  intake_days datetime,
  primary key (medicine_record_medicine_id, medicine_record_prescription_id, quantity),
  foreign key (medicine_record_prescription_id) references prescription(prescription_id),
  foreign key (medicine_record_medicine_id) references medicine(medicine_id)
);



create table prescription_test_record(
  prescription_record_test_id int,
  prescription_record_presription_id int,
  test_date datetime,
  result varchar(255),
  primary key (prescription_record_test_id, prescription_record_presription_id,test_date),
  foreign key (prescription_record_test_id) references test(test_id),
  foreign key (prescription_record_presription_id) references prescription(prescription_id)
);


-- patient recommendation system

create table hhms_user_patient_doctor_recommendation (
    recommended_doc_id int,
    description varchar(255),
    reason_for_recommendation varchar(255),
    recommendationdate datetime,
    primary key(recommended_doc_id, reason_for_recommendation),
    foreign key (recommended_doc_id) references hhms_user_doctor(doc_id)
);

create table hhms_user_patient_medicine_recommendation (
    recommended_medicine_id int,
    remark varchar(255),
    reason_for_recommendation varchar(255),
    recommendationdate datetime,
    frequency int,
    dosage int,
    primary key (recommended_medicine_id, reason_for_recommendation),
    foreign key (recommended_medicine_id) references medicine(medicine_id)
);


create table hhms_user_patient_diet_recommendation (
    recommended_diet_id int,
    description varchar(255),
    reason_for_recommendation varchar(255),
    recommendationdate datetime,
    primary key (recommended_diet_id, reason_for_recommendation, recommendationdate),
    foreign key (recommended_diet_id) references diet(diet_id)
);


create table hhms_user_patient_facility_recommendation (
    recommended_facility_id int,
    description varchar(255),
    reason_for_recommendation varchar(255),
    recommendationdate datetime,
    primary key(recommended_facility_id, reason_for_recommendation),
    foreign key (recommended_facility_id) references facility(facility_id)
);

-- patient recommendation system end