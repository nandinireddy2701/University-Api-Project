# app.py
from flask import Flask, send_from_directory
from routes.departments import departments_bp
from routes.students import students_bp
from routes.courses import courses_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(departments_bp)
app.register_blueprint(students_bp)
app.register_blueprint(courses_bp)

# Bonus: Static Homepage
@app.route('/')
def homepage():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
