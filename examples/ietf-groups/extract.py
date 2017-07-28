"""
Grab all mailing list archive URLs from the IETF active groups page.
"""

from bs4 import BeautifulSoup
import urllib2

url = 'https://datatracker.ietf.org/list/wg/'
response = urllib2.urlopen(url)
html = response.read()

soup = BeautifulSoup(html, 'html.parser')
table = soup.body.table

if table:
    for row in table('tr'):
        if row('td'):
            link = row('td')[0].a
            print link.get('href')