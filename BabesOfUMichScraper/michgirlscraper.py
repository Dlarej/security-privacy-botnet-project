import urllib
from BeautifulSoup import BeautifulSoup
import sys


if (len(sys.argv) != 2):
    print 'Usage: <url>'
with open (sys.argv[1], "r") as myFile:
    htmlSource = myFile.read()


parsed_html = BeautifulSoup(htmlSource)

spans = parsed_html.body.findAll('span',attrs={'class':'heading-comments'})

for span in spans:
    a = span.find('a', href=True)
    with open('umichgirls.txt', 'a') as f:
        f.write('http://54.165.104.227/redirect.php?link=' + a['href'] + '\n')
