import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import json
import urllib3

class CusisClient:
    username = ''
    password = ''
    session = None
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    formInput = {}
    courseQueryAPI = 'https://cusis.cuhk.edu.hk/psc/csprd/EMPLOYEE/HRMS/c/CU_SCR_MENU.CU_TMSR801.GBL'

    def __init__(self):
        self.username = os.getenv("STUDENT_ID")
        self.password = os.getenv("PASSWORD")
        self.session = requests.session()
        self.session.headers.update(self.header)

    def login(self):
        url = 'https://cusis.cuhk.edu.hk/psp/csprd/?cmd=login'
        data = {
            'userid': self.username,
            'pwd': self.password
        }
        response = self.session.post(url, data=data, verify=False)

        if 'tab=DEFAULT' in response.text:
            print('Logged in')
            return True
        else:
            print('Login failed')
            print(response.text)
            return False

    def logout(self):
        url = 'https://cusis.cuhk.edu.hk/psp/csprd/EMPLOYEE/HRMS/?cmd=logout'
        self.session.get(url)

    def isLoggedIn(self):
        pass


    def getAcademicCareer(self):
        key = ['code', 'name']
        data = {}
        
        response = self.query(self.courseQueryAPI, data)
        return self.parseSelect(response, key, 'CLASS_SRCH_WRK2_ACAD_CAREER')

    def getAcademicYear(self):
        key = ['code', 'name']
        data = {}
        
        response = self.query(self.courseQueryAPI, data)
        return self.parseSelect(response, key, 'CLASS_SRCH_WRK2_STRM$50$')
        
    def getFacultyList(self):
        key = ['code', 'name']
        data = {
            'ICAction': 'CU_RC_TMSR801_SUBJECT$prompt',
        }
        self.query(self.courseQueryAPI, data)
        data = {
            'ICAction': '#ICViewAll',
        }
        response = self.query(self.courseQueryAPI, data)
        result = self.parseTable(response, key)
        self.resetQuery()
        return result

    def getCourseList(self, career, semester, subject):
        key = ['code', 'id', 'title', 'unit', 'staff', 'quota', 'vacancy', 'type', 'session', 'language', 'period', 'room', 'date', 'addConsent', 'dropConsent', 'department']
        data = {
            'ICAction':'CU_RC_TMSR801_SSR_PB_CLASS_SRCH',
            'CLASS_SRCH_WRK2_ACAD_CAREER': career,
            'CLASS_SRCH_WRK2_STRM$50$': semester,
            'CU_RC_TMSR801_SUBJECT': subject,
        }
        response = self.query(self.courseQueryAPI, data)
        result = self.parseTable(response, key)
        self.newQuery()
        return result

    def query(self, url, data):
        data = {**self.formInput, **data}
        print(data)
        response = self.session.post(url, data=data, verify=False)
        self.updateFormData(response)
        return response

    def initQuery(self):
        self.query(self.courseQueryAPI, {})
    
    def resetQuery(self):
        data = {
            'ICAction': '#ICCancel'
        }
        self.query(self.courseQueryAPI, data)

    def newQuery(self):
        data = {
            'ICAction': 'CU_RC_TMSR801_SSR_PB_NEW_SEARCH'
        }
        self.query(self.courseQueryAPI, data)

    def updateFormData(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        inputList = soup.find_all('input', attrs={'type': 'hidden'})
        self.formInput = dict(map(lambda input: (input.get('name'), input.get('value')), inputList))

    def parseTable(self, response, key):
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all('tr')
        result = [[column.text.strip() for column in row.select('td[class $= "ROW"]')] for row in data]
        return [dict(zip(key, row)) for row in result if len(row) > 0]
    
    def parseSelect(self, response, key, name):
        soup = BeautifulSoup(response.text)
        data = soup.find('select', attrs={'name': name}).find_all('option')
        result = [[row.get('value'), row.text.strip()] for row in data if row.get('value')]
        return [dict(zip(key, row)) for row in result]

if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    load_dotenv()
    client = CusisClient()
    if client.login():
        client.initQuery()
        facultyList = client.getFacultyList()
        print(facultyList)
        courseList = client.getCourseList('UG', 2110, 'ACCT')
        print(courseList)
        courseList = client.getCourseList('UG', 2110, 'MATH')
        print(courseList)
        '''
        with open('faculty.json', 'w') as outfile:
            json.dump(facultyList, outfile)
        for faculty in facultyList:
            with open('%s.json' % faculty['code'], 'w') as outfile:
                courseList = client.getCourseList('UG', 2110, faculty['code'])
                json.dump(facultyList, outfile)
                break
        '''
        client.logout()