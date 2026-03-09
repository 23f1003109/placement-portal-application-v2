from functools import wraps
from flask_login import current_user
from flask import abort


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

def bool_parser(value):
    if value is None:
        return None
    return value.lower() in {"true", "yes", "1"}




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