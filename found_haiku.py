# http://stackoverflow.com/questions/10414957/using-python-to-find-syllables
# is where i got the bulk of this from

import urllib
from BeautifulSoup import BeautifulSoup

name="text"
name="optionSyllableCount"
name="optionWordCount"


url = 'http://www.wordcalc.com/index.php'
post_data = urllib.urlencode(
    {'text': 'virginia'}) 
post_data = '%s&optionSyllableCount&optionWordCount' % post_data

cnxn = urllib.urlopen(url, post_data)
response = cnxn.read()
cnxn.close()

soup = BeautifulSoup(response)
h3_matches = [h3 for h3 in soup.findAll('h3') if h3.text == 'Statistics']
if len(h3_matches) != 1:
  raise Exception('Wrong number of <h3>Statistics</h3>')
h3_match = h3_matches[0]
table = h3_match.findNextSibling('table')

td_matches = [td for td in table.findAll('td')
              if td.text == 'Syllable Count']
if len(td_matches) != 1:
  raise Exception('Wrong number of <td>Syllable Count</td>')
td_match = td_matches[0]

td_value = td_match.findNextSibling('td')
syllable_count = int(td_value.text)

print(syllable_count)
