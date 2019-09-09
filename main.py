import requests
from bs4 import BeautifulSoup




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
            return True
        else:
            print('login')
            print(response.text)
            return False

    def logout(self):
        pass


    def isLoggedIn(self):
        pass

    def initQuery(self):
        self.query(self.courseQueryAPI, {})

    def getAcademicYear(self):
        data = {
            'ICAction': '#ICCancel',
        }


        response = self.query(self.courseQueryAPI, data)
        print(response.text)

    def getFacultyList(self):
        data = {
            'ICAction': 'CU_RC_TMSR801_SUBJECT$prompt',
        }
        self.query(self.courseQueryAPI, data)
        data = {
            'ICAction': '#ICViewAll',
        }
        response = self.query(self.courseQueryAPI, data)
        soup = BeautifulSoup(response.text)
        data = soup.find_all('tr')[3:]
        getColumnContent = lambda column: column
        getRowContent = lambda row: list(map(getColumnContent, row))
        
        print(list(map(getRowContent, data)))

        print('Fac List')
        # print(response.text)

    def getCourseList(self):
        data = {
            'ICAction':'CU_RC_TMSR801_SSR_PB_CLASS_SRCH',
            'CLASS_SRCH_WRK2_ACAD_CAREER':'UG',
            'CLASS_SRCH_WRK2_STRM$50$': 2110,
            'CU_RC_TMSR801_SUBJECT': 'ACCT'
        }
        response = self.query(self.courseQueryAPI, data)
        print('Course List')
        print(response.text)

    def query(self, url, data):
        data = {**self.formInput, **data}
        response = self.session.post(url, data=data, verify=False)
        self.updateFormData(response)
        return response

    def updateFormData(self, response):
        soup = BeautifulSoup(response.text)
        inputList = soup.find_all('input', attrs={'type': 'hidden'})
        self.formInput = dict(map(lambda input: (input.get('name'), input.get('value')), inputList))

if __name__ == '__main__':
    client = CusisClient()

    if client.login():
        client.initQuery()
        client.getFacultyList()
        
