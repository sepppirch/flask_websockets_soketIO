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
    exists = False

    for x in nl:
        if int(x['id']) == int(text):
            print("already exists")
            exists = True
        
    """Return a meme name and url from a meme keywords.
    """
    if exists == False:

        url = 'http://knowyourmeme.com/memes/' + str(text)
        #print(url)
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        valid = soup.find('title')
        print("name: " + str(valid))


                


        if str(valid) == '<title>Page Not Found (404) - Know Your Meme</title>':
            print("404")
        else:
            

            x =  '{"name":"x", "id":-1, "tags":[],"links":[]}'


            #nl = []
            #with open('nodelist.txt', 'r+') as f:
                #nl = json.load(f)

            y = json.loads(x)
            kids = []
            tags = []
            #f = open("nodelist.txt", "a")
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


            
            if soup.find('a', text='View Related Entries'):
            #print(children_url)

                children_url = "https://knowyourmeme.com/" + soup.find('a', text='View Related Entries').get("href")
                kids = kym_children(children_url)

            y["id"] = id
            y["tags"] = tags
            y["links"] = kids
            y["name"] = valid.getText()
            #print(nl)
            nl.append(y)
        
            with open('nodelist.txt', 'w') as f:
                json.dump(nl, f)
            #f.write(str(y))
            #f.close()

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
                

nl = []
todo = [38850, 38601, 38577, 37024, 36009, 33967, 33893, 33702, 33081, 32889, 32416, 31855, 31779, 30877, 30634, 30332]

with open('nodelist.txt', 'r+') as f:
    nl = json.load(f)

print(str(len(nl)))
print(type(nl))

#for i in todo:
for i in range(8,100):

    kym_id(i)