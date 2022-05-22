import json
import re
from venv import create
from bs4 import BeautifulSoup
import bs4
import requests
import pandas as pd

url = "https://www.mafteiach.app/all/by_year/5711/"

response = requests.get(url)

htmlContent = response.content

soup = BeautifulSoup(htmlContent, "html.parser")

banned_words = ['share', 'arrow_back', 'videocam', '\n\\', ', ']

month_titles = [] #/
event_titles = [] #/
event_dates = [] #/
event_items = [] 
event_links = [] #/

def formatString(string):
    return ' '.join(i for i in string.split() if i not in banned_words )

def remove_dict_duplicates(list_of_dicts):
    """
    Remove duplicates.
    """
    packed = set(((k, frozenset(v.items())) for elem in list_of_dicts for
                 k, v in elem.items()))
    return [{k: dict(v)} for k, v in packed]


def createListOfUniqueDict(l_list):
    seen = set()
    new_l = l_list
    l_list = []
    for k in new_l:
        d = tuple(k.items())
        if d not in seen:
            seen.add(d)
            l_list.append(k)
    return l_list
#---------------------------------------------------------------------------------------------------------------------

#Get the event dates
for mon in range(1, 13):
    link_list = []
    event_a = []
    event_b = []
    link = []
    a = True
    for event in range(1, 15):
        id_a = "month_" + str(mon) + "A" + "_farbrengen_" + str(event) + "_button"
        id = "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"
        id_b = "month_" + str(mon) + "B" + "_farbrengen_" + str(event) + "_button"
        if (soup.find(id = id_a) == None):
            button = soup.find('button', {"id": id})
            if(button != None):
                link_list.append(button.a.attrs['href'].removeprefix('/').replace('all/', ''))
        elif (soup.find(id = id_a) != None ):
            button_a = soup.find('button', {"id": id_a})
            button_b = soup.find('button', {"id": id_b})
            if(button_a != None):
                event_a.append(button_a.a.attrs['href'].removeprefix('/').replace('all/', ''))
            if(button_b != None):
                event_b.append(button_b.a.attrs['href'].removeprefix('/').replace('all/', ''))
    event_dates.append(event_a)
    event_dates.append(event_b)
    event_dates.append(link_list)



    #     if (soup.find(id='month_' + str(mon) + "A" + "_farbrengen_" + str(event) + "_button")) == None:
    #         toSearch = "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"
    #         button = soup.find('button', {'id': toSearch})
    #         if(button != None):
    #             link = button.a.attrs['href'].removeprefix('/').replace('all/', '')
    #         link_list.append(link)
    #         a = not a
    #     else:   
    #         toSearch = "month_" + str(mon) + "A"+ "_farbrengen_" + str(event) + "_button"
    #         button = soup.find('button', {'id': toSearch})
    #         if(button != None):
    #             link = button.a.attrs['href'].removeprefix('/').replace('all/', '')
    #         link_list.append(link)
    #         a = False
    # event_dates.append(link_list)

event_dates = [x for x in event_dates if x]

# print(len(event_dates))

# for e in event_dates:
#     print((e))
#     print('\n')
#---------------------------------------------------------------------------------------------------------------------

# Get the month titles
for mon in range(1, 14):
    id = "month_" + str(mon) + "_button"
    id_a = "month_" + str(mon) + "A" + "_button"
    id_b = "month_" + str(mon) + "B" + "_button"
    if soup.find('button', {'id': id_a}) != None:
        month_titles.append(soup.find('button', {'id': id_a}).text.strip())
        month_titles.append(soup.find('button', {'id': id_b}).text.strip())
    elif soup.find('button', {'id': id}) != None:
        month_titles.append(soup.find('button', {'id': id}).text.strip())

# for v in month_titles:
#     print(v)
    # with open("./months.txt", 'a') as f:
    #     f.write(str(v) +"\n")

# ---------------------------------------------------------------------------------------------------------------------

