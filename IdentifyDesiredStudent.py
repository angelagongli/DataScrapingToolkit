# We want to come to only one StudentResult for every student in Menaka's dataset,
# => Narrow the set of StudentResult based on exact First Name and Last Name as well as
# Middle Name/Middle Initial, Expected Age and City where we can

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
        firstStudent = Student_DF.iloc[0]
        if hasattr(firstStudent, "cohort"):
            desiredStudentAge = datetime.datetime.now().year - firstStudent.cohort + 22
        elif hasattr(firstStudent, "cohort_yr"):
            desiredStudentAge = datetime.datetime.now().year - firstStudent.cohort_yr + 22
        for Student in Student_DF.itertuples(name='Student'):
            # School and Cohort are implicit in the subset of Menaka's whole dataset
            # Being analyzed in the one file here => Student Number is sufficient/
            # All that is required in addition to School and Cohort for us to be
            # Able to uniquely identify the Student
            AllResultOfStudent_DF = StudentResult_DF[StudentResult_DF['student_no'] == Student.student_no]
            if hasattr(Student, "city"):
                desiredStudentCity = Student.city
            FirstPassStudentResults = []
            for StudentResult in AllResultOfStudent_DF.itertuples(name='StudentResult'):
                if (StudentResult.firstname.upper() in StudentResult.resultName.upper() and
                    StudentResult.lastname.upper() in StudentResult.resultName.upper()):
                    FirstPassStudentResults.append(StudentResult)
            if len(FirstPassStudentResults) > 1:
                RefinedStudentResults = []
                for StudentResult in FirstPassStudentResults:
                    if (StudentResult.middlename.upper() in StudentResult.resultName.upper() or
                        f" {StudentResult.middlename[0:1].upper()} " in StudentResult.resultName.upper()):
                        RefinedStudentResults.append(StudentResult)
                    if (StudentResult.resultAge >= desiredStudentAge - 1 and
                        StudentResult.resultAge <= desiredStudentAge + 1):
                        RefinedStudentResults.append(StudentResult)
                    if desiredStudentCity.upper() in StudentResult.resultCityHistory.upper():
                        RefinedStudentResults.append(StudentResult)
                if len(RefinedStudentResults) > 1:
                    for StudentResult in RefinedStudentResults:
                        if ((StudentResult.middlename.upper() in StudentResult.resultName.upper() or
                            f" {StudentResult.middlename[0:1].upper()} " in StudentResult.resultName.upper()) and
                            (StudentResult.resultAge >= desiredStudentAge - 1 and
                            StudentResult.resultAge <= desiredStudentAge + 1) and
                            desiredStudentCity.upper() in StudentResult.resultCityHistory.upper()):
                            IdentifiedStudentResults.append(StudentResult)
                            break
                elif len(RefinedStudentResults) == 1:
                    IdentifiedStudentResults.append(RefinedStudentResults[0])
            elif len(FirstPassStudentResults) == 1:
                IdentifiedStudentResults.append(FirstPassStudentResults[0])
        IdentifiedStudent_DF = pd.DataFrame(data=IdentifiedStudentResults)
        with pd.ExcelWriter(os.path.join(root, 'StudentResults', file),
                            mode='a') as writer:
            IdentifiedStudent_DF.to_excel(writer, sheet_name='IdentifiedStudentResults')
        # Keep all data required to uniquely identify the student the relative belongs to in
        # Whole dataset in the IdentifiedStudentRelative, as well as all of the student's information
        # Entered into the URL returning the StudentResult per Menaka's request
        IdentifiedStudentRelative = collections.namedtuple('IdentifiedStudentRelative',
            ['student_no', 'firstname', 'middlename', 'lastname',
            'school', 'cohort', 'studentRelativeFirstName', 'studentRelativeMiddleName',
            'studentRelativeLastName'])
        IdentifiedStudentRelatives = []
        for StudentResult in IdentifiedStudent_DF.itertuples(name='StudentResult'):
            if StudentResult.resultType == 'Relatives':
                IdentifiedStudentRelativeArr = StudentResult.resultData.split("*")
                for StudentRelativeName in IdentifiedStudentRelativeArr:
                    StudentRelativeNameArr = StudentRelativeName.split(" ")
                    if len(StudentRelativeNameArr) == 2:
                        studentRelativeFirstName = StudentRelativeNameArr[0]
                        studentRelativeLastName = StudentRelativeNameArr[1]
                    elif len(StudentRelativeNameArr) == 3:
                        studentRelativeFirstName = StudentRelativeNameArr[0]
                        studentRelativeMiddleName = StudentRelativeNameArr[1]
                        studentRelativeLastName = StudentRelativeNameArr[2]
                    elif len(StudentRelativeNameArr) > 3:
                        studentRelativeFirstName = StudentRelativeNameArr[0]
                        studentRelativeMiddleName = StudentRelativeNameArr[1]
                        for namePiece in StudentRelativeNameArr[2:-1]:
                            studentRelativeMiddleName = studentRelativeMiddleName + namePiece
                        studentRelativeLastName = StudentRelativeNameArr[-1]
                    identifiedStudentRelative = IdentifiedStudentRelative(StudentResult.student_no,
                        StudentResult.firstname, StudentResult.middlename, StudentResult.lastname,
                        StudentResult.school, StudentResult.cohort, studentRelativeFirstName,
                        studentRelativeMiddleName, studentRelativeLastName)
                    IdentifiedStudentRelatives.append(identifiedStudentRelative)
        IdentifiedStudentRelative_DF = pd.DataFrame(data=IdentifiedStudentRelatives)
        with pd.ExcelWriter(os.path.join(root, 'StudentResults', file),
                            mode='a') as writer:
            IdentifiedStudentRelative_DF.to_excel(writer, sheet_name='IdentifiedStudentRelatives')
