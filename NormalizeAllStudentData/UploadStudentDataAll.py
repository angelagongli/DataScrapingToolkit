import pandas as pd
import os
import mysql.connector

cnx = mysql.connector.connect(user='root',
                              password=None,
                              host='127.0.0.1',
                              database='Student_DB')
cursor = cnx.cursor()

US_StateAbbreviationLookUp = {
  'ALABAMA': 'AL',
  'ALASKA': 'AK',
  'AMERICAN SAMOA': 'AS',
  'ARIZONA': 'AZ',
  'ARKANSAS': 'AR',
  'CALIFORNIA': 'CA',
  'COLORADO': 'CO',
  'CONNECTICUT': 'CT',
  'DELAWARE': 'DE',
  'DISTRICT OF COLUMBIA': 'DC',
  'FLORIDA': 'FL',
  'GEORGIA': 'GA',
  'GUAM': 'GU',
  'HAWAII': 'HI',
  'IDAHO': 'ID',
  'ILLINOIS': 'IL',
  'INDIANA': 'IN',
  'IOWA': 'IA',
  'KANSAS': 'KS',
  'KENTUCKY': 'KY',
  'LOUISIANA': 'LA',
  'MAINE': 'ME',
  'MARYLAND': 'MD',
  'MASSACHUSETTS': 'MA',
  'MICHIGAN': 'MI',
  'MINNESOTA': 'MN',
  'MISSISSIPPI': 'MS',
  'MISSOURI': 'MO',
  'MONTANA': 'MT',
  'NEBRASKA': 'NE',
  'NEVADA': 'NV',
  'NEW HAMPSHIRE': 'NH',
  'NEW JERSEY': 'NJ',
  'NEW MEXICO': 'NM',
  'NEW YORK': 'NY',
  'NORTH CAROLINA': 'NC',
  'NORTH DAKOTA': 'ND',
  'NORTHERN MARIANA ISLANDS':'MP',
  'OHIO': 'OH',
  'OKLAHOMA': 'OK',
  'OREGON': 'OR',
  'PENNSYLVANIA': 'PA',
  'PUERTO RICO': 'PR',
  'RHODE ISLAND': 'RI',
  'SOUTH CAROLINA': 'SC',
  'SOUTH DAKOTA': 'SD',
  'TENNESSEE': 'TN',
  'TEXAS': 'TX',
  'UTAH': 'UT',
  'VERMONT': 'VT',
  'VIRGIN ISLANDS': 'VI',
  'VIRGINIA': 'VA',
  'WASHINGTON': 'WA',
  'WEST VIRGINIA': 'WV',
  'WISCONSIN': 'WI',
  'WYOMING': 'WY'
}

add_student = ("INSERT INTO Students "
               "(school, cohort, firstName, middleName, lastName, major, city, state, country) "
               "VALUES (%(school)s, %(cohort)s, %(firstName)s, %(middleName)s, %(lastName)s, %(major)s, %(city)s, %(state)s, %(country)s)")

root = 'C:\\Users\\angel\\Documents\\Automation\\Web_Scraping\\Commencement Program Lists'
for file in os.listdir(root):
  fullFilePath = os.path.join(root, file)
  if os.path.isfile(fullFilePath):
    df = pd.read_excel(fullFilePath)
    firstStudent = df.iloc[0]
    if not hasattr(firstStudent, "major"):
      continue
    print(f"Now Processing {firstStudent.school}...")
    Students = []
    for student in df.itertuples(name='Student'):
      if (pd.isna(student.school) or (pd.isna(student.cohort)
        if hasattr(student, "cohort") else pd.isna(student.cohort_yr)) or
        pd.isna(student.firstname) or pd.isna(student.lastname) or
        pd.isna(student.major)):
        continue
      Student = {
        'school': student.school.upper().strip(),
        'cohort': student.cohort if hasattr(student, "cohort") else student.cohort_yr,
        'firstName': student.firstname.upper().strip(),
        'middleName': student.middlename.upper().strip() if not pd.isna(student.middlename) else None,
        'lastName': student.lastname.upper().strip(),
        'major': student.major.upper().strip(),
        'city': (student.city.upper().strip() if not pd.isna(student.city) else None)
          if hasattr(student, "city") else None,
        'state': ((US_StateAbbreviationLookUp[student.state.upper().strip()]
          if student.state.upper().strip() in US_StateAbbreviationLookUp.keys()
          else student.state.upper().strip())
          if not pd.isna(student.state) else None)
          if hasattr(student, "state") else None,
        'country': (student.country.upper().strip()
          if not pd.isna(student.country) else None)
          if hasattr(student, "country") else None
      }
      Students.append(Student)
    cursor.executemany(add_student, Students)

cnx.commit()

cursor.close()
cnx.close()
