import mysql.connector
from mysql.connector import errorcode

cnx = mysql.connector.connect(user='root',
                                password=None,
                                host='127.0.0.1',
                                database='Student_DB')
cursor = cnx.cursor()

DB_NAME = 'Student_DB'
TABLES = {}

# Straight from Menaka's dataset of individual commencement program Excel files,
# Only reading in data from commencement programs reporting major because Menaka is
# Studying the relationship between major choice and political belief
TABLES['Students'] = (
    "CREATE TABLE `Students` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `school` varchar(100) NOT NULL,"
    "  `cohort` int NOT NULL,"
    "  `firstName` varchar(100) NOT NULL,"
    "  `middleName` varchar(100),"
    "  `lastName` varchar(100) NOT NULL,"
    "  `major` varchar(100) NOT NULL,"
    "  `city` varchar(100),"
    "  `state` varchar(100),"
    "  `country` varchar(100),"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

# We will be able to quickly retrieve all of the Student's information entered into the URL
# Returning the StudentResult per Menaka's request by doing inner join with the Student
# Table on student_id
TABLES['StudentResults'] = (
    "CREATE TABLE `StudentResults` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `student_id` int NOT NULL,"
    "  `resultName` varchar(100) NOT NULL,"
    "  `resultAge` int,"
    "  `resultCity` varchar(100),"
    "  `resultCityHistory` varchar(100),"
    "  `resultType` enum('StudentVoterRecord','StudentRelatives') NOT NULL,"
    "  `resultData` varchar(200) NOT NULL,"
    "  `identificationStep` enum('Not Identified','First Pass','Refined','Identified') NOT NULL DEFAULT 'Not Identified',"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`student_id`)"
    "     REFERENCES `Students`(`id`)"
    "     ON DELETE CASCADE"
    ") ENGINE=InnoDB")

# We will be able to quickly retrieve all of the Student's information entered into the URL
# Returning the StudentResult in turn returning the StudentRelativeResult per Menaka's request
# By doing inner join with the Student table on student_id
TABLES['StudentRelativeResults'] = (
    "CREATE TABLE `StudentRelativeResults` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `student_id` int NOT NULL,"
    "  `relativeResultName` varchar(100) NOT NULL,"
    "  `relativeResultAge` int,"
    "  `relativeResultCity` varchar(100),"
    "  `relativeResultGender` varchar(100),"
    "  `relativeResultRace` varchar(100),"
    "  `relativeResultVoterRecordURL` varchar(100) NOT NULL,"
    "  `relativeResultSource` enum('StudentVoterRecord','StudentRelatives') NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`student_id`)"
    "     REFERENCES `Students`(`id`)"
    "     ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['VoterRecords'] = (
    "CREATE TABLE `VoterRecords` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `student_id` int NOT NULL,"
    "  `studentRelative_id` int,"
    "  `partyAffiliation` varchar(100),"
    "  `registeredToVoteIn` varchar(100),"
    "  `registrationDate` date,"
    "  `voterStatus` varchar(100),"
    "  `statusReason` varchar(100),"
    "  `precinct` varchar(100),"
    "  `precinctSplit` varchar(100),"
    "  `ward` varchar(100),"
    "  `congressionalDistrict` varchar(100),"
    "  `houseDistrict` varchar(100),"
    "  `senateDistrict` varchar(100),"
    "  `countyDistrict` varchar(100),"
    "  `schoolBoardDistrict` varchar(100),"
    "  `voterRecordType` enum('StudentVoterRecord','StudentRelativeVoterRecord') NOT NULL,"
    "  PRIMARY KEY (`id`),"
    "  FOREIGN KEY (`student_id`)"
    "     REFERENCES `Students`(`id`)"
    "     ON DELETE CASCADE,"
    "  FOREIGN KEY (`studentRelative_id`)"
    "     REFERENCES `StudentRelativeResults`(`id`)"
    "     ON DELETE CASCADE"
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
