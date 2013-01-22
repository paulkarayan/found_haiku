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

# 1) retrive text from URL
# 2) parse into sentences / sentence fragments, then into words
# 3) count the syllables in each word & sentence. save 5 or 7 syllable ones.
# 4) put sentences that have 5 or 7 syllables together
# 5) print out haiku
# 6) ?
# 7) profit

#dict of sentences and their syllable counts
worddict = {}






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

def parsesentences(wordlist):
# through the glory of regex, break apart the sentence
# see http://stackoverflow.com/questions/367155/splitting-a-string-into-words-and-punctuation

#to do: need to count for each sentance! despite what this says, i think
# that wordlist 

  for sentence in wordlist:
    #sentence is the unicode string, unbroken  
    print(sentence, '<-sentence variable')
    words = re.findall(r"[\w']+|[.,!?;]", "%s" % str(sentence))
    #words is the list of unicode strings in a sentence 
    print(words)
    syllablecounter = 0
    sensyllablecounter = 0
    for word in words:
      #print(str(word))
      syllablecounter = countsyllables(str(word))
      sensyllablecounter += syllablecounter
      print(sensyllablecounter)


    if sensyllablecounter == 5:
      worddict[str(sentence)] = sensyllablecounter
    elif sensyllablecounter == 7:
      worddict[str(sentence)] = sensyllablecounter
    else:
      print('%s is not a good match!' % sensyllablecounter)

  return(worddict)


def visible(element):
  if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
    return False
  elif re.match('<!--.*-->', str(element)):
    return False
  return True

  


def removeblanks(element):
  if element == '\n':
    return False
  else:
    return True



def pulldownurltext(url):

  #retrieve visible text from an url based on:
  #http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text

  #test for now:
  #url = 'http://www.paulkarayan.com'

  html = urllib.urlopen(url).read()
  soup = BeautifulSoup(html)
  texts = soup.findAll(text=True)
  visible_texts = filter(visible, texts)
  wordlist = filter(removeblanks, visible_texts)       
  # return a list of visible text with u'content', and new lines removed
  return(wordlist)


def main(url):
  
  returnedwl = pulldownurltext(url)
  print('I\'ve got a word list!')
  print(parsesentences(returnedwl))



if __name__ == '__main__':
    try:
        
        # eventually:  
        url = sys.argv[1]
        
        #but for now:
        #sentence = sys.argv[1]
       

    except:
        print usage
        sys.exit(-1)


    main(url)
