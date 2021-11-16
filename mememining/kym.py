import sys
import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import re
import urllib.request
import json


SEARCH_SIMILARITY_THRESHOLD = .1

HEADERS = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')}


def kymSearch(text):
    """Return a meme name and url from a meme keywords.
    """
    r = requests.get('http://knowyourmeme.com/search?q=%s' % text, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    memes_list = soup.find(class_='entry_list')
    for link in memes_list.find_all('a', href=True):
        print(link['href'])

    if memes_list:
        meme_path = memes_list.find_all('href', class_="href")
        print(meme_path)
        return #meme_path.replace('-', ' '), 'https://knowyourmeme.com%s' % meme_path
    return None, None


def kym_id(text):
    """Return a meme name and url from a meme keywords.
    """
    url = 'http://knowyourmeme.com/memes/' + str(text)
    #print(url)
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    valid = soup.find('title')
    print("name: " + str(valid))



    if str(valid) == '<title>Page Not Found (404) - Know Your Meme</title>':
        print("404")
    else:
        x =  '{"name":"x", "id":-1, "tags":[1,2]}'
        y = json.loads(x)
        kids = []
        tags = []
        id = -1

        tag_list = soup.find(class_='tags')
        for link in tag_list.find_all('a', href=True):
            #print(link['href'])
            tags.append(link.get_text())
            #
        

        data = str(soup).splitlines()
        for line in data:
            if line.__contains__('<article class="entry" id='):
                id = int(re.search(r'\d+', line).group())
                print("ID: " + str(id))

        this_url = soup.find('meta', property='og:url').get("content")
        img_url = soup.find('meta', property='og:image').get("content")
        #print(this_url)
        children_url = "https://knowyourmeme.com/" + soup.find('a', text='View Related Entries').get('href')
        #print(children_url)


        kids = kym_children(children_url)

        y["id"] = id
        y["tags"] = tags
        y["links"] = kids
        y["name"] = valid.getText()
        print(y)
        urllib.request.urlretrieve(img_url, str(id) + ".jpg")
        '''with open('./{}.txt'.format(text), "w"  , encoding='utf-8') as file:
            file.write(str(soup))
            file.close
        '''
def kym_children(url):
    
    #print(url)
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    valid = soup.find('title')

    if str(valid) == '<title>Page Not Found (404) - Know Your Meme</title>':
        print("404")
    else:

        kids = []
        data = str(soup).splitlines()
        for line in data:
            if line.__contains__('<table class="entry_list">'):
                #print("Child ID: " + line)
                theline = re.split("( )",line)

                for x in theline:
                    if x.__contains__('class="entry_'):
                        if x.__contains__('list'):
                            
                            print()
                        else:
                            id = int(re.search(r'\d+', x).group())
                            #print("Child ID: " + str(id))
                            kids.append(id)


        return kids       # 
                


kym_id(sys.argv[1])