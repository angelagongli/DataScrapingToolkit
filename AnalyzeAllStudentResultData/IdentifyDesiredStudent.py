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

student_id = 1

pull_studentinformation = ("SELECT cohort, firstName, middleName, lastName, "
                            "city, state, country FROM Students WHERE id=%s")

pull_allresultsforstudent = ("SELECT id, resultName "
                            "FROM StudentResults WHERE student_id=%s")

pull_allresultsforstudentatstep = ("SELECT id, resultName, resultAge, resultCity, resultCityHistory "
                                    "FROM StudentResults WHERE student_id=%s AND identificationStep=%s")

update_studentresultidentificationstep = ("UPDATE StudentResults SET identificationStep=%s WHERE id=%s")

outerCursor.execute(pull_studentinformation, student_id)

for (cohort, firstName, middleName, lastName, city, state, country) in outerCursor:
    desiredStudentAge = datetime.datetime.now().year - cohort + 22
    firstName = firstName
    middleName = middleName
    lastName = lastName
    city = city

outerCursor.execute(pull_allresultsforstudent, student_id)

for (id, resultName) in outerCursor:
    if (firstName in resultName.upper() and
        lastName in resultName.upper()):
        innerCursor.execute(update_studentresultidentificationstep, ('First Pass', id))
        cnx.commit()

outerCursor.execute(pull_allresultsforstudentatstep, (student_id, 'First Pass'))

for (id, resultName, resultAge, resultCity, resultCityHistory) in outerCursor:
    if (middleName in resultName.upper() or
        f" {middleName[0:1]} " in resultName.upper()):
        innerCursor.execute(update_studentresultidentificationstep, ('Refined', id))
        cnx.commit()
    elif (resultAge >= desiredStudentAge - 1 and
       resultAge <= desiredStudentAge + 1):
        innerCursor.execute(update_studentresultidentificationstep, ('Refined', id))
        cnx.commit()
    elif city in resultCityHistory.upper():
        innerCursor.execute(update_studentresultidentificationstep, ('Refined', id))
        cnx.commit()

outerCursor.execute(pull_allresultsforstudentatstep, (student_id, 'Refined'))

for (id, resultName, resultAge, resultCity, resultCityHistory) in outerCursor:
    if ((middleName in resultName.upper() or
        f" {middleName[0:1]} " in resultName.upper()) and
        (resultAge >= desiredStudentAge - 1 and
        resultAge <= desiredStudentAge + 1) and
        city in resultCityHistory.upper()):
        innerCursor.execute(update_studentresultidentificationstep, ('Identified', id))
        cnx.commit()
        break

innerCursor.close()
outerCursor.close()
cnx.close()