# Get the event titles
for mon in range(1, 13):
    current_event = []
    event_a = []
    event_b = []
    edited_title = ""
    for event in range(1, 15):
        if (soup.find(id='month_' + str(mon) + "A" + "_farbrengen_" + str(event) + "_button")) == None:
            if(soup.find('button', {'id': "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"}) != None):
                current_event.append(({
                   "event":
                    formatString(soup.find('button', {'id': "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"}).text.strip()),
                    "month": formatString(soup.find('button', {'id': "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"}).attrs['id'].strip()),
                    "link": formatString(soup.find('button', {'id': "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"}).a.attrs['href'].strip())
                    }))
        else:
            if(soup.find('button', {'id': "month_" + str(mon) + "A" + "_farbrengen_" + str(event) + "_button"}) != None):
                event_a.append(({
                   "event":
                    formatString(soup.find('button', {'id': "month_" + str(mon) + "A" + "_farbrengen_" + str(event) + "_button"}).text.strip()),
                    "month":formatString(soup.find('button', {'id': "month_" + str(mon) + "A" + "_farbrengen_" + str(event) + "_button"}).attrs['id'].strip()).strip(),
                    "link":formatString(soup.find('button', {'id': "month_" + str(mon) + "A" + "_farbrengen_" + str(event) + "_button"}).a.attrs['href'].strip())
                    }))
            if (soup.find('button', {'id': "month_" + str(mon) + "B" + "_farbrengen_" + str(event) + "_button"}) != None):
                event_b.append(({
                   "event":
                    formatString(soup.find('button', {'id': "month_" + str(mon) + "B" + "_farbrengen_" + str(event) + "_button"}).text.strip()),
                    "month":formatString(soup.find('button', {'id': "month_" + str(mon) + "B" + "_farbrengen_" + str(event) + "_button"}).attrs['id'].strip()).strip(),
                    "link":formatString(soup.find('button', {'id': "month_" + str(mon) + "B" + "_farbrengen_" + str(event) + "_button"}).a.attrs['href'].strip()),  
                    }
                    ))
    event_titles.append(event_a)
    event_titles.append(event_b)
    event_titles.append(current_event)  

event_titles = [x for x in event_titles if x]

# for e in event_titles:
#     print(e)
#     print('\n')
# ---------------------------------------------------------------------------------------------------------------------

#Get the event links
base_url = 'https://www.mafteiach.app'
for mon in range(1, 14):
    link_list = []
    link_a = []
    link_b = []
    for event in range(1, 15):
        toSearch_a = "month_" + str(mon) + "A"+ "_farbrengen_" + str(event) + "_button"
        toSearch_b = "month_" + str(mon) + "B"+ "_farbrengen_" + str(event) + "_button"
        if (soup.find(id='month_' + str(mon) + "A" + "_farbrengen_" + str(event) + "_button")) == None:
            toSearch = "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"
            button = soup.find('button', {'id': toSearch})
            if(button != None):
                link = {'title': formatString(button.text.strip()), 'link': base_url.strip() + button.a.attrs['href']}
                link_list.append(link)
        else:
            if (soup.find(id='month_' + str(mon) + "A" + "_farbrengen_" + str(event) + "_button")) != None:
                event_a = soup.find('button', {'id': toSearch_a})
                if(event_a != None ):
                    link_a.append({'link': (base_url.strip() + event_a.a.attrs['href'].strip()).strip(), 'title': formatString(event_a.text.strip())})
            if (soup.find(id='month_' + str(mon) + "B" + "_farbrengen_" + str(event) + "_button")) != None:
                event_b = soup.find('button', {'id': toSearch_b})
                if(event_b != None):
                    link_b.append({'link': (base_url.strip() + event_b.a.attrs['href'].strip()).strip(), 'title': formatString(event_b.text.strip())})
    event_links.append(link_a)
    event_links.append(link_b)
    event_links.append(link_list)
    
event_links = [x for x in event_links if x] 

#---------------------------------------------------------------------------------------------------------------------

# e_link = []

base_url = 'https://www.mafteiach.app'

