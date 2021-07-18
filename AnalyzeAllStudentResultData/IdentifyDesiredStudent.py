# We want to come to only one StudentResult for every student in Menaka's dataset,
# => Narrow the set of StudentResult based on exact First Name and Last Name as well as
# Middle Name/Middle Initial, Expected Age and City where we can

import datetime
import mysql.connector

cnx = mysql.connector.connect(user='root',
                              password=None,
                              host='127.0.0.1',
                              database='Student_DB')
outerCursor = cnx.cursor(buffered=True)
innerCursor = cnx.cursor(buffered=True)

pull_studentinformation = ("SELECT cohort, firstName, middleName, lastName, "
                            "city, state, country FROM Students WHERE id=%(student_id)s")

pull_allresultsforstudentatstep = ("SELECT id, resultName, resultAge, resultCity, resultCityHistory "
                                    "FROM StudentResults WHERE student_id=%(student_id)s AND identificationStep=%(identificationStep)s")

update_studentresultidentificationstep = ("UPDATE StudentResults SET identificationStep=%s WHERE id=%s")

for i in range(1, 100):
    student_data = {
        'student_id': i,
        'identificationStep': 'Not Identified'
    }

    outerCursor.execute(pull_studentinformation, student_data)

    for (cohort, firstName, middleName, lastName, city, state, country) in outerCursor:
        desiredStudentAge = datetime.datetime.now().year - cohort + 22
        firstName = firstName
        middleName = middleName
        lastName = lastName
        city = city

    outerCursor.execute(pull_allresultsforstudentatstep, student_data)

    for (id, resultName, resultAge, resultCity, resultCityHistory) in outerCursor:
        if (firstName in resultName.upper() and
            lastName in resultName.upper()):
            innerCursor.execute(update_studentresultidentificationstep, ('First Pass', id))
            cnx.commit()

    student_data['identificationStep'] = 'First Pass'
    outerCursor.execute(pull_allresultsforstudentatstep, student_data)

    for (id, resultName, resultAge, resultCity, resultCityHistory) in outerCursor:
        if middleName and (middleName in resultName.upper() or
            f" {middleName[0:1]} " in resultName.upper()):
            innerCursor.execute(update_studentresultidentificationstep, ('Refined', id))
            cnx.commit()
        elif resultAge and (resultAge >= desiredStudentAge - 1 and
            resultAge <= desiredStudentAge + 1):
            innerCursor.execute(update_studentresultidentificationstep, ('Refined', id))
            cnx.commit()
        elif city and city in resultCityHistory.upper():
            innerCursor.execute(update_studentresultidentificationstep, ('Refined', id))
            cnx.commit()

    student_data['identificationStep'] = 'Refined'
    outerCursor.execute(pull_allresultsforstudentatstep, student_data)

    for (id, resultName, resultAge, resultCity, resultCityHistory) in outerCursor:
        if ((middleName and (middleName in resultName.upper() or
            f" {middleName[0:1]} " in resultName.upper())) and
            (resultAge and (resultAge >= desiredStudentAge - 1 and
            resultAge <= desiredStudentAge + 1)) and
            (city and city in resultCityHistory.upper())):
            innerCursor.execute(update_studentresultidentificationstep, ('Identified', id))
            cnx.commit()
            break

innerCursor.close()
outerCursor.close()
cnx.close()
