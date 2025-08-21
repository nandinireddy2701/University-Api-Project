import requests

# Function to fetch departments
def fetch_departments():
    base_url = "http://127.0.0.1:5001/departments"
    page = 1
    all_records = []
    total_records = None

    while True:
        response = requests.get(base_url, params={"page": page})
        
        if response.status_code != 200:
            print(f"Failed to fetch page {page}. Status code:", response.status_code)
            break

        result = response.json()
        records = result["data"]["records"]
        all_records.extend(records)

        if total_records is None:
            total_records = result["data"]["total"]

        # If we've collected all records, break the loop
        if len(all_records) >= total_records:
            break

        page += 1

    # Now print all records
    print("Total Departments:", len(all_records))
    print("\nDepartments and Instructors:\n")
    for dept in all_records:
        print(f"Department: {dept['dept_name']}")
        print(f"  Building: {dept['building']}")
        print(f"  Budget: ${dept['budget']}")
        if dept['instructors']:
            print("  Instructors:")
            for instructor in dept['instructors']:
                print(f"    - {instructor['name']} (ID: {instructor['id']}, Salary: ${instructor['salary']})")
        else:
            print("  No instructors.")
        print("-" * 40)

    return all_records


# Function to fetch students
def fetch_students():
    base_url = "http://127.0.0.1:5001/students"
    page = 1
    all_students = []

    while True:
        response = requests.get(base_url, params={"page": page})

        if response.status_code != 200:
            print(f"Failed to fetch page {page}. Status code:", response.status_code)
            break

        result = response.json()
        students = result["data"]["records"]

        if not students:
            break  # No more data

        all_students.extend(students)

        if len(students) < 10:  # Assuming the API returns 10 records per page max
            break

        page += 1

    print(f"\n Total Students Fetched: {len(all_students)}\n")
    for student in all_students:
        print(f" ID: {student['id']}")
        print(f"   Name: {student['name']}")
        print(f"   Department: {student['dept_name']}")

        if student['courses']:
            print("    Enrolled Courses:")
            for course in student['courses']:
                print(f"     - {course['course_id']} | Section {course['section_id']} | {course['semester']} {course['year']}")
        else:
            print("    Enrolled Courses: None")

        print("-" * 50)

    return all_students


# Function to fetch courses
def fetch_courses():
    base_url = "http://127.0.0.1:5001/courses"
    page = 1
    all_courses = []

    while True:
        response = requests.get(base_url, params={"page": page})

        if response.status_code != 200:
            print(f" Failed to fetch page {page}. Status code:", response.status_code)
            break

        result = response.json()
        courses = result["data"]["records"]

        if not courses:
            break

        all_courses.extend(courses)

        if len(courses) < 10:  # Assuming 10 records per page
            break

        page += 1

    print(f"\n Total Courses Fetched: {len(all_courses)}\n")
    for course in all_courses:
        print(f" Course ID: {course['course_id']}")
        print(f"   Title: {course['title']}")
        print(f"   Department: {course['dept_name']}")

        if course['instructors']:
            print("    Instructors:")
            for instructor in course['instructors']:
                print(f"     - {instructor['name']} (ID: {instructor['instructor_id']}) | Section {instructor['section']} | {instructor['semester']} {instructor['year']}")
        else:
            print("    Instructors: None")

        print("-" * 50)

    return all_courses



# Function to run all fetch operations
def run_fetch_operations():
    print("Fetching departments data...")
    fetch_departments()
    
    print("Fetching students data...")
    fetch_students()

    print("Fetching courses data...")
    fetch_courses()

if __name__ == "__main__":
    run_fetch_operations()


