# Menaka's dataset is constructed from the individual commencement programs of
# All schools within her set of schools mostly from 2004-2020 but actually going back
# All the way to 1996 => Vast variation within her dataset of data fields reported,
# Naming/coding of the data fields, capitalization/casing, abbreviation, completeness etc.
# Among schools and even among years within a school because of the peacemeal way
# Menaka is saving/cleaning her data at the time she receives/scrapes it and preserving
# All of the data she can that is contained in the commencement program.

# We can read in every file for our analysis of student major choice/political belief and
# Clean it up ad hoc at the time, but ideally Menaka's dataset will be fully normalized and
# Loaded into DB all in one table. We can streamline the composite key into one primary key
# (ID integer) and then efficiently relate the Student DB table to the rest of Menaka's data:
# Student's Credit Report/Debt, Student's Household's Assets/Liabilities, Student's Occupational
# Choice, Student's/Student's Relative's Voter Registration Data etc. => TODO: Implement

import mysql.connector
from mysql.connector import errorcode

cnx = mysql.connector.connect(user='root',
                                password=None,
                                host='127.0.0.1',
                                database='Student_DB')
cursor = cnx.cursor()

DB_NAME = 'Student_DB'
TABLES = {}
TABLES['Students'] = (
    "CREATE TABLE `Students` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `school` varchar(100) NOT NULL,"
    "  `cohort` int NOT NULL,"
    "  `firstname` varchar(100) NOT NULL,"
    "  `middlename` varchar(100) NOT NULL,"
    "  `lastname` varchar(100) NOT NULL,"
    # ...
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table exists")
        else:
            print(err.msg)
    else:
        print("Table created")

cursor.close()
cnx.close()
