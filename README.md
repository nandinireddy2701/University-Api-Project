#  University Information System APIs

##  Project Overview  
This project implements a set of **RESTful APIs** for a University Information System to manage **Departments, Students, and Courses**. The APIs provide structured JSON responses, support **pagination**, and are designed for integration with external applications or analytical workflows.  

The project was extended to **Project 2**, where the API data was integrated with **Redis** (key-value storage) and **MongoDB** (document collections) for scalable data retrieval, storage, and analysis.  

--------

##  Objectives  
- Provide detailed **department information** with associated instructors.  
- Retrieve **student details** along with their enrolled courses.  
- List **courses** and their respective instructors.  
- Support **pagination** for efficient data handling.  
- Ensure consistent **JSON schema** across all endpoints.  
- Integrate APIs with **Redis** and **MongoDB** for persistence and querying.  

--------

##  Tech Stack  
- Backend: Python (FastAPI / Flask)  
- Database: PostgreSQL  
- Storage: Redis, MongoDB  
- Testing: Postman  
- Visualization (Bonus): Static HTML homepage  

--------

##  API Endpoints (Project 1)

### 1. Departments API  
**Endpoint:** `GET /departments`  
- Retrieves department information with instructors.  
- **Query Parameters:**  
  - `page` → page number (default: 1)  
  - `page_size` → records per page (default: 10)  

### 2. Students API  
**Endpoint:** `GET /students`  
- Retrieves student details and enrolled courses.  
- **Query Parameters:**  
  - `page` → page number (default: 1)  
  - `page_size` → records per page (default: 10)  

### 3. Courses API  
**Endpoint:** `GET /courses`  
- Retrieves course details and assigned instructors.  
- **Query Parameters:**  
  - `page` → page number (default: 1)  
  - `page_size` → records per page (default: 10)  

--------

##  Data Integration (Project 2)  

###  Redis  
- Data stored as **key-value pairs** with API-specific folders:  
  - `departments:{id}`  
  - `students:{id}`  
  - `courses:{id}`  
- Example: students:101 → {student data} 

###  MongoDB  
- Data stored in **separate collections**:  
- `departments`  
- `students`  
- `courses`  

--------

###  Queries Performed  
**Redis:**  
- Retrieve Computer Science department.  
- Retrieve student *Peter Lynch*.  
- Retrieve course *Data Engineering*.  

 **MongoDB:**  
- Count total documents in each collection.  
- Find instructors in the Computer Science department.  
- Find courses taken by *Peter Lynch* in Fall 2023.  
- Find instructor of *Hands-on Data Science* and semester taught.  

--------

### Test endpoints via Postman or browser:

http://127.0.0.1:5001/departments

http://127.0.0.1:5001/students

http://127.0.0.1:5001/courses














