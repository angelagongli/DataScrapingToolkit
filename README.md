# Student/Student Relative Voter Registration Data Scraping from voterrecords.com

## Summary Up to 7/24/2021

### Menakas Suggested Process
1. Search all students in every commencement program from every school/year in the dataset
   1. If the student returns no voter records, scrape the list of students/student's relatives returned by TruthFinder on voterrecords.com in lieu of student voter record results
   1. If the student returns one or more voter records, scrape the first page of student voter record results returned
1. Narrow the results returned by TruthFinder/voterrecords.com to just one Student for every student in the commencement program dataset according to the rule of a yet to be determined algorithm
1. For all student voter records returned by voterrecords.com and then identified by our process, go to the Student's Voter Record page and scrape all of the student's voter registration data as well as the student's Related Records designated by voterrecords.com
1. For all students/student's relatives returned by TruthFinder and then identified by our process, repeat the whole cycle for the student's relatives, only continuing in our data scraping process when the student's relative does return a voter record


### In Progress Implementation
* Initial implementation doing file I/O directly from the commencement program Excel workbooks themselves and then writing to a series of Excel sheets for every step in the data scraping/identification process in succession
* More streamlined implementation reading from/writing to MySQL Database making the iterative identification process much more self-contained within related DB tables in the DB


## To Be Resolved If Continuing On

To Be Resolved if Menaka is interested in pursuing the student/student relative voter registration data scraping project in spite of the following issue/blocker list:

* Voterrecords.com only lists the voter records of 19 states
* Voterrecords.com explicitly states that Related Records on its site are simply public records with similar data and makes no guarantee that the Related Records are really relatives by blood/marriage => Unclear how Menaka is going to make sure the Related Records listed on the Student's Voter Record/return from TruthFinder are really the Student's Relatives
* Unclear how Menaka if planning to identify the Student's Relative from all of the voter records returned from searching on the Student's Relative's name when the Student's Relative's name is all we have to go on, trusting that the Student's Relative's name is even accurate
* Unclear how the Student's Relative's Voter Record can be helpful for Menaka in the situation when we do not have the Student's own Voter Record
* The site's search functionality is not consistent, and Menaka's suggested process of using more data points in the search wherever available does not always lead to more accurate results
* This is not really my concern as the main task at hand is to first construct the student/student relative voter registration dataset, but at the most fundamental level of thinking about how to answer the research question, how is Menaka hoping to analyze the relationship between the Student's major choice and political belief based on such a broad indicator as Party Affiliation (the only data point on voterrecords.com that is really related to political belief) and additionally analyze the Student's Relatives' political belief with such tenuous inference interference on the Student's Relatives based solely on the site's own designation when A we have not yet come up with a way to infer political belief from just the voter registration data on voterrecords.com and B it is not yet clear that the data on voterrecords.com is reliable?


## Notes from Menaka on 7/31/2021

* When the Student returns voter records, scrape all of the voter records returned *before* the narrowing/identification process => All of the voter registration data we pull for the Student from voterrecords.com will be helpful for Menaka to identify the Student once we put everything together with Menaka's address data she has scraped from BeenVerified
* When the Student returns results from TruthFinder:
  * If the Student returns only one result from TruthFinder, save the one result's Student/Student's Relatives and repeat the whole cycle for all of the one result's designated list of relatives returned by TruthFinder
  * If the Student returns more than one result from TruthFinder, save only the list of Student/Student's Relatives returned by TruthFinder and hold on before repeating the whole cycle so we can return to the identification of the Student/the whole process for the Student's Relatives once we do have the Student's Voter Record from Menaka's co-author's voter registration data gathering process if the Student does come up in the requested dataset
* Party Affiliation is the only data point Menaka thinks we need to be able to study the student's political belief, but Menaka still wants us to scrape all of the detailed voter registration data e.g. Registration Date, House District/Senate District contained in the Student's Voter Record on voterrecords.com
* 9/19/2021 notes Menaka to ask her co-author an her developer about voter records or BeenVerified address data of students in different states and I will then try to help her narrow down the voter registration/TruthFinder data and restrict the data scraping procedure to only the set of states on voterrecords.com accordingly

