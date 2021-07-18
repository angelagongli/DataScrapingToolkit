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
    year = firstStudent.cohort if hasattr(firstStudent, "cohort") else firstStudent.cohort_yr
    print(f"Now Processing {firstStudent.school} in {year}...")
    Students = []
    for student in df.itertuples(name='Student'):
      if (pd.isna(student.school) or not student.school.strip() or
        (pd.isna(student.cohort) if hasattr(student, "cohort") else
        pd.isna(student.cohort_yr)) or
        pd.isna(student.firstname) or not student.firstname.strip() or
        pd.isna(student.lastname) or not student.lastname.strip() or
        pd.isna(student.major) or not student.major.strip()):
        continue
      if (pd.isna(student.middlename) or not student.middlename.strip()):
        middleName = None
      else:
        middleName = student.middlename.upper().strip()
      if (hasattr(student, "city") and not pd.isna(student.city) and student.city.strip()):
        city = student.city.upper().strip()
      else:
        city = None
      if (hasattr(student, "state") and not pd.isna(student.state) and student.state.strip()):
        if student.state.upper().strip() in US_StateAbbreviationLookUp.keys():
          state = US_StateAbbreviationLookUp[student.state.upper().strip()]
        else:
          state = student.state.upper().strip()
      else:
        state = None
      if (hasattr(student, "country") and not pd.isna(student.country) and student.country.strip()):
        country = student.country.upper().strip()
      else:
        country = None
      Student = {
        'school': student.school.upper().strip(),
        'cohort': student.cohort if hasattr(student, "cohort") else student.cohort_yr,
        'firstName': student.firstname.upper().strip(),
        'middleName': middleName,
        'lastName': student.lastname.upper().strip(),
        'major': student.major.upper().strip(),
        'city': city,
        'state': state,
        'country': country
      }
      Students.append(Student)
    cursor.executemany(add_student, Students)
    cnx.commit()
    print(f"Upload of {firstStudent.school} in {year} complete!")

cursor.close()
cnx.close()