# #Get event items
for mon in range(1, 14):
    content_a  = []
    content_b = []
    content = []
    for event in range(1, 15):
        event_a = "month_" + str(mon) + "A"+ "_farbrengen_" + str(event) + "_content"
        event_b = "month_" + str(mon) + "B"+ "_farbrengen_" + str(event) + "_content"
        event_norm = "month_" + str(mon) + "_farbrengen_" + str(event) + "_content"
        button_norm = []
        button_a = []
        button_b = []
        if (soup.find('div', id=event_a)) == None:
            content_norm = soup.find('div', id = event_norm)
            but_norm = soup.find('button', id = "month_" + str(mon) + "_farbrengen_" + str(event) + "_button")
            if(soup.find('div', id = event_norm) != None):
                button_norm = content_norm.find_all('button', {'class': re.compile(r'farbrengen-detail-button')})
                for b in button_norm:
                    cont = b.find_next_sibling('div', {'class': re.compile(r'-content hidden')})
                    if(b.find_next_sibling('div', {'class': re.compile(r'-content hidden')}) != None):
                        cont_list_norm = cont.find_all('a')
                        for con in cont_list_norm:
                            content.append({"content": {"link": con.attrs['href'].strip(), "title": formatString(con.text.strip())}, "id": content_norm.attrs['id'], "event_title": formatString(but_norm.text.strip()), "event_link": (base_url.strip() + but_norm.a.attrs['href'].strip())})
                    else:
                            content.append({"content": {"link": None, "title": None}, "id": content_norm.attrs['id'], "event_title": formatString(but_norm.text.strip()), "event_link": (base_url.strip() + but_norm.a.attrs['href'].strip())})
        else:
            if(soup.find(id=event_a) != None):
                cont_a = soup.find('div', id = event_a)
                but_a = soup.find('button', id = "month_" + str(mon) + "A" + "_farbrengen_" + str(event) + "_button")
                if(soup.find('div', id = event_a) != None):
                    button_a = cont_a.find_all('button', {'class': re.compile(r'farbrengen-detail-button')})
                    for b in button_a:
                        cont = b.find_next_sibling('div', {'class': re.compile(r'-content hidden')})
                        if(b.find_next_sibling('div', {'class': re.compile(r'-content hidden')}) != None):
                            cont_list_a = cont.find_all('a')
                            for con in cont_list_a:
                                content_a.append({"content": {"link": con.attrs['href'].strip(), "title": formatString(cont.text.strip())}, "id": cont_a.attrs['id'], "event_title": formatString(but_a.text.strip()), "event_link": (base_url.strip() + but_a.a.attrs['href'].strip())})
                        else:
                                content_a.append({"content": {"link": None, "title": None}, "id": cont_a.attrs['id'], "event_title": formatString(but_a.text.strip()), "event_link": (base_url.strip() + but_a.a.attrs['href'].strip())})
            if(soup.find(id=event_b) != None):
                cont_b = soup.find('div', id = event_b)
                but_b = soup.find('button', id = "month_" + str(mon) + "B" + "_farbrengen_" + str(event) + "_button")
                if(soup.find('div', id = event_b) != None):
                    button_b = cont_b.find_all('button', {"class": re.compile(r'farbrengen-detail-button')})
                    for b in button_b:
                        cont = b.find_next_sibling('div', {'class': re.compile(r'-content hidden')}) 
                        if(b.find_next_sibling('div', {'class': re.compile(r'-content hidden')}) != None):
                            cont_list_b = cont.find_all('a')
                            for con in cont_list_b:
                                content_b.append({"content": {"link": con.attrs['href'].strip(), "title": formatString(con.text.strip())}, "id": cont_b.attrs['id'], "event_title": formatString(but_b.text.strip()), "event_link": (base_url.strip() + but_b.a.attrs['href'].strip())})
                        else:
                                content_b.append({"content": {"link": None, "title": None}, "id": cont_b.attrs['id'], "event_title": formatString(but_b.text.strip()), "event_link": (base_url.strip() + but_b.a.attrs['href'].strip())})
    event_items.append(content_a)
    event_items.append(content_b)
    event_items.append(content)

event_items = [x for x in event_items if x]

dummmy_list = event_items

event_items = []

for i in dummmy_list:
    new_dict = []
    n_urls = set()

    for j in range(len(i)):
        if not i[j]['content']['link'] in n_urls:
            new_dict.append(i[j])
            n_urls.add(i[j]['content']['link'])
    i = new_dict
    event_items.append(i)

