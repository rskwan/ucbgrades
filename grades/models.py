from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from . import engine

Base = declarative_base()

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Department: {0} ({1})>".format(self.name, self.code)

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    number = Column(String)
    division = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", backref=backref("courses", order_by=id))

    def __str__(self):
        return "{0} {1}".format(self.department, self.number)

    def __repr__(self):
        return "<Course: {0} {1}>".format(self.department, self.number)

class Distribution(Base):
    __tablename__ = "distributions"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", backref=backref("distributions", order_by=id))

    a_plus = Column(Integer)
    a = Column(Integer)
    a_minus = Column(Integer)
    b_plus = Column(Integer)
    b = Column(Integer)
    b_minus = Column(Integer)
    c_plus = Column(Integer)
    c = Column(Integer)
    c_minus = Column(Integer)
    d_plus = Column(Integer)
    d = Column(Integer)
    d_minus = Column(Integer)
    f = Column(Integer)

    def __repr__(self):
        return "<Distribution: {0}>".format(self.course)

    def grades_as_list(self):
        return [self.a_plus, self.a, self.a_minus,
                self.b_plus, self.b, self.b_minus,
                self.c_plus, self.c, self.c_minus,
                self.d_plus, self.d, self.d_minus, self.f]

Base.metadata.create_all(engine)
