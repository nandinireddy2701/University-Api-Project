import redis
import json

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def retrieve_data_from_redis(key):
    """
    Retrieve data from Redis by the provided key.
    """
    data = redis_client.get(key)
    
    if data:
        return json.loads(data)  
    else:
        return None

def main():
    # Data for Computer Science department
    dept_key = "departments:CompSci"
    print(f"Retrieving data for key: {dept_key}")
    dept_data = retrieve_data_from_redis(dept_key)
    
    if dept_data:
        print(f"\nData for Computer Science department:")
        print(json.dumps(dept_data, indent=4))  
    else:
        print(f"No data found for key: {dept_key}")
    
    # Data for student "Peter Lynch"
    student_key = "students:1999"
    print(f"\nRetrieving data for key: {student_key}")
    student_data = retrieve_data_from_redis(student_key)
    
    if student_data:
        print(f"\nData for student 'Peter Lynch':")
        print(json.dumps(student_data, indent=4))  
    else:
        print(f"No data found for key: {student_key}")
    
    # Data for course "Data Engineering"
    course_key = "courses:Data1050"
    print(f"\nRetrieving data for key: {course_key}")
    course_data = retrieve_data_from_redis(course_key)
    
    if course_data:
        print(f"\nData for course 'Data Engineering':")
        print(json.dumps(course_data, indent=4))  
    else:
        print(f"No data found for key: {course_key}")

if __name__ == "__main__":
    main()