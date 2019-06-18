import os

import pdfkit
from flask import make_response, render_template

from app import app
from app.models import (Company, Contact, Education, Employment, Project,
                        School, Skill, Technology)

TEMPLATE_DIR = "app/templates/resume_templates"


@app.route("/")
@app.route("/index")
def index():
    templates = [
        os.path.splitext(file)[0]
        for file in os.listdir(TEMPLATE_DIR)
        if file.endswith(".html")
    ]
    return render_template("index.html", templates=templates)


def get_template(template_name=None, **kwargs):
    filename = "{}/{}.html".format(TEMPLATE_DIR, template_name)
    education_records = Education.query.order_by("end_date")
    companies = Company.query.all()
    projects = Project.query.all()
    employments = Employment.query.order_by("start_date")
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
        "include_css": True,
        "template_name": template_name,
        "download_mode": False,
    }
    context.update(kwargs)
    if os.path.exists(filename):
        template_name = "resume_templates/{}.html".format(template_name)
        return render_template(template_name, **context)
    return ""


@app.route("/template/<string:template_name>")
def template(template_name):
    return get_template(template_name=template_name)


@app.route("/template/<string:template_name>/download")
def download(template_name):
    padding = 0.4
    wkhtml_options = {
        "margin-top": "{}in".format(padding),
        "margin-right": "{}in".format(padding),
        "margin-bottom": "{}in".format(padding),
        "margin-left": "{}in".format(padding),
        "encoding": "UTF-8",
        "no-outline": None,
        "page-size": "A4",
        "dpi": 400,
    }
    static_dir = os.path.join(os.path.abspath(os.path.dirname(".")), "app", "static")
    css = [
        "/css/{}.css".format(template_name),
        "/css/{}-fonts.css".format(template_name),
        "/css/font-awesome.min.css",
        "/css/bootstrap.min.css",
        "/css/print.css",
    ]
    css = ["{}{}".format(static_dir, link) for link in css]
    template = get_template(
        template_name=template_name, include_css=False, download_mode=True
    )
    filename = "resume_{}.pdf".format(template_name)
    pdf = pdfkit.from_string(template, False, options=wkhtml_options, css=css)
    response = make_response(pdf)
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    response.mimetype = "application/pdf"
    return response
