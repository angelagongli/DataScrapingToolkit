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
