import requests
from bs4 import BeautifulSoup

username = ''
password = ''
session = None
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}


def login():
    url = 'https://cusis.cuhk.edu.hk/psp/csprd/?cmd=login'
    data = {
        'userid': username,
        'pwd': password
    }
    response = session.post(url, data=data, verify=False)

    if 'tab=DEFAULT' in response.text:
        return True
    else:
        print('login')
        print(response.text)
        return False


def logout():
    pass


def isLoggedIn():
    pass


def getAcademicYear():
    url = 'https://cusis.cuhk.edu.hk/psc/csprd/EMPLOYEE/HRMS/c/CU_SCR_MENU.CU_TMSR801.GBL'
    data = {
        'ICType': 'Panel',
        'ICAction': '#ICCancel',
    }

    response = session.post(url, data=data, verify=False)
    print(response.text)


def getFacultyList():
    url = 'https://cusis.cuhk.edu.hk/psc/csprd/EMPLOYEE/HRMS/c/CU_SCR_MENU.CU_TMSR801.GBL'
    data = {
        'ICType': 'Panel',
        'ICAction': '#ICAdvSearch',
    }

    response = session.post(url, data=data, verify=False)
    print('Fac List')
    print(response.text)

def getCourseList():
    url = 'https://cusis.cuhk.edu.hk/psc/csprd/EMPLOYEE/HRMS/c/CU_SCR_MENU.CU_TMSR801.GBL'
    data = {
        'ICType': 'Panel',
        'ICAction':'CU_RC_TMSR801_SSR_PB_CLASS_SRCH',
		'CLASS_SRCH_WRK2_ACAD_CAREER':'UG',
		'CLASS_SRCH_WRK2_STRM$50$': 2110,
        'CU_RC_TMSR801_SUBJECT': 'ACCT'
    }

    response = session.post(url, data=data, verify=False)
    print('Course List')
    print(response.text)



if __name__ == '__main__':
    session = requests.session()
    session.headers.update(header)
    if login():
        getCourseList()
