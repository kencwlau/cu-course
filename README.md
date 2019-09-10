# CUHK Course
This is a Python 3 script for fetching the faculty list and the course list from CUSIS.

## Usage
The script requires an .env file at the root of the repository and the sample .env file is as follow.
```text
STUDENT_ID=1155000000
PASSWORD=
```

The following command install all dependencies of the script.
```bash
pip install python-dotenv requests2 bs4
```

Execute the following command to execute the script.
```bash
python ./main.py
```

## Anatomy
The `CusisClient` handles all HTTP requests to the CUSIS webpage. The public methods are as follows.

### login
Login into CUSIS database.

### logout
Log out CUSIS database.

### query
Query the given URL with data by HTTP POST method.

### initQuery
Initialize query by entering the home page of CUSIS.

### resetQuery
Back to the home page of the CUSIS.

### newQuery
Start a new query when the current query finish.

### parseTable
Parse the CUSIS table and export data in JSON format with the given key lists.

### parseSelect
Parse the CUSIS select input and export options in JSON format with the given key lists.

### getAcademicCareer
Get all available academic career in CUHK.

### getAcademicYear
Get all available semester codes in current academic year.

### getFacultyList
Get all faculty code and name in CUHK.

### getCourseList
Get all courses with given career, semester code and faculty code.