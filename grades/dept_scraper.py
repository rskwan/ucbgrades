import re
import requests
from bs4 import BeautifulSoup
from . import Session
from .models import Department 

def scrape_departments(session):
    sburl = 'https://schedulebuilder.berkeley.edu/explore/'
    r = requests.get(sburl)
    soup = BeautifulSoup(r.text)
    for ulist in soup.find_all(id = re.compile("^deptlist")):
        for entry in ulist.find_all('li'):
            parts = entry.a.string.split(" (")
            if get_department(parts[0], session) is None:
                dept = Department(name = parts[0], code = parts[1][:-1])
                session.add(dept)

def get_department(name, session):
    query = session.query(Department).filter_by(name=name)
    if query.count() > 0:
        return query.first()
    else:
        return None

def run():
    session = Session()
    try:
        scrape_departments(session)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
