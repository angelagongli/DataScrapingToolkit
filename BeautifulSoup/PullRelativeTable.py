from bs4 import BeautifulSoup
from bs4.element import NavigableString

with open("C:\\Users\\angel\\GitHub\\DataScrapingToolkit\\HTML\\Menaka_Hampole.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

for link in soup.find_all('a', string="That's The One!"):
    for relative in link.parent.find_previous_sibling().contents:
        if isinstance(relative, NavigableString):
            print(relative.strip())
