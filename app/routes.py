import os

from flask import render_template

from app import app

from app.models import (
    School, Education, Company, Employment,
    Project, Technology, Contact, Skill
)

TEMPLATE_DIR = "app/templates/resume_templates"


@app.route('/')
@app.route('/index')
def index():
    templates = [
        os.path.splitext(file)[0]
        for file in os.listdir(TEMPLATE_DIR)
        if file.endswith(".html")]
    return render_template("index.html", templates=templates)


@app.route('/template/<string:template_name>')
def template(template_name):
    filename = "{}/{}.html".format(TEMPLATE_DIR, template_name)
    education_records = Education.query.order_by('-end_date')
    companies = Company.query.all()
    projects = Project.query.all()
    employments = Employment.query.order_by('-start_date')
    technologies = Technology.query.all()
    contact = Contact.query.first()
    skills = Skill.query.all()
    context = {
        "companies": companies,
        "projects": projects,
        "education_records": education_records,
        "technologies": technologies,
        "contact": contact,
        "skills": skills,
        "employments": employments,
    }
    if os.path.exists(filename):
        template_name = "resume_templates/{}.html".format(template_name)
        return render_template(template_name, **context)
