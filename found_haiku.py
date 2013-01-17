# http://stackoverflow.com/questions/10414957/using-python-to-find-syllables
# is where i got the bulk of this from

import urllib
from BeautifulSoup import BeautifulSoup
import re
import sys


usage = """
Usage:
python found_haiku.py <URL> 

Example:
python found_haiku.py http://www.paulkarayan.com

"""
# todo:
# 1) retrive text from URL
# 2) parse into sentences / sentence fragments, then into words
# 3) count the syllables in each word & sentence
# 4) put sentences that have 5 or 7 syllables together
# 5) print out haiku
# 6) ?
# 7) profit

#dict of sentences and their syllable counts
worddict = {}


def main(sentence):
	#just a dummy so i can run from command line
	print(parsesentences(sentence))

def parsesentences(sentence):
# through the glory of regex, break apart the sentence
# see http://stackoverflow.com/questions/367155/splitting-a-string-into-words-and-punctuation
	
	wordlist = re.findall(r"[\w']+|[.,!?;]", "%s" % sentence)
	syllablecounter = 0

	for word in wordlist:
		print(word)
		syllablecounter += countsyllables(word)

		print(syllablecounter)

	if syllablecounter == 5:
		worddict[sentence] = syllablecounter
	elif syllablecounter == 7:
		worddict[sentence] = syllablecounter
	else:
		print(syllablecounter, ' is not a good match!')

	return(worddict)

def countsyllables(word):

	name="text"
	name="optionSyllableCount"
	name="optionWordCount"


	url = 'http://www.wordcalc.com/index.php'
	post_data = urllib.urlencode(
    	{'text': '%s' % word}) 
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

	return(syllable_count)


if __name__ == '__main__':
    try:
        
        # eventually:  
        #url = sys.argv[1]
        
        #but for now:
        sentence = sys.argv[1]
       

    except:
        print usage
        sys.exit(-1)

#this will change to url
    main(sentence)