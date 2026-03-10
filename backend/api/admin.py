from flask import Blueprint, request
from flask_login import login_required

from ..extensions import db
from ..helperFunctions import bool_parser, role_required, serialize_application, serialize_company, serialize_drive, serialize_student
from ..models import Application, Company, Drive, Student


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/companies/<int:company_id>')
@login_required
@role_required('admin')
def get_company(company_id):
    company = Company.query.get_or_404(company_id)
    return serialize_company(company)


@admin_bp.route('/companies')
@login_required
@role_required('admin')
def list_companies():
    query = Company.query
    args = request.args
    name = args.get('name')
    industry = args.get('industry')
    company_id = args.get('company_id')
    is_approved = args.get('is_approved')
    is_blacklisted = args.get('is_blacklisted')

    if name:
        query = query.filter(Company.name.ilike(f'%{name}%'))
    if industry:
        query = query.filter(Company.industry.ilike(f'%{industry}%'))
    if company_id:
        try:
            query = query.filter(Company.id == int(company_id))
        except ValueError:
            pass
    if is_approved is not None:
        query = query.filter(Company.is_approved == bool_parser(is_approved))
    if is_blacklisted is not None:
        query = query.filter(Company.is_blacklisted == bool_parser(is_blacklisted))

    companies = query.order_by(Company.id.asc()).all()
    return [serialize_company(company) for company in companies]


@admin_bp.route('/students/<int:student_id>')
@login_required
@role_required('admin')
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return serialize_student(student)


@admin_bp.route('/students')
@login_required
@role_required('admin')
def list_students():
    query = Student.query
    args = request.args
    name = args.get('name')
    student_id = args.get('student_id')
    contact_number = args.get('contact_number')
    is_blacklisted = args.get('is_blacklisted')

    if name:
        query = query.filter(Student.name.ilike(f'%{name}%'))
    if student_id:
        try:
            query = query.filter(Student.id == int(student_id))
        except ValueError:
            pass
    if contact_number:
        query = query.filter(Student.contact_number.ilike(f'%{contact_number}%'))
    if is_blacklisted is not None:
        query = query.filter(Student.is_blacklisted == bool_parser(is_blacklisted))

    students = query.order_by(Student.id.asc()).all()
    return [serialize_student(student) for student in students]


@admin_bp.route('/drives/<int:drive_id>')
@login_required
@role_required('admin')
def get_drive(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    return serialize_drive(drive)


@admin_bp.route('/drives')
@login_required
@role_required('admin')
def list_drives():
    query = Drive.query
    args = request.args
    is_completed = args.get('is_completed')
    is_approved = args.get('is_approved')
    drive_id = args.get('drive_id')
    company_id = args.get('company_id')
    name = args.get('name')

    if is_completed is not None:
        query = query.filter(Drive.is_completed == bool_parser(is_completed))
    if is_approved is not None:
        query = query.filter(Drive.is_approved == bool_parser(is_approved))
    if drive_id:
        try:
            query = query.filter(Drive.id == int(drive_id))
        except ValueError:
            pass
    if company_id:
        try:
            query = query.filter(Drive.company_id == int(company_id))
        except ValueError:
            pass
    if name:
        query = query.filter(Drive.name.ilike(f'%{name}%'))

    drives = query.order_by(Drive.id.asc()).all()
    return [serialize_drive(drive) for drive in drives]


@admin_bp.route('/applications/<int:application_id>')
@login_required
@role_required('admin')
def get_application(application_id):
    application = Application.query.get_or_404(application_id)
    return serialize_application(application)


@admin_bp.route('/applications')
@login_required
@role_required('admin')
def list_applications():
    query = Application.query
    args = request.args
    student_id = args.get('student_id')
    drive_id = args.get('drive_id')
    status = args.get('status')

    if student_id:
        try:
            query = query.filter(Application.student_id == int(student_id))
        except ValueError:
            pass
    if drive_id:
        try:
            query = query.filter(Application.drive_id == int(drive_id))
        except ValueError:
            pass
    if status:
        query = query.filter(Application.status.ilike(f'%{status}%'))

    applications = query.order_by(Application.id.asc()).all()
    return [serialize_application(application) for application in applications]


@admin_bp.route('/students/<int:student_id>/toggle-blacklist', methods=['POST'])
@login_required
@role_required('admin')
def toggle_student(student_id):
    student = Student.query.get_or_404(student_id)
    student.is_blacklisted = not student.is_blacklisted
    db.session.commit()
    return {'success': True, 'student': serialize_student(student)}


@admin_bp.route('/companies/<int:company_id>/toggle-blacklist', methods=['POST'])
@login_required
@role_required('admin')
def toggle_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.is_blacklisted = not company.is_blacklisted
    db.session.commit()
    return {'success': True, 'company': serialize_company(company)}


@admin_bp.route('/companies/<int:company_id>/approve', methods=['POST'])
@login_required
@role_required('admin')
def approve_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.is_approved = True
    db.session.commit()
    return {'success': True, 'company': serialize_company(company)}


@admin_bp.route('/drives/<int:drive_id>/approve', methods=['POST'])
@login_required
@role_required('admin')
def approve_drive(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    drive.is_approved = True
    db.session.commit()
    return {'success': True, 'drive': serialize_drive(drive)}


@admin_bp.route('/drives/<int:drive_id>/toggle-approval', methods=['POST'])
@login_required
@role_required('admin')
def toggle_drive_approval(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    drive.is_approved = not drive.is_approved
    db.session.commit()
    return {'success': True, 'drive': serialize_drive(drive)}


@admin_bp.route('/drives/<int:drive_id>/complete', methods=['POST'])
@login_required
@role_required('admin')
def complete_drive(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    drive.is_completed = True
    db.session.commit()
    return {'success': True, 'drive': serialize_drive(drive)}


@admin_bp.route('/seed', methods=['POST'])
@login_required
@role_required('admin')
def seed():
    from .seed import seed_database

    seed_database()
    return {'message': 'Database seeding completed'}
