from flask import Blueprint, request, jsonify
from flasgger import swag_from
from db_config import get_db_connection

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/courses', methods=['GET'])
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
            'description': 'A list of courses with instructors',
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
                                        'course_id': {'type': 'string'},
                                        'title': {'type': 'string'},
                                        'dept_name': {'type': 'string'},
                                        'instructors': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'instructor_id': {'type': 'string'},
                                                    'name': {'type': 'string'},
                                                    'section': {'type': 'integer'},
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
def get_courses():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))

        if page <= 0:
            return jsonify({"code": 0, "msg": "There is no negative or zero page number please Enter a valid page number which is greater than 0", "data": {"records": [], "total": 0}})
        if page_size <= 0:
            return jsonify({"code": 0, "msg": "There is no negative or zero page number please Enter a valid page size greater than 0", "data": {"records": [], "total": 0}})

        offset = (page - 1) * page_size
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT course_id, title, dept_name
            FROM course
            ORDER BY course_id
            LIMIT %s OFFSET %s
        """, (page_size, offset))
        courses = cur.fetchall()

        records = []
        for course in courses:
            course_id, title, dept_name = course
            cur.execute("""
                SELECT t.ID, i.name, t.sec_id, t.semester, t.year
                FROM teaches t
                JOIN instructor i ON t.ID = i.ID
                WHERE t.course_id = %s
            """, (course_id,))
            instructors = cur.fetchall()

            records.append({
                "course_id": course_id,
                "title": title,
                "dept_name": dept_name,
                "instructors": [
                    {"instructor_id": str(i[0]), "name": i[1], "section": i[2], "semester": i[3], "year": i[4]} for i in instructors
                ]
            })

        total_records = len(records)
        cur.close()
        conn.close()

        return jsonify({"code": 1, "msg": "Success", "data": {"records": records, "total": total_records}})

    except Exception as e:
        return jsonify({"code": 0, "msg": str(e), "data": {"records": [], "total": 0}})