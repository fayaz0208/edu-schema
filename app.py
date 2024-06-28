from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='eduschema',
            user='root',
            password='Sathya143#'
        )
        if conn.is_connected():
            print('Connected to MySQL database')
        return conn
    except Error as e:
        print(e)
        return None

conn = connect()
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('home.html')

# Course Management
@app.route('/course_management', methods=['GET', 'POST'])
def course_management():
    if request.method == 'POST':
        action = request.form.get('action')
        course_id = request.form.get('course_id')
        course_name = request.form.get('course_name')
        course_description = request.form.get('course_description')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        if action == 'Add':
            query = "INSERT INTO Courses (course_name, course_description, start_date, end_date) VALUES (%s, %s, %s, %s)"
            values = (course_name, course_description, start_date, end_date)
            cursor.execute(query, values)
            conn.commit()
            flash('Course added successfully.')
        elif action == 'Update':
            query = "UPDATE Courses SET course_name = %s, course_description = %s, start_date = %s, end_date = %s WHERE course_id = %s"
            values = (course_name, course_description, start_date, end_date, course_id)
            cursor.execute(query, values)
            conn.commit()
            flash('Course updated successfully.')
        elif action == 'Remove':
            query = "DELETE FROM Courses WHERE course_id = %s"
            cursor.execute(query, (course_id,))
            conn.commit()
            flash('Course removed successfully.')
        return redirect(url_for('course_management'))
    else:
        cursor.execute("SELECT * FROM Courses")
        courses = cursor.fetchall()
        return render_template('course_management.html', courses=courses)

# Instructors Management
@app.route('/instructor_management', methods=['GET', 'POST'])
def instructor_management():
    if request.method == 'POST':
        action = request.form.get('action')
        instructor_id = request.form.get('instructor_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        bio = request.form.get('bio')

        if action == 'Add':
            query = "INSERT INTO Instructors (first_name, last_name, email, bio) VALUES (%s, %s, %s, %s)"
            values = (first_name, last_name, email, bio)
            cursor.execute(query, values)
            conn.commit()
            flash('Instructor added successfully.')
        elif action == 'Update':
            query = "UPDATE Instructors SET first_name = %s, last_name = %s, email = %s, bio = %s WHERE instructor_id = %s"
            values = (first_name, last_name, email, bio, instructor_id)
            cursor.execute(query, values)
            conn.commit()
            flash('Instructor updated successfully.')
        elif action == 'Remove':
            query = "DELETE FROM Instructors WHERE instructor_id = %s"
            cursor.execute(query, (instructor_id,))
            conn.commit()
            flash('Instructor removed successfully.')
        return redirect(url_for('instructor_management'))
    else:
        cursor.execute("SELECT * FROM Instructors")
        instructors = cursor.fetchall()
        return render_template('instructor_management.html', instructors=instructors)

# Student Enrollment
@app.route('/student_enrollment', methods=['GET', 'POST'])
def student_enrollment():
    if request.method == 'POST':
        action = request.form.get('action')
        student_id = request.form.get('student_id')
        course_id = request.form.get('course_id')
        enrollment_date = request.form.get('enrollment_date')
        
        if action == 'Enroll':
            query = "INSERT INTO Enrollments (student_id, course_id, enrollment_date) VALUES (%s, %s, %s)"
            values = (student_id, course_id, enrollment_date)
            cursor.execute(query, values)
            conn.commit()
            flash('Student enrolled successfully.')
        return redirect(url_for('student_enrollment'))
    else:
        cursor.execute("SELECT * FROM Enrollments")
        enrollments = cursor.fetchall()
        return render_template('student_enrollment.html', enrollments=enrollments)

# Assessment and Grades
@app.route('/assessment_grades', methods=['GET', 'POST'])
def assessment_grades():
    if request.method == 'POST':
        action = request.form.get('action')
        course_id = request.form.get('course_id')
        assessment_id = request.form.get('assessment_id')
        assessment_name = request.form.get('assessment_name')
        assessment_type = request.form.get('assessment_type')
        max_score = request.form.get('max_score')
        student_id = request.form.get('student_id')
        score = request.form.get('score')
        graded_date = request.form.get('graded_date')

        if action == 'Create':
            query = "INSERT INTO Assessments (course_id, assessment_name, assessment_type, max_score) VALUES (%s, %s, %s, %s)"
            values = (course_id, assessment_name, assessment_type, max_score)
            cursor.execute(query, values)
            conn.commit()
            flash('Assessment created successfully.')
        elif action == 'Input':
            query = "INSERT INTO Grades (student_id, assessment_id, score, graded_date) VALUES (%s, %s, %s, %s)"
            values = (student_id, assessment_id, score, graded_date)
            cursor.execute(query, values)
            conn.commit()
            flash('Grade inputted successfully.')
        return redirect(url_for('assessment_grades'))
    else:
        cursor.execute("SELECT * FROM Assessments")
        assessments = cursor.fetchall()
        cursor.execute("SELECT * FROM Grades")
        grades = cursor.fetchall()
        return render_template('assessment_grades.html', assessments=assessments, grades=grades)

if __name__ == '__main__':
    app.run(debug=True)

# Don't forget to close the connection when you're done
close_connection(conn)
