import urllib.request
from flask import Flask, render_template, redirect, jsonify, request
from flask_cors import CORS
import subprocess
import sys
import re
from wit import Wit


app = Flask(__name__)
CORS(app)



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/parseHere/', methods = ['POST'])
def parse():
    text = request.form["pageData"]
    return parsify(text)


@app.route('/imageProcess/', methods = ['POST'])
def imgProc():
    url = request.form["pageData"]
    urllib.request.urlretrieve(url, "./temp.jpg")
    subprocess.call(["gocr", "./temp.jpg", "-o", "file"])
    f = open('file', 'r')
    return parsify(f.read())


def parsify(text):





#controller
@app.route('/students/')
def get_all_students():
    students = Student.query.all()
    return render_template('students_all.html', students=students)

@app.route('/students/<rollno>', methods=['GET', 'POST'])
def individual_student_op(rollno):
    if request.method == 'GET':
        students = Student.query.\
                filter(Student.rollno == rollno).\
                all()
        return render_template('students_all.html', students=students)
    else:
        def update_student():

            student= Student.query.\
                     filter(Student.rollno == rollno).\
                     first()
            student.name = name
            db.session.commit()



@app.route('/students/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'GET':
        return render_template('create_student.html')
    else:
        print(request.form)
        # ^ Dictionary
        new = Student(request.form["rollno"], request.form["name"])
        db.session.add(new)
        db.session.commit()
        return redirect('/students/%s'%(new.rollno))

@app.route('/students/search?q=<key>')
def find_student(key):
    new = Student.query.\
        filter(Student.name == key).\
        first()
    print(new)
    return redirect('/students/%s'%(new.rollno))


@app.route('/students/<rollno>/delete', methods=['POST'])
def delete_student(rollno):
    students = Student.query.\
        filter(Student.rollno == rollno).\
        first()
    db.session.delete(students)
    db.session.commit()
    return redirect('/students/')



@app.route('/courses/')
def get_all_courses():
    courses = Course.query.all()
    return render_template('courses_all.html', courses=courses)

@app.route('/courses/<code>', methods=['GET', 'POST'])
def individual_course_op(code):
    if request.method == 'GET':
        courses = Course.query.\
                filter(Course.code == code).\
                all()
        return render_template('courses_all.html', courses=courses)
    else:
        def update_course():

            course= Course.query.\
                     filter(Course.code == code).\
                     first()
            course.name = name
            db.session.commit()



@app.route('/courses/create', methods=['GET', 'POST'])
def create_course():
    if request.method == 'GET':
        return render_template('create_course.html')
    else:
        print(request.form)
        # ^ Dictionary
        new = Course(request.form["code"], request.form["name"])
        db.session.add(new)
        db.session.commit()
        return redirect('/courses/%s'%(new.code))

@app.route('/courses/<code>/delete', methods=['POST'])
def delete_course(code):
    courses = Course.query.\
        filter(Course.code == code).\
        first()
    db.session.delete(courses)
    db.session.commit()
    return redirect('/courses/')

@app.route('/courses/search?q=<key>')
def find_course(key):
    new = Course.query.\
        filter(Course.name == key).\
        first()
    return redirect('/courses/%s'%(new.code))

app.run(host='localhost', port=3000, debug=True)
