from app import db


class Contact(db.Model):
    """ Information about you
    """

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    mobile_number = db.Column(db.String(15), nullable=True)
    email_address = db.Column(db.String(255), nullable=True)
    linked_in_url = db.Column(db.String(255), nullable=True)
    linked_in_username = db.Column(db.String(255), nullable=True)
    github_url = db.Column(db.String(255), nullable=True)
    github_username = db.Column(db.String(255), nullable=True)
    skype_url = db.Column(db.String(255), nullable=True)
    skype_username = db.Column(db.String(255), nullable=True)
    pinterest_url = db.Column(db.String(255), nullable=True)
    pinterest_username = db.Column(db.String(255), nullable=True)
    twitter_url = db.Column(db.String(255), nullable=True)
    twitter_username = db.Column(db.String(255), nullable=True)
    address = db.Column(db.Text, nullable=True)
    profile = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return self.full_name

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)


class Skill(db.Model):
    """ A technical skill you have
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    importance = db.Column(db.Integer, default=0)


class School(db.Model):
    """ The school or institution attended
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    education_records = db.relationship("Education", backref="school", lazy=True)

    def __repr__(self):
        return self.name


class Education(db.Model):
    """ A record of the programme done at the school
    """

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    school_id = db.Column(db.Integer, db.ForeignKey("school.id"), nullable=True)
    program_name = db.Column(db.String(255), nullable=True)


class Company(db.Model):
    """ A company you worked at
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    employments = db.relationship("Employment", backref="company", lazy=True)

    def __repr__(self):
        return self.name


class Employment(db.Model):
    """ A period of employment at a company
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    achievements = db.Column(db.Text, nullable=True)
    overview = db.Column(db.Text, nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    projects = db.relationship(
        "Project", backref="employment", lazy=True, order_by="-Project.start_date"
    )

    def __repr__(self):
        return f"{self.title}, {self.company.name}"

    @property
    def achievement_listing(self):
        """ Returns a list of achievements
        """
        if not self.achievements:
            return []
        return self.achievements.split("\n")


technologies = db.Table(
    "project_technologies",
    db.Column(
        "technology_id", db.Integer, db.ForeignKey("technology.id"), primary_key=True
    ),
    db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True),
)
project_frameworks = db.Table(
    "project_frameworks",
    db.Column(
        "framework_id", db.Integer, db.ForeignKey("framework.id"), primary_key=True
    ),
    db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True),
)


class Project(db.Model):
    """ A project you did while at a place of employment
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    employment_id = db.Column(db.Integer, db.ForeignKey("employment.id"), nullable=True)
    summary = db.Column(db.Text)
    technologies = db.relationship(
        "Technology",
        secondary=technologies,
        lazy="subquery",
        backref=db.backref("projects", lazy=True),
    )
    frameworks = db.relationship(
        "Framework",
        secondary=project_frameworks,
        lazy="subquery",
        backref=db.backref("projects", lazy=True),
    )
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return self.name

    @property
    def frameworks_by_technology(self):
        result = []
        all_technologies = []
        all_frameworks = []
        for framework in self.frameworks:
            all_frameworks.append(framework)
            technology = framework.technology
            assert technology, f"Technology for {framework} should not be None"
            if technology not in all_technologies:
                all_technologies.append(technology)

        for technology in all_technologies:
            frameworks = ", ".join(
                [
                    framework.name
                    for framework in all_frameworks
                    if framework.technology.id == technology.id
                ]
            )
            result.append({"technology": technology, "frameworks": frameworks})
        return result


class Framework(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    technology_id = db.Column(db.Integer, db.ForeignKey("technology.id"))

    def __repr__(self):
        return self.name


class Technology(db.Model):
    """ A technology that was used to execute on the project
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    icon = db.Column(db.String(255), nullable=True)
    frameworks = db.relationship("Framework", backref="technology")

    def __repr__(self):
        framework_names = ", ".join([framework.name for framework in self.frameworks])
        if framework_names:
            return f"{self.name} ({framework_names})"
        return self.name

    @property
    def icon_url(self):
        base_url = "/static/img/%s.png"
        icons = {
            "python": "python",
            "ruby": "ruby",
            "android": "mobile",
            "javascript": "javascript",
            ".net": "microsoft",
            "php": "php",
            "html": "browser",
            "database": "database",
        }
        icon = icons.get(self.name.lower())
        return (base_url % icon) if icon else None
