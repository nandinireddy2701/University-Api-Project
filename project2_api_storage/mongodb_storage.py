from pymongo import MongoClient
from main import fetch_departments, fetch_students, fetch_courses

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["university_data"]  

# Function to insert departments into MongoDB
def insert_departments_to_db(departments):
    for dept in departments:
        db.departments.update_one(
            {"dept_name": dept['dept_name']},  
            {"$set": dept},  
            upsert=True  
        )
    print("Departments inserted into MongoDB.")

# Function to insert students into MongoDB
def insert_students_to_db(students):
    for student in students:
        db.students.update_one(
            {"id": student['id']},  
            {"$set": student},  
            upsert=True
        )
    print("Students inserted into MongoDB.")

# Function to insert courses into MongoDB
def insert_courses_to_db(courses):
    for course in courses:
        db.courses.update_one(
            {"course_id": course['course_id']},  
            {"$set": course},  
            upsert=True
        )
    print("Courses inserted into MongoDB.")

# Function to fetch and store data in MongoDB
def run_fetch_and_store_operations():
    print("Fetching departments data...")
    departments = fetch_departments()  
    insert_departments_to_db(departments)  
    
    print("Fetching students data...")
    students = fetch_students()  
    insert_students_to_db(students)  

    print("Fetching courses data...")
    courses = fetch_courses()  
    insert_courses_to_db(courses)  

if __name__ == "__main__":
    run_fetch_and_store_operations()
