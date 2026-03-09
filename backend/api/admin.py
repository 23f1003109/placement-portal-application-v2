from flask import Blueprint, request
from flask_login import login_required
from ..models import Student, Company, Drive, Application
from ..extensions import db

admin_bp = Blueprint("admin", __name__)

from functools import wraps
from flask_login import current_user
from flask import abort


def bool_parser(value):
    if value is None:
        return None
    return value.lower() in {"true", "yes", "1"}


def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)

            if current_user.role.name != role:
                abort(403)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def serialize_company(company):
    return {
        "id": company.id,
        "name": company.name,
        "industry": company.industry,
        "hr_name": company.hr_name,
        "hr_email": company.hr_email,
        "hr_contact": company.hr_contact,
        "description": company.description,
        "location": company.location,
        "website": company.website,
        "is_approved": company.is_approved,
        "is_blacklisted": company.is_blacklisted,
        "user_id": company.user_id,
    }


def serialize_student(student):
    return {
        "id": student.id,
        "name": student.name,
        "department": student.department,
        "degree": student.degree,
        "contact_number": student.contact_number,
        "is_blacklisted": student.is_blacklisted,
        "user_id": student.user_id,
    }


def serialize_drive(drive):
    return {
        "id": drive.id,
        "company_id": drive.company_id,
        "company_name": drive.company.name if drive.company else None,
        "name": drive.name,
        "job_title": drive.job_title,
        "job_description": drive.job_description,
        "job_location": drive.job_location,
        "eligibility_criteria": drive.eligibility_criteria,
        "application_deadline": drive.application_deadline.isoformat() if drive.application_deadline else None,
        "salary": drive.salary,
        "is_completed": drive.is_completed,
    }


def serialize_application(application):
    return {
        "id": application.id,
        "student_id": application.student_id,
        "student_name": application.student.name if application.student else None,
        "drive_id": application.drive_id,
        "drive_name": application.drive.name if application.drive else None,
        "company_id": application.company.id if application.company else None,
        "company_name": application.company.name if application.company else None,
        "application_date": application.application_date.isoformat() if application.application_date else None,
        "status": application.status,
        "resume_link": application.resume_link,
    }


@admin_bp.route("/dashboard")
@login_required
@role_required("admin")
def dashboard():

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = Drive.query.count()
    total_applications = Application.query.count()

    return {
        "students": total_students,
        "companies": total_companies,
        "drives": total_drives,
        "applications": total_applications
    }


@admin_bp.route("/companies/<int:company_id>")
@login_required
@role_required("admin")
def get_company(company_id):
    company = Company.query.get_or_404(company_id)
    return serialize_company(company)


@admin_bp.route("/companies")
@login_required
@role_required("admin")
def list_companies():
    query = Company.query
    args = request.args
    name = args.get("name")
    industry = args.get("industry")
    company_id = args.get("company_id")
    is_approved = args.get("is_approved")
    is_blacklisted = args.get("is_blacklisted")

    if name:
        query = query.filter(Company.name.ilike(f'%{name}%'))
    if industry:
        query = query.filter(Company.industry.ilike(f'%{industry}%'))

    if company_id:
        try:
            cid = int(company_id)
            query = query.filter(Company.id == cid)
        except ValueError:
            pass
    if is_approved is not None:
        is_approved = bool_parser(is_approved)
        query = query.filter(Company.is_approved == is_approved)
    if is_blacklisted is not None:
        is_blacklisted = bool_parser(is_blacklisted)
        query = query.filter(Company.is_blacklisted == is_blacklisted)
    companies = query.all()

    return [serialize_company(company) for company in companies]


@admin_bp.route('/students/<int:student_id>')
@login_required
@role_required("admin")
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return serialize_student(student)


@admin_bp.route('/students')
@login_required
@role_required("admin")
def list_students():
    query = Student.query
    args = request.args
    name = args.get("name")
    student_id = args.get("student_id")
    contact_number = args.get("contact_number")
    is_blacklisted = args.get("is_blacklisted")

    if name:
        query = query.filter(Student.name.ilike(f'%{name}%'))
    if student_id:
        try:
            sid = int(student_id)
            query = query.filter(Student.id == sid)
        except ValueError:
            pass
    if contact_number:
        query = query.filter(Student.contact_number.ilike(f'%{contact_number}%'))

    if is_blacklisted is not None:
        query = query.filter(Student.is_blacklisted == bool_parser(is_blacklisted))

    students = query.all()
    return [serialize_student(student) for student in students]


@admin_bp.route('/drives/<int:drive_id>')
@login_required
@role_required("admin")
def get_drive(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    return serialize_drive(drive)


@admin_bp.route('/drives')
@login_required
@role_required("admin")
def list_drives():
    query = Drive.query
    args = request.args
    is_completed = args.get("is_completed")
    drive_id = args.get("drive_id")
    company_id = args.get("company_id")
    name = args.get("name")

    if is_completed is not None:
        query = query.filter(Drive.is_completed == bool_parser(is_completed))

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

    drives = query.all()

    return [serialize_drive(drive) for drive in drives]


@admin_bp.route('/applications/<int:application_id>')
@login_required
@role_required("admin")
def get_application(application_id):
    application = Application.query.get_or_404(application_id)
    return serialize_application(application)


@admin_bp.route('/applications')
@login_required
@role_required("admin")
def list_applications():
    query = Application.query
    args = request.args
    student_id = args.get("student_id")
    drive_id = args.get("drive_id")
    status = args.get("status")

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
        query = query.filter(Application.status.ilike(f"%{status}%"))

    applications = query.all()

    return [serialize_application(application) for application in applications]


@admin_bp.route('/students/<int:student_id>/toggle-blacklist', methods=['POST'])
@login_required
@role_required("admin")
def toggle_student(student_id):
    student = Student.query.get_or_404(student_id)
    student.is_blacklisted = not student.is_blacklisted
    db.session.commit()
    return {"success": True}


@admin_bp.route('/companies/<int:company_id>/toggle-blacklist', methods=['POST'])
@login_required
@role_required("admin")
def toggle_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.is_blacklisted = not company.is_blacklisted
    db.session.commit()
    return {"success": True}


@admin_bp.route('/companies/<int:company_id>/approve', methods=['POST'])
@login_required
@role_required("admin")
def approve_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.is_approved = True
    db.session.commit()
    return {"success": True}


@admin_bp.route('/drives/<int:drive_id>/complete', methods=['POST'])
@login_required
@role_required("admin")
def complete_drive(drive_id):
    drive = Drive.query.get_or_404(drive_id)
    drive.is_completed = True
    db.session.commit()
    return {"success": True}


@admin_bp.route('/seed', methods=['POST'])
@login_required
@role_required("admin")
def seed():
    from .seed import seed_database
    seed_database()
    return {"message": "Database seeding completed"}
