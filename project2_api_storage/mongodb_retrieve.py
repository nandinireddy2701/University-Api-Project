from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["university_data"]  # Your database name

# Function to get the number of documents in a collection
def get_collection_length(collection_name):
    collection = db[collection_name]
    count = collection.count_documents({})
    return count

# Function to find how many instructors belong to Computer Science department
def get_instructors_in_computer_science():
    departments = db.departments.find({"dept_name": "CompSci"})
    for dept in departments:
        instructors = dept.get('instructors', [])
        return len(instructors)  # Return the number of instructors

# Function to find how many courses Peter Lynch took in Fall 2023
def get_courses_taken_by_peter_lynch():
    students = db.students.find({"name": "Peter Lynch"})
    for student in students:
        courses = student.get('courses', [])
        fall_2023_courses = [course for course in courses if course['semester'] == 'Fall' and course['year'] == 2023]
        return len(fall_2023_courses)  

# Function to find who taught the course "Hands-on Data Science" and when
def get_instructor_for_hands_on_data_science():
    courses = db.courses.find({"title": "Hands-on data science"})
    for course in courses:
        instructors = course.get('instructors', [])
        if instructors:
            instructor_info = []
            for instructor in instructors:
                instructor_info.append({
                    'name': instructor['name'],
                    'section': instructor['section'],
                    'semester': instructor['semester'],
                    'year': instructor['year']
                })
            return instructor_info  

# Function to execute the queries and print the results
def retrieve_and_print_results():
    # Get collection lengths
    departments_count = get_collection_length("departments")
    students_count = get_collection_length("students")
    courses_count = get_collection_length("courses")

    print(f"Total number of departments: {departments_count}")
    print(f"Total number of students: {students_count}")
    print(f"Total number of courses: {courses_count}")
    
    # Get the number of instructors in the Computer Science department
    cs_instructors_count = get_instructors_in_computer_science()
    print(f"Number of instructors in Computer Science department: {cs_instructors_count}")
    
    # Get the number of courses Peter Lynch took in Fall 2023
    peter_lynch_courses = get_courses_taken_by_peter_lynch()
    print(f"Number of courses Peter Lynch took in Fall 2023: {peter_lynch_courses}")
    
    # Get the instructor(s) for the course "Hands-on data science"
    hands_on_data_science_instructors = get_instructor_for_hands_on_data_science()
    print(f"Instructor(s) for Hands-on Data Science course:")
    for instructor in hands_on_data_science_instructors:
        print(f" - {instructor['name']} taught in {instructor['semester']} {instructor['year']} (Section: {instructor['section']})")

if __name__ == "__main__":
    retrieve_and_print_results()
