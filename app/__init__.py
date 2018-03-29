from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app, name='resume', template_mode='bootstrap3')

from app import routes, models

admin.add_view(ModelView(models.School, db.session))
admin.add_view(ModelView(models.Education, db.session))
admin.add_view(ModelView(models.Company, db.session))
admin.add_view(ModelView(models.Employment, db.session))
admin.add_view(ModelView(models.Project, db.session))
admin.add_view(ModelView(models.Technology, db.session))
admin.add_view(ModelView(models.Contact, db.session))
admin.add_view(ModelView(models.Skill, db.session))
