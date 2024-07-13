import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
from datetime import datetime

fake = Faker()

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query, data):
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def seed_data(connection):
    # Insert data into hhms_user
    user_types = ['doctor', 'patient', 'admin', 'manager']
    for _ in range(20):
        f_name = fake.first_name()
        l_name = fake.last_name()
        contact_number = fake.phone_number()[:10]
        city = fake.city()[:10]
        district = fake.city_suffix()[:10]
        division = fake.state()[:10]
        date_of_birth = fake.date_of_birth(minimum_age=20, maximum_age=80).strftime('%Y-%m-%d')
        type = random.choice(user_types)
        user_status = 'active'
        execute_query(connection, 
                      "INSERT INTO hhms_user (f_name, l_name, contact_number, city, district, division, date_of_birth, type, user_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                      (f_name, l_name, contact_number, city, district, division, date_of_birth, type, user_status))

    # Insert data into hhms_user_doctor
    for user_id in range(1, 21):
        if fake.random_element(elements=user_types) == 'doctor':
            department = fake.word()[:15]
            years_of_experience = fake.random_int(min=1, max=30)
            daily_hours = fake.random_int(min=1, max=12)
            room_number = fake.random_int(min=100, max=500)
            execute_query(connection, 
                          "INSERT INTO hhms_user_doctor (doc_id, department, years_of_experience, daily_hours, room_number) VALUES (%s, %s, %s, %s, %s)", 
                          (user_id, department, years_of_experience, daily_hours, room_number))
                          
    # Insert data into hhms_user_doctor_specialization
    for user_id in range(1, 21):
        if fake.random_element(elements=user_types) == 'doctor':
            specialization = fake.word()[:10]
            execute_query(connection, 
                          "INSERT INTO hhms_user_doctor_specialization (doc_id, specialization) VALUES (%s, %s)", 
                          (user_id, specialization))

    # Insert data into hhms_user_patient
    for user_id in range(1, 21):
        if fake.random_element(elements=user_types) == 'patient':
            execute_query(connection, 
                          "INSERT INTO hhms_user_patient (pat_id) VALUES (%s)", 
                          (user_id,))

    # Insert data into hhms_user_patient_health_record
    for _ in range(20):
        blood_type = fake.random_element(elements=('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'))
        bmi = round(random.uniform(18.5, 30.0), 2)
        height = round(random.uniform(150.0, 200.0), 2)
        weight = round(random.uniform(50.0, 100.0), 2)
        blood_pressure = f"{random.randint(90, 140)}/{random.randint(60, 90)}"
        heart_rate = random.randint(60, 100)
        cholesterol_level = round(random.uniform(150.0, 240.0), 2)
        sugar_level = round(random.uniform(70.0, 180.0), 2)
        patient_user_id = random.randint(1, 20)
        record_date = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        execute_query(connection, 
                      "INSERT INTO hhms_user_patient_health_record (blood_type, bmi, height, weight, blood_pressure, heart_rate, cholesterol_level, sugar_level, patient_user_id, record_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                      (blood_type, bmi, height, weight, blood_pressure, heart_rate, cholesterol_level, sugar_level, patient_user_id, record_date))

    # Insert data into diet
    for _ in range(10):
        calorie_intake = fake.random_int(min=1500, max=3000)
        description = fake.text(max_nb_chars=100)
        diet_type = fake.word()[:10]
        execute_query(connection, 
                      "INSERT INTO diet (calorie_intake, description, diet_type) VALUES (%s, %s, %s)", 
                      (calorie_intake, description, diet_type))

    # Insert data into exercise
    for _ in range(10):
        name = fake.word()[:10]
        sets = f"{random.randint(1, 5)} sets"
        rep = f"{random.randint(5, 20)} reps"
        execute_query(connection, 
                      "INSERT INTO exercise (name, sets, rep) VALUES (%s, %s, %s)", 
                      (name, sets, rep))

    # Insert data into diet_exercise_record
    for _ in range(10):
        exercise_frequency = random.randint(1, 7)
        de_diet_id = random.randint(1, 10)
        de_exercise_id = random.randint(1, 10)
        execute_query(connection, 
                      "INSERT INTO diet_exercise_record (exercise_frequency, de_diet_id, de_exercise_id) VALUES (%s, %s, %s)", 
                      (exercise_frequency, de_diet_id, de_exercise_id))

    # Insert data into facility
    facility_types = ['hospital', 'diagnostic', 'pharmacy']
    for _ in range(10):
        f_type = random.choice(facility_types)
        f_website = fake.url()
        f_address = fake.address()[:100]
        execute_query(connection, 
                      "INSERT INTO facility (f_type, f_website, f_address) VALUES (%s, %s, %s)", 
                      (f_type, f_website, f_address))

    # Insert data into facility_contact_number
    for facility_id in range(1, 11):
        contact_number = fake.phone_number()[:15]
        execute_query(connection, 
                      "INSERT INTO facility_contact_number (facility_id, contact_number) VALUES (%s, %s)", 
                      (facility_id, contact_number))

    # Insert data into facility_hospital
    for facility_id in range(1, 11):
        if fake.random_element(elements=facility_types) == 'hospital':
            total_bed = fake.random_int(min=50, max=200)
            number_of_icu = fake.random_int(min=1, max=10)
            number_of_ambulance = fake.random_int(min=1, max=10)
            manager_id = random.randint(1, 20)
            execute_query(connection, 
                          "INSERT INTO facility_hospital (h_facility_id, total_bed, number_of_icu, number_of_ambulance, manager_id) VALUES (%s, %s, %s, %s, %s)", 
                          (facility_id, total_bed, number_of_icu, number_of_ambulance, manager_id))

    # Insert data into facility_hospital_doctor
    for facility_id in range(1, 11):
        if fake.random_element(elements=facility_types) == 'hospital':
            for _ in range(3):
                h_doctor_id = random.randint(1, 20)
                starttime = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
                endtime = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
                dutyhours = round(random.uniform(1.0, 8.0), 1)
                execute_query(connection, 
                              "INSERT INTO facility_hospital_doctor (h_facility_id, h_doctor_id, starttime, endtime, dutyhours) VALUES (%s, %s, %s, %s, %s)", 
                              (facility_id, h_doctor_id, starttime, endtime, dutyhours))

    # Insert data into service
    for _ in range(10):
        servicename = fake.word()[:50]
        description = fake.text(max_nb_chars=255)
        availability = fake.word()[:50]
        execute_query(connection, 
                      "INSERT INTO service (servicename, description, availability) VALUES (%s, %s, %s)", 
                      (servicename, description, availability))

    # Insert data into facility_hospital_service
    

    for facility_id in range(1, 11):
        if fake.random_element(elements=facility_types) == 'hospital':
            for _ in range(3):
                service_id = random.randint(1, 10)
                cost = fake.random_int(min=100, max=10000)
                servicehours = fake.random_int(min=1, max=24)
                capacity = fake.random_int(min=1, max=100)
                execute_query(connection, 
                              "INSERT INTO facility_hospital_service (service_id, h_facility_id, cost, servicehours, capacity) VALUES (%s, %s, %s, %s, %s)", 
                              (service_id, facility_id, cost, servicehours, capacity))

    # Insert data into facility_hospital_service_ambulance
    for service_id in range(1, 11):
        drivername = fake.name()[:50]
        drivercontact = fake.phone_number()[:15]
        vehicletype = fake.word()[:20]
        isavailable = random.choice([True, False])
        execute_query(connection, 
                      "INSERT INTO facility_hospital_service_ambulance (ambulance_service_id, drivername, drivercontact, vehicletype, isavailable) VALUES (%s, %s, %s, %s, %s)", 
                      (service_id, drivername, drivercontact, vehicletype, isavailable))

    # Insert data into facility_hospital_service_icu
    for service_id in range(1, 11):
        wardnumber = fake.bothify(text='??###')[:5]
        capacity = fake.random_int(min=1, max=10)
        doctorhours = fake.random_int(min=1, max=24)
        execute_query(connection, 
                      "INSERT INTO facility_hospital_service_icu (icu_service_id, wardnumber, capacity, doctorhours) VALUES (%s, %s, %s, %s)", 
                      (service_id, wardnumber, capacity, doctorhours))

    # Insert data into facility_hospital_service_bed_service
    for service_id in range(1, 11):
        room_number = fake.bothify(text='??###')[:5]
        bedtype = fake.word()[:20]
        lastoccupieddate = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        execute_query(connection, 
                      "INSERT INTO facility_hospital_service_bed_service (bed_service_id, room_number, bedtype, lastoccupieddate) VALUES (%s, %s, %s, %s)", 
                      (service_id, room_number, bedtype, lastoccupieddate))

    # Insert data into facility_diagnostic_center
    for facility_id in range(1, 11):
        if fake.random_element(elements=facility_types) == 'diagnostic':
            license_number = fake.bothify(text='??###-###-###')[:20]
            execute_query(connection, 
                          "INSERT INTO facility_diagnostic_center (diag_facility_id, license_number) VALUES (%s, %s)", 
                          (facility_id, license_number))

    # Insert data into test
    for _ in range(10):
        testname = fake.word()[:20]
        testdate = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        testdescription = fake.text(max_nb_chars=255)
        execute_query(connection, 
                      "INSERT INTO test (testname, testdate, testdescription) VALUES (%s, %s, %s)", 
                      (testname, testdate, testdescription))

    # Insert data into facility_diagnostic_center_test
    for facility_id in range(1, 11):
        if fake.random_element(elements=facility_types) == 'diagnostic':
            for _ in range(3):
                test_id = random.randint(1, 10)
                cost = fake.random_int(min=100, max=5000)
                equipmentused = fake.word()[:20]
                execute_query(connection, 
                              "INSERT INTO facility_diagnostic_center_test (diag_facility_id, test_id, cost, equipmentused) VALUES (%s, %s, %s, %s)", 
                              (facility_id, test_id, cost, equipmentused))

    # Insert data into facility_pharmacy
    for facility_id in range(1, 11):
        if fake.random_element(elements=facility_types) == 'pharmacy':
            license_number = fake.bothify(text='??###-###-###')[:20]
            execute_query(connection, 
                          "INSERT INTO facility_pharmacy (facility_pharmacy_id, license_number) VALUES (%s, %s)", 
                          (facility_id, license_number))

    # Insert data into medicine
    for _ in range(10):
        name = fake.word()[:50]
        manufacturer = fake.company()[:50]
        expiry_date = fake.date_time_between(start_date='now', end_date='+2y').strftime('%Y-%m-%d %H:%M:%S')
        manufacture_date = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
        prescription_id = random.randint(1, 10)
        execute_query(connection, 
                      "INSERT INTO medicine (name, manufacturer, expiry_date, manufacture_date, prescription_id) VALUES (%s, %s, %s, %s, %s)", 
                      (name, manufacturer, expiry_date, manufacture_date, prescription_id))

    # Insert data into medicine_inventory
    for _ in range(10):
        inventory_medicine_id = random.randint(1, 10)
        inventory_pharmacy_facility_id = random.randint(1, 10)
        quantity = random.randint(10, 100)
        cost_per_unit = round(random.uniform(1.0, 100.0), 2)
        batch_no = fake.bothify(text='??###-###-###')[:15]
        execute_query(connection, 
                      "INSERT INTO medicine_inventory (inventory_medicine_id, inventory_pharmacy_facility_id, quantity, cost_per_unit, batch_no) VALUES (%s, %s, %s, %s, %s)", 
                      (inventory_medicine_id, inventory_pharmacy_facility_id, quantity, cost_per_unit, batch_no))

    # Insert data into prescription
    for _ in range(10):
        doctor_user_id = random.randint(1, 20)
        patient_user_id = random.randint(1, 20)
        diet_id = random.randint(1, 10)
        prescriptiondate = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        prescriptiondescription = fake.text(max_nb_chars=255)
        execute_query(connection, 
                      "INSERT INTO prescription (doctor_user_id, patient_user_id, diet_id, prescriptiondate, prescriptiondescription) VALUES (%s, %s, %s, %s, %s)", 
                      (doctor_user_id, patient_user_id, diet_id, prescriptiondate, prescriptiondescription))

    # Insert data into prescription_medicine_record
    for _ in range(10):
        medicine_record_prescription_id = random.randint(1, 10)
        quantity = round(random.uniform(1.0, 10.0), 2)
        frequency = random.randint(1, 4)
        medicine_record_medicine_id = random.randint(1, 10)
        dosage = random.randint(1, 4)
        intake_days = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        execute_query(connection, 
                      "INSERT INTO prescription_medicine_record (medicine_record_prescription_id, quantity, frequency, medicine_record_medicine_id, dosage, intake_days) VALUES (%s, %s, %s, %s, %s, %s)", 
                      (medicine_record_prescription_id, quantity, frequency, medicine_record_medicine_id, dosage, intake_days))

    # Insert data into prescription_test_record
    for _ in range(10):
        prescription_record_test_id = random.randint(1, 10)
        prescription_record_prescription_id = random.randint(1, 10)
        test_date = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        result = fake.text(max_nb_chars=255)
        execute_query(connection, 
                      "INSERT INTO prescription_test_record (prescription_record_test_id, prescription_record_prescription_id, test_date, result) VALUES (%s, %s, %s, %s)", 
                      (prescription_record_test_id, prescription_record_prescription_id, test_date, result))

    # Insert data into hhms_user_patient_doctor_recommendation
    for _ in range(10):
        recommended_doc_id = random.randint(1, 20)
        description = fake.text(max_nb_chars=255)
        reason_for_recommendation = fake.text(max_nb_chars=255)
        recommendationdate = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
        execute_query(connection, 
                      "INSERT INTO hhms_user_patient_doctor_recommendation (recommended_doc_id, description, reason_for_recommendation, recommendationdate) VALUES (%s, %s, %s, %s)", 
                      (recommended_doc_id, description, reason_for_recommendation, recommendationdate))

def main():
    connection = create_connection("localhost", "root", "6947", "noureenSuxDik")

    
    seed_data(connection)

if __name__ == "__main__":
    main()
