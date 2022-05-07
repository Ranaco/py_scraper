from asyncio import events
from email.mime import base
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

url = "https://www.mafteiach.app/"

response = requests.get(url)

htmlContent = response.content

soup = BeautifulSoup(htmlContent, "html.parser")

banned_words = ['share', 'arrow_back', 'videocam']

month_titles = [] #/
event_titles = [] #/
event_dates = [] #/
event_itmes = [] 
event_links = [] #/

def formatString(string):
    return ' '.join(i for i in string.split() if i not in banned_words )

# for mon in range(1, 13):
#     for event in range(1, 15):
#         to_search = 'month_' + str(mon) + "_farbrengen_" + str(event) + "_content"
#         if(soup.find(id=to_search)):
#             if(soup.find('button', {"class": "farbrengen-detail-button farbrengen-detail-button-disabled button"}) != None):  
#                 print(to_search)

#---------------------------------------------------------------------------------------------------------------------

for mon in range(1, 13):
    link_list = []
    link = []
    a = True
    for event in range(1, 15):
        if (soup.find(id='month_' + str(mon) + "A" + "_farbrengen_" + str(event) + "_content")) == None:
            toSearch = "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"
            button = soup.find('button', {'id': toSearch})
            if(button != None):
                link = button.a.attrs['href'].removeprefix('/').replace('all/', '')
            link_list.append(link)
            a = not a
        else:   
            toSearch = "month_" + str(mon) + "A"+ "_farbrengen_" + str(event) + "_button"
            # print(toSearch)
            button = soup.find('button', {'id': toSearch})
            if(button != None):
                link = button.a.attrs['href'].removeprefix('/').replace('all/', '')
            link_list.append(link)
            a = False

    event_dates.append(link_list)


# for date in event_dates:
#     for link in date:
#         print(link)
#         print('\n')
#     print('\n\n\n\n\n')

# #---------------------------------------------------------------------------------------------------------------------

for mon in range(1, 13):
    if(soup.find('button', {'id': "month_"+str(mon)+"_button"}) != None):
        month_titles.append(soup.find('button', {'id': "month_"+str(mon)+"_button"}).text.strip())

# ---------------------------------------------------------------------------------------------------------------------

for mon in range(1, 13):
    current_event = []
    edited_title = ""
    for event in range(1, 15):
        if (soup.find(id='month_' + str(mon) + "A" + "_farbrengen_" + str(event) + "_content")) == None:
            if(soup.find('button', {'id': "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"}) != None):
                edited_title = formatString(soup.find('button', {'id': "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"}).text)
            current_event.append(edited_title.strip())
        else:
            if(soup.find('button', {'id': "month_" + str(mon) + "A" + "_farbrengen_" + str(event) + "_button"}) != None):
                edited_title = formatString(soup.find('button', {'id': "month_" + str(mon) + "A" + "_farbrengen_" + str(event) + "_button"}).text)
            current_event.append(edited_title.strip())
    event_titles.append(current_event)    

dummy_events = event_titles

event_titles = []

for event in dummy_events:
    event_titles.append(list(set(event)))

# ---------------------------------------------------------------------------------------------------------------------

for mon in range(1, 13):
    link_list = []
    link = []
    for event in range(1, 15):
        toSearch = "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"
        button = soup.find('button', {'id': toSearch})
        if(button != None):
            base_url = 'https://www.mafteiach.app'
            link = (base_url.strip() + button.a.attrs['href'].strip()).strip()
        link_list.append(link)
    event_links.append(link_list)

# ---------------------------------------------------------------------------------------------------------------------

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
    # print(_list)
    _list = []
    for l in present_list:
        l = list(set(l))
        # print(l)
        _list.append(l)
    print(_list)    

trimList(event_dates)

# for dates in event_dates:
#     print(dates)
#     print('\n\n\n\n')

# event_dates = list(set(event_dates))
# event_titles = list(set(event_titles))
# event_links = list(set(event_links))
# month_titles = list(set(month_titles))

# count = 0

# for list  in list_of_lists:
#     with open("./" + str(count) + ".txt", "a") as f:
#         f.write(str(list))
#         count += 1

# df = pd.DataFrame({'Month': month_titles, 'Event': event_titles, 'Date': event_dates, 'Link': event_links})
# with open('./data.txt', 'a') as f:
#     con = df.to_csv(f, sep='\t', index=False)
#     f.write(str(con))

# for mon in range(1, 13):
#     events = []
#     for event in range(1, 15):    
#         if(soup.find('div', {'id': "month_" + str(mon) + "_farbrengen_" + str(event) + "_content"}) != None):
#             edited_title = soup.find('div', {'id': "month_" + str(mon) + "_farbrengen_" + str(event) + "_content"}).text.replace('share', '')
#             print(formatString(str(soup.find('div', {'id': "month_" + str(mon) + "_farbrengen_" + str(event) + "_content"}).text.strip())))
#             print("\n\n\n\n\n")

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
