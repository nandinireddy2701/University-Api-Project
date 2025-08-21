from flask import Blueprint, request, jsonify
from flasgger import swag_from
from db_config import get_db_connection

departments_bp = Blueprint('departments', __name__)

@departments_bp.route('/departments', methods=['GET'])
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
            'description': 'A list of departments with instructors',
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
                                        'dept_name': {'type': 'string'},
                                        'building': {'type': 'string'},
                                        'budget': {'type': 'number'},
                                        'instructors': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'object',
                                                'properties': {
                                                    'id': {'type': 'string'},
                                                    'name': {'type': 'string'},
                                                    'salary': {'type': 'integer'}
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
def get_departments():
    try:
        # Parse query parameters safely
        try:
            page = int(request.args.get('page', 1))
        except (ValueError, TypeError):
            return jsonify({
                "code": 0,
                "msg": "Page must be a valid positive integer",
                "data": {"records": [], "total": 0}
            })

        try:
            page_size_raw = request.args.get('page_size', 10)
            page_size = int(page_size_raw) if page_size_raw else 10
        except (ValueError, TypeError):
            return jsonify({
                "code": 0,
                "msg": "Page size must be a valid positive integer",
                "data": {"records": [], "total": 0}
            })

        if page <= 0:
            return jsonify({
                "code": 0,
                "msg": "There is no negative or zero page number please Enter a valid page number greater than 0",
                "data": {"records": [], "total": 0}
            })

        if page_size <= 0:
            return jsonify({
                "code": 0,
                "msg": "There is no negative or zero page number please Enter a valid page size greater than 0",
                "data": {"records": [], "total": 0}
            })

        offset = (page - 1) * page_size

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT dept_name, building, budget
            FROM department
            ORDER BY dept_name
            LIMIT %s OFFSET %s
        """, (page_size, offset))
        departments = cur.fetchall()

        records = []
        for dept in departments:
            dept_name, building, budget = dept

            cur.execute("""
                SELECT id, name, salary
                FROM instructor
                WHERE dept_name = %s
            """, (dept_name,))
            instructors = cur.fetchall()

            records.append({
                "dept_name": dept_name,
                "building": building,
                "budget": budget,
                "instructors": [
                    {"id": str(instr[0]), "name": instr[1], "salary": instr[2]} for instr in instructors
                ]
            })

        total_records = len(records)

        cur.close()
        conn.close()

        return jsonify({
            "code": 1,
            "msg": "Success",
            "data": {
                "records": records,
                "total": total_records
            }
        })

    except Exception as e:
        return jsonify({
            "code": 0,
            "msg": str(e),
            "data": {"records": [], "total": 0}
        })