# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Class, Section, Student
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()
    
    # Add sample data if empty
    if Class.query.count() == 0:
        # Create classes
        classes = ['Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5']
        for class_name in classes:
            cls = Class(name=class_name)
            db.session.add(cls)
        
        db.session.commit()
        
        # Create sections for each class
        sections = ['A', 'B', 'C']
        for cls in Class.query.all():
            for section_name in sections:
                section = Section(name=section_name, class_id=cls.id)
                db.session.add(section)
        
        db.session.commit()
        
        # Add sample students
        sample_students = [
            ("2024001", "John Doe", "john@example.com", "1234567890", "Class 1", "A"),
            ("2024002", "Jane Smith", "jane@example.com", "1234567891", "Class 1", "A"),
            ("2024003", "Mike Johnson", "mike@example.com", "1234567892", "Class 1", "B"),
            ("2024004", "Sarah Williams", "sarah@example.com", "1234567893", "Class 2", "A"),
            ("2024005", "Tom Brown", "tom@example.com", "1234567894", "Class 2", "B"),
            ("2024006", "Lisa Davis", "lisa@example.com", "1234567895", "Class 3", "A"),
        ]
        
        for roll, name, email, phone, class_name, section_name in sample_students:
            class_obj = Class.query.filter_by(name=class_name).first()
            section_obj = Section.query.filter_by(name=section_name, class_id=class_obj.id).first()
            
            student = Student(
                roll_number=roll,
                name=name,
                email=email,
                phone=phone,
                class_id=class_obj.id,
                section_id=section_obj.id
            )
            db.session.add(student)
        
        db.session.commit()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# Student Management
@app.route('/students')
def list_students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        roll_number = request.form.get('roll_number')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        class_id = request.form.get('class_id')
        section_id = request.form.get('section_id')
        
        # Check if roll number exists
        existing = Student.query.filter_by(roll_number=roll_number).first()
        if existing:
            flash('Roll number already exists!', 'error')
            return redirect(url_for('add_student'))
        
        student = Student(
            roll_number=roll_number,
            name=name,
            email=email,
            phone=phone,
            class_id=class_id,
            section_id=section_id
        )
        
        db.session.add(student)
        db.session.commit()
        
        flash('Student added successfully!', 'success')
        return redirect(url_for('list_students'))
    
    classes = Class.query.all()
    sections = Section.query.all()
    return render_template('add_student.html', classes=classes, sections=sections)

@app.route('/student/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    
    if request.method == 'POST':
        student.roll_number = request.form.get('roll_number')
        student.name = request.form.get('name')
        student.email = request.form.get('email')
        student.phone = request.form.get('phone')
        student.class_id = request.form.get('class_id')
        student.section_id = request.form.get('section_id')
        
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('list_students'))
    
    classes = Class.query.all()
    sections = Section.query.all()
    return render_template('edit_student.html', student=student, classes=classes, sections=sections)

@app.route('/student/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('list_students'))

# Class Management
@app.route('/classes')
def list_classes():
    classes = Class.query.all()
    return render_template('classes.html', classes=classes)

@app.route('/class/add', methods=['POST'])
def add_class():
    name = request.form.get('name')
    
    existing = Class.query.filter_by(name=name).first()
    if existing:
        flash('Class already exists!', 'error')
    else:
        class_obj = Class(name=name)
        db.session.add(class_obj)
        db.session.commit()
        flash('Class added successfully!', 'success')
    
    return redirect(url_for('list_classes'))

@app.route('/class/delete/<int:id>')
def delete_class(id):
    class_obj = Class.query.get_or_404(id)
    db.session.delete(class_obj)
    db.session.commit()
    flash('Class deleted successfully!', 'success')
    return redirect(url_for('list_classes'))

# Section Management
@app.route('/sections')
def list_sections():
    sections = Section.query.all()
    return render_template('sections.html', sections=sections)

@app.route('/section/add', methods=['POST'])
def add_section():
    name = request.form.get('name')
    class_id = request.form.get('class_id')
    
    existing = Section.query.filter_by(name=name, class_id=class_id).first()
    if existing:
        flash('Section already exists for this class!', 'error')
    else:
        section = Section(name=name, class_id=class_id)
        db.session.add(section)
        db.session.commit()
        flash('Section added successfully!', 'success')
    
    return redirect(url_for('list_sections'))

@app.route('/section/delete/<int:id>')
def delete_section(id):
    section = Section.query.get_or_404(id)
    db.session.delete(section)
    db.session.commit()
    flash('Section deleted successfully!', 'success')
    return redirect(url_for('list_sections'))

# API endpoint to get sections for a class (for dynamic forms)
@app.route('/api/sections/<int:class_id>')
def get_sections(class_id):
    sections = Section.query.filter_by(class_id=class_id).all()
    return jsonify([{'id': s.id, 'name': s.name} for s in sections])

# MAIN FEATURE: Show Students by Class & Section
@app.route('/students/by-class')
def students_by_class():
    classes = Class.query.all()
    selected_class = request.args.get('class_id', type=int)
    selected_section = request.args.get('section_id', type=int)
    
    students = []
    class_name = ""
    section_name = ""
    
    if selected_class and selected_section:
        students = Student.query.filter_by(
            class_id=selected_class, 
            section_id=selected_section
        ).all()
        
        class_obj = Class.query.get(selected_class)
        section_obj = Section.query.get(selected_section)
        class_name = class_obj.name if class_obj else ""
        section_name = section_obj.name if section_obj else ""
    
    # Get sections for the selected class
    sections = []
    if selected_class:
        sections = Section.query.filter_by(class_id=selected_class).all()
    
    return render_template(
        'students_by_class.html',
        classes=classes,
        sections=sections,
        selected_class=selected_class,
        selected_section=selected_section,
        students=students,
        class_name=class_name,
        section_name=section_name
    )

# Alternative: View with filter form
@app.route('/students/filter', methods=['GET', 'POST'])
def filter_students():
    if request.method == 'POST':
        class_id = request.form.get('class_id')
        section_id = request.form.get('section_id')
        return redirect(url_for('students_by_class', class_id=class_id, section_id=section_id))
    
    classes = Class.query.all()
    return render_template('filter_students.html', classes=classes)

if __name__ == '__main__':
    app.run(debug=True)