## Guide to Building the Student/Student Relative Voter Registration Dataset for Yourself

### Background
* Our starting point for building our Student/Student Relative Voter Registration dataset is Menaka's commencement program data gathered from all of the individual schools in her dataset
* We have just a couple of tools in our toolkit:
  * [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/) and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) are our way of navigating voterrecords.com and then finding all of the data we want to scrape from the site
  * We house all of our student/student relative voter registration data in one place, i.e. our [MySQL](https://dev.mysql.com/) database
  * [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/) is our way of bridging the divide between our normalization/data scraping process from voterrecords.com and our DB for storing our data
  * [MySQL Workbench](https://dev.mysql.com/doc/workbench/en/) is helpful GUI for MySQL
* We are pulling new voter registration data from [voterrecords.com](voterrecords.com) for all of the students in Menaka's commencement program dataset as well as their relatives to add back to Menaka's original student dataset
* Our hope is that we can accurately and cleanly organize all of our student/student relative data starting from Menaka's commencement program data that we are reading in at the beginning to our voter registration data that we are scraping from voterrecords.com and then all the way through our entire process of identifying the student from our scraped data


### What do all of our files do?
Only the following files in the repository will be helpful for you in building our Student/Student Relative Voter Registration dataset, the rest is my brainstorming/from my earlier draft:
* `NormalizeAllStudentData\CreateTableAll.py`:
  * Generates the DB schema
  * You should first create **Student_DB** in your local MySQL instance!
* `NormalizeAllStudentData\UploadStudentDataAll.py`:
  * Normalizes and uploads all of the student data from Menaka's individual commencement program Excel files to our **Student_DB.Students** table
* `WebDriver\ScrapeStudentResultDataAll.py`
  * We navigate voterrecords.com searching for all of the students in our dataset one by one, entering the student's full name, city and state and saving their resulting data in our **Student_DB.StudentResults** table:
    * When the student does not return voter records on voterrecords.com, the data we save is the student's list of relatives returned by TruthFinder
    * When the student does return 1+ voter record on voterrecords.com, the data we save is the first page of the student's voter records on voterrecords.com
* `AnalyzeAllStudentResultData\IdentifyDesiredStudent.py`:
  * We narrow down our saved data for every student in our dataset one by one based on the student's name, expected age, city and state
  * Per Menaka, we will need to narrow down/identify the student by hand as well so we want to be saving all the data we can from voterrecords.com in order to have the most complete information possible for our manual process
  * And then it grabs the list of TruthFinder results stored in an asterisk delimited string in the identified student's record and parses the names to construct querystrings for searching for voter record results to inserting **Student_DB.StudentRelativeResults**
* `BeautifulSoup\PullVoterRecordDataAll.py`:
  * For all of the students in our dataset who do return a voter record, we save all of the student's first page of voter records returned under the student's name, city and state on voterrecords.com into our **Student_DB.VoterRecords** table


### Reference

* [Helpful guide on Selenium WebDriver configuration for web data scraping](https://blog.m157q.tw/posts/2020/09/11/bypass-cloudflare-detection-while-using-selenium-with-chromedriver/) from Menaka

* Should email Menaka that as much as I would love to keep helping her on the data scraping project I think the circumstance of the website's voter record data or lack thereof is prohibitively difficult and Menaka should start thinking about a solution/approach that is more in reach than scraping a free website or the particular free website we have been looking at. She can even put her time and energy toward helping her co-author request state government voter record data if she doesn't come up with a new data source herself. No one's fault but IMO it will be far better for all of us to be realistic and circumspect early on than blindly optimistic now and disappointed later when the website's data doesn't magically improve esp. keeping in mind her co-author's expectation if they were really counting on the data and thinking about what bad news deliver late could mean for her co-author
