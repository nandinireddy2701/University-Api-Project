import redis
import json
from main import fetch_departments, fetch_students, fetch_courses

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def store_data_in_redis(key_prefix, data):
    """
    Stores the provided data under the given key_prefix in Redis.
    Stores the full item as a JSON string.
    """
    for item in data:
        if key_prefix == "departments":
            key = f"{key_prefix}:{item['dept_name']}"
        elif key_prefix == "students":
            key = f"{key_prefix}:{item['id']}"
        elif key_prefix == "courses":
            key = f"{key_prefix}:{item['course_id']}"
        else:
            print(f" Unknown data type for key_prefix: {key_prefix}")
            continue

        redis_client.set(key, json.dumps(item))
        print(f" Stored key: {key}")
        print(f"Storing data: {json.dumps(item)}")
        
        # Store the entire item as a JSON string
        redis_client.set(key, json.dumps(item))
        print(f" Stored key: {key}, value: {json.dumps(item)}")

def main():
    departments_data = fetch_departments()
    students_data = fetch_students()
    courses_data = fetch_courses()

    print("Storing data in Redis...")
    store_data_in_redis("departments", departments_data)
    store_data_in_redis("students", students_data)
    store_data_in_redis("courses", courses_data)

if __name__ == "__main__":
    main()