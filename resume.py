from app import app, db
from app.models import (
    School, Education, Company, Employment,
    Project, Technology
)


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'School': School,
        'Education': Education,
        'Company': Company,
        'Employment': Employment,
        'Project': Project,
        'Technology': Technology,
    }
