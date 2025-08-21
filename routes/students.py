from flask import Blueprint, request, jsonify
from flasgger import swag_from
from db_config import get_db_connection

students_bp = Blueprint('students', __name__)

@students_bp.route('/students', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Page number'
        },
        {
            'name': 'page_size',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'Number of records per page'
        }
    ],
    'responses': {
        200: {
            'description': 'A list of students with enrolled courses',
            'schema': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer'},
                    'msg': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'records': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {'type': 'string'},
                                        'name': {'type': 'string'},
                                        'dept_name': {'type': 'string'},
                                        'courses': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'course_id': {'type': 'string'},
                                                    'section_id': {'type': 'integer'},
                                                    'semester': {'type': 'string'},
                                                    'year': {'type': 'integer'}
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            'total': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    }
})
def get_students():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))

        if page <= 0:
            return jsonify({"code": 0, "msg": "There is no negative or zero page number please Enter a valid page number greater than 0", "data": {"records": [], "total": 0}})
        if page_size <= 0:
            return jsonify({"code": 0, "msg": "There is no negative or zero page number please Enter a valid page size greater than 0", "data": {"records": [], "total": 0}})

        offset = (page - 1) * page_size
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM student")
        total = cur.fetchone()[0]

        cur.execute("""
            SELECT ID, name, dept_name FROM student
            ORDER BY ID
            LIMIT %s OFFSET %s
        """, (page_size, offset))
        students = cur.fetchall()

        records = []
        for student in students:
            student_id, name, dept_name = student
            cur.execute("""
                SELECT course_id, sec_id, semester, year
                FROM takes
                WHERE ID = %s
            """, (student_id,))
            courses = cur.fetchall()

            records.append({
                "id": str(student_id),
                "name": name,
                "dept_name": dept_name,
                "courses": [
                    {"course_id": c[0], "section_id": c[1], "semester": c[2], "year": c[3]} for c in courses
                ]
            })

        total_records = len(records)
        cur.close()
        conn.close()

        return jsonify({"code": 1, "msg": "Success", "data": {"records": records, "total": total_records}})

    except Exception as e:
        return jsonify({"code": 0, "msg": str(e), "data": {"records": [], "total": 0}})