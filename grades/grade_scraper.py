import datetime, re
from bs4 import BeautifulSoup
import execjs
import requests
from . import Session
from .models import Department, Course, Distribution
from .dept_scraper import get_department

def scrape_grades(session):
    """Populate the database with courses and grade distributions."""
    semester, year = sem_and_year()
    course_id = 1
    # keep increasing the course_id until there are no more courses to be explored
    while True:
        course = get_course_by_id(course_id, session)
        if course is None:
            url_fmt = "https://schedulebuilder.berkeley.edu/explore/courses/{0}/{1}/{2}"
            url = url_fmt.format(semester, year, course_id)
            req = requests.get(url)
            if req.status_code != 200:
                break
            else:
                process_course_page(req.text, course_id, session)
        course_id += 1

def process_course_page(txt, course_id, session):
    """Adds the course's grade distribution to the database, if applicable.
    Takes as input a string of the course page's HTML."""
    soup = BeautifulSoup(txt)
    lines = soup.find(id = 'tab-grades').find_all('script')[1].get_text().splitlines()
    jstext = '\n'.join(filter(lambda line: line.find("google") == -1, lines))
    distributions = execjs.compile(jstext).eval("grade_distributions")

    if len(distributions) > 0:
        info = distributions[0]['section']['offering']['course']
        dept_name = info['department']['name']
        number = info['identifier']
        div = division(number)
        if div is not None:
            dept = get_department(dept_name, session)
            if dept is not None:
                course = Course(id = course_id, department = dept,
                                number = number, division = div)
                session.add(course)
                data = total_distribution(distributions)
                # there has to be a better way to do this
                distro = Distribution(course = course,
                                      a_plus = data['a_plus'],
                                      a = data['a'],
                                      a_minus = data['a_minus'],
                                      b_plus = data['b_plus'],
                                      b = data['b'],
                                      b_minus = data['b_minus'],
                                      c_plus = data['c_plus'],
                                      c = data['c'],
                                      c_minus = data['c_minus'],
                                      d_plus = data['d_plus'],
                                      d = data['d'],
                                      d_minus = data['d_minus'],
                                      f = data['f'])
                session.add(distro)
                print dept_name, number

def total_distribution(distributions):
    """Given a set of grade distributions, returns the sum of them."""
    data = {}
    grade_names = []
    for letter in 'abcd':
        for suffix in ['_plus', '', '_minus']:
            data[letter + suffix] = 0
            grade_names.append(letter + suffix)
    data['f'] = 0
    grade_names.append('f')
    for distro in distributions:
        for grade_name in grade_names:
            data[grade_name] += distro[grade_name]
    return data

def get_course_by_id(course_id, session):
    """Returns the course with id COURSE_ID, if it exists, and None if it
    doesn't exist."""
    query = session.query(Course).filter_by(id = course_id)
    if query.count() > 0:
        return query.first()
    else:
        return None

def get_course(dept, number, session):
    """Returns the course with the department and number specified, if it
    exists, and None if it doesn't exist."""
    query = session.query(Course).filter_by(department = dept, number = number)
    if query.count() > 0:
        return query.first()
    else:
        return None

def sem_and_year():
    """Gets the semester and year to use.
        January-April: Spring of this year
        April-October: Fall of this year
        November-December: Spring of next year
    """
    today = datetime.date.today()
    if today.month > 4 and today.month < 11:
        semester = "FL"
        year = today.year
    else:
        semester = "SP"
        if today.month < 4:
            year = today.year
        else:
            year = today.year + 1
    return semester, year

def division(number):
    """Gets the division of the class by its number."""
    match = re.search("[0-9]+", number)
    if match:
        num = int(match.group(0))
        if num < 100:
            return "lower"
        elif num < 200:
            return "upper"
        elif num < 300:
            return "graduate"
        else:
            return "other"
    else:
        return None

def run():
    session = Session()
    try:
        scrape_grades(session)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