#remove dulplicate dicts from event_items
# event_items = [dict(t) for t in {tuple(d.items()) for d in event_items}]
# for i in event_items:
#     for j in i:
#         print(str(j) + '\n')
#     print('\n')
    # print(str(i) + "\n")
    # print('\n')

# event_items = []
# for e in event_items:
#     e = createListOfUniqueDict(e)
# ---------------------------------------------------------------------------------------------------------------------

#There will be five five code lines for getting the link of each event
# data = {} 
# for mon in range(1, 13):
#     button = soup.find('div', {'id': "month_" + str(mon) + "A" + "_content"}) if soup.find('div', {"id": "month_" + str(mon) + "A" + "_content"}) != None else soup.find('div', {'id': "month_" + str(mon) + "_content"})
#     event_list = []
#     curr_list = []
#     for event in range(1, 15):
#         current_event = button.find('div', {'id': "month_" + str(mon) + "A" + "_farbrengen_" + str(event)}) if soup.find('div', {"id": "month_" + str(mon) + "A" + "_farbrengen_" + str(event)}) != None else soup.find('div', {'id': "month_" + str(mon) + "_farbrengen_" + str(event)}) if soup.find('div', {"id": "month_" + str(mon) + "_farbrengen_" + str(event)}) != None else None
#         event_list.append(current_event)
#         buttons = soup.find_all(id = "month_" + str(mon) +"_farbrengen_" + str(event)+ "_content")
#         for button in buttons:
#             links = button.find_all('a')
#             for link in links:
#                 lin = link.attrs['href']
#                 print(lin)
#                 curr_list.append(lin)
#             for e in event_list:
#                 id_a = "month_" + str(mon) + "A" + "_farbrengen_" + str(event) + "_content"
#                 id = "month_" + str(mon) + "_farbrengen_" + str(event) + "_content"
#                 div = e.find('div', {'id': id_a}) if e.find('div', {'id': id_a}) != None else e.find('div', {'id': id})     

#             print('\n\n\n\n')

#----------------------------------------------------------------------------------------------------------------------

#Parse and format the data
list_of_lists = [event_titles, event_dates, event_links, month_titles]

month_titles.append('null')

list_length = []

def getMaxLen(list):
    max_list = []
    for newList in list:
        if len(newList) > len(max_list):
            max_list = newList
    return len(max_list)

def equalList(list, max_len):
    len_list = len(list)
    short = max_len - len_list
    for i in range(short):
        list.append('null')
    return list

def trimList(_list):
    present_list = _list
    _list = []
    for l in present_list:
        l = list(set(l))
        print(l)
        print('\n')
        _list.append(l)
    return _list

# event_dates = trimList(event_dates)
# event_titles = trimList(event_titles)
# event_links = trimList(event_links)

max_len = getMaxLen(list_of_lists)

event_dates = equalList(event_dates, max_len)
event_titles = equalList(event_titles, max_len)
event_links = equalList(event_links, max_len)
event_items = equalList(event_items, max_len)


#Create the csv file
df = pd.DataFrame({'Month': json.dumps(month_titles, ensure_ascii=False), 'Event': json.dumps(event_items, ensure_ascii=False), 'Date': json.dumps(event_dates, ensure_ascii=False), 'Link': json.dumps(event_links, ensure_ascii=False) }, index=[0])
con = df.to_csv('./data.csv', sep=',', index=False)

kd = pd.read_csv('./data.csv')

# ---------------------------------------------------------------------------------------------------------------------

#print(button.get('id'))
#There will be two code lines to get an event title     
# event_title_div = first_button_div.find(id='month_1_farbrengen_2')
# print(str(event_title_div.find('div').find(class_='pa2').text))

#There will be two code lines for the onclick data
#event_title_div = first_button_div.find(id='month_1_farbrengen_2')
#print(event_title_div.a.attrs['onclick'])

#There will be two code lines for the name of different types of sources for the available events
#buttons = first_button_div.find(id='month_1_farbrengen_1_content')
#links = buttons.find_all('button')
#for link in links:
#    print(link.text)

#There will be five five code lines for getting the link of each event 
#buttons = first_button_div(id='month_1_farbrengen_1_content')
#for button in buttons:
    #print(button.find_all('a'))
    #links = button.find_all('a')
    #for link in links: 
        #print(link.attrs['href'])
