from flask import Blueprint
from flask_login import login_required, current_user

student_bp = Blueprint("student", __name__)