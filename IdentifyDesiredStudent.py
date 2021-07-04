# We want to come to only one StudentResult for every student in Menaka's dataset

import pandas as pd
import os
import collections
import datetime

root = 'C:\\Users\\angel\\Documents\\Automation\\Web_Scraping\\Commencement Program Lists'

for file in os.listdir(root):
    fullFilePath = os.path.join(root, file)
    fullStudentResultFilePath = os.path.join(root, 'StudentResults', file)
    StudentResult = collections.namedtuple('StudentResult',
        ['student_no', 'firstname', 'middlename', 'lastname',
        'school', 'cohort', 'resultName', 'resultAge',
        'resultCity', 'resultCityHistory', 'resultType', 'resultData'])
    IdentifiedStudentResults = []
    if os.path.isfile(fullFilePath) and os.path.isfile(fullStudentResultFilePath):
        Student_DF = pd.read_excel(fullFilePath)
        StudentResult_DF = pd.read_excel(fullStudentResultFilePath)
        desiredStudentAge = datetime.datetime.now().year - Student_DF.iloc[0].cohort_yr + 22
        for Student in Student_DF.itertuples(name='Student'):
            AllResultOfStudent_DF = StudentResult_DF[StudentResult_DF['firstname'] == Student.firstname]
            for StudentResult in AllResultOfStudent_DF.itertuples(name='StudentResult'):
                if (StudentResult.resultAge >= desiredStudentAge - 1 and StudentResult.resultAge <= desiredStudentAge + 1):
                    IdentifiedStudentResults.append(StudentResult)
        IdentifiedStudent_DF = pd.DataFrame(data=IdentifiedStudentResults)
        with pd.ExcelWriter(os.path.join(root, 'StudentResults', file),
                            mode='a') as writer:
            IdentifiedStudent_DF.to_excel(writer, sheet_name='IdentifiedStudentResults')
