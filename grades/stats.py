import csv
from operator import add, mul
from . import Session
from .models import Department, Course, Distribution

def get_dept_avgs(session):
    """Return a list of tuples, each consisting of the department name,
    the lower division average, the upper division average, and the total
    average."""
    avgs = []
    overall_counts = [[0 for _ in range(13)] for _ in range(3)]
    for dept in session.query(Department).order_by(Department.id):
        lower_counts = sum_distributions(dept, session, "lower")
        upper_counts = sum_distributions(dept, session, "upper")
        ug_counts = map(add, lower_counts, upper_counts)
        all_counts = [lower_counts, upper_counts, ug_counts]
        overall_counts = map(lambda x, y: map(add, x, y),
                             all_counts, overall_counts)
        all_sums = map(sum, all_counts)
        all_avgs = map(compute_avg, all_counts)
        if any(all_avgs):
            combined = reduce(add, [[all_sums[i], all_avgs[i]] for i in range(3)])
            avgs.append(tuple([dept.name, dept.code] + combined))
    overall_sums = map(sum, overall_counts)
    overall_avgs = map(compute_avg, overall_counts)
    combined = reduce(add, [[overall_sums[i], overall_avgs[i]] for i in range(3)])
    avgs.append(tuple(['Overall', 'ALL'] + combined))
    return avgs

def sum_distributions(dept, session, div = None):
    """Returns a list of grade counts for DEPT, with division determined by
    DIV -- by default, we sum all grades, but we can filter by division if
    given. The list is indexed as follows:
        0 : A+
        1 : A
        2 : A-
        ...
        10: D
        11: D-
        12: F
    """
    if div is None:
        courses = session.query(Course).filter_by(department = dept) 
    else:
        courses = session.query(Course).filter_by(department = dept,
                                                  division = div)
    total = [0 for _ in range(13)]
    for course in courses:
        for distro in session.query(Distribution).filter_by(course = course):
            total = map(add, total, distro.grades_as_list())
    return total

def compute_avg(counts):
    """Given a list of grade counts, returns the average GPA if there are any
    counts, and 0 otherwise."""
    if sum(counts) > 0:
        weights = [4.0, 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0]
        return sum(map(mul, weights, counts)) / sum(counts)
    else:
        return 0

def write_to_csv(avgs):
    f = open('dept_avgs.csv', 'wb')
    writer = csv.writer(f)
    writer.writerow(['Department', 'Code',
                     'Lower Division Grades', 'Lower Division Average',
                     'Upper Division Grades', 'Upper Division Average',
                     'Undergraduate Grades', 'Undergraduate Average'])
    for tup in avgs:
        writer.writerow(tup)
    f.close()

def run():
    session = Session()
    try:
        write_to_csv(get_dept_avgs(session))
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
