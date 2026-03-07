from flask import Blueprint
from flask_login import login_required, current_user
from ..models import User, Student, Company, Drive, Application

admin_bp = Blueprint("admin", __name__)

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

@admin_bp.route("/companies")
@login_required
@role_required("admin")
def list_companies():

    companies = Company.query.all()

    return [
        {
            "id": company.id,
            "name": company.name,
            "industry": company.industry,
            "hr_name": company.hr_name,
            "hr_email": company.hr_email,
            "hr_contact": company.hr_contact,
            "is_approved": company.is_approved,
            "is_blacklisted": company.is_blacklisted
        }
        for company in companies
    ]