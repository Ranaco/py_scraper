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
event_itmes = [] 
event_links = [] #/

def formatString(string):
    return ' '.join(i for i in string.split() if i not in banned_words )

def createListOfUniqueDict(event_link_list):
    seen = set()
    new_l = event_link_list
    event_link_list = []
    for k in new_l:
        d = tuple(k.items())
        if d not in seen:
            seen.add(d)
            event_link_list.append(k)
    return event_link_list
#---------------------------------------------------------------------------------------------------------------------

#Get the event dates
# for mon in range(1, 13):
#     link_list = []
#     link = []
#     a = True
#     for event in range(1, 15):
#         if (soup.find(id='month_' + str(mon) + "A" + "_farbrengen_" + str(event) + "_button")) == None:
#             toSearch = "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"
#             button = soup.find('button', {'id': toSearch})
#             if(button != None):
#                 link = button.a.attrs['href'].removeprefix('/').replace('all/', '')
#             link_list.append(link)
#             a = not a
#         else:   
#             toSearch = "month_" + str(mon) + "A"+ "_farbrengen_" + str(event) + "_button"
#             button = soup.find('button', {'id': toSearch})
#             if(button != None):
#                 link = button.a.attrs['href'].removeprefix('/').replace('all/', '')
#             link_list.append(link)
#             a = False

#     event_dates.append(link_list)
    
#---------------------------------------------------------------------------------------------------------------------

#Get the month titles
# for mon in range(1, 13):
#     if(soup.find('button', {'id': "month_"+str(mon)+"_button"}) != None):
#         month_titles.append(soup.find('button', {'id': "month_"+str(mon)+"_button"}).text.strip())

# ---------------------------------------------------------------------------------------------------------------------

#Get the event titles
# for mon in range(1, 13):
#     current_event = []
#     edited_title = ""
#     for event in range(1, 15):
#         if (soup.find(id='month_' + str(mon) + "A" + "_farbrengen_" + str(event) + "_button")) == None:
#             if(soup.find('button', {'id': "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"}) != None):
#                 edited_title = formatString(soup.find('button', {'id': "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"}).text.strip())
#             current_event.append(edited_title.strip())
#         else:
#             if(soup.find('button', {'id': "month_" + str(mon) + "A" + "_farbrengen_" + str(event) + "_button"}) != None):
#                 edited_title = formatString(soup.find('button', {'id': "month_" + str(mon) + "A" + "_farbrengen_" + str(event) + "_button"}).text.strip())
#             current_event.append(edited_title.strip())
#     event_titles.append(current_event)    

# dummy_events = event_titles

# event_titles = []

# for event in dummy_events:
#     event_titles.append(list(set(event)))

# ---------------------------------------------------------------------------------------------------------------------

#Get the event links
# for mon in range(1, 13):
#     link_list = []
#     link = []
#     for event in range(1, 15):
#         if (soup.find(id='month_' + str(mon) + "A" + "_farbrengen_" + str(event) + "_button")) == None:
#             toSearch = "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"
#             button = soup.find('button', {'id': toSearch})
#             if(button != None):
#                 base_url = 'https://www.mafteiach.app'
#                 link = (base_url.strip() + button.a.attrs['href'].strip()).strip()
#             link_list.append(link)
#         else:
#             toSearch = "month_" + str(mon) + "A"+ "_farbrengen_" + str(event) + "_button"
#             button = soup.find('button', {'id': toSearch})
#             if(button != None):
#                 base_url = 'https://www.mafteiach.app'
#                 link = (base_url.strip() + button.a.attrs['href'].strip()).strip()
#             link_list.append(link)
#     event_links.append(link_list)

#---------------------------------------------------------------------------------------------------------------------

e_link = []

#Get event items
for mon in range(1, 13):
    button = soup.find('div', {'id': "month_" + str(mon) + "A" + "_content"}) if soup.find('div', {"id": "month_" + str(mon) + "A" + "_content"}) != None else soup.find('div', {'id': "month_" + str(mon) + "_content"})
    event_list = []
    for event in range(1, 15):
        current_event = button.find('div', {'id': "month_" + str(mon) + "A" + "_farbrengen_" + str(event)}) if soup.find('div', {"id": "month_" + str(mon) + "A" + "_farbrengen_" + str(event)}) != None else soup.find('div', {'id': "month_" + str(mon) + "_farbrengen_" + str(event)}) if soup.find('div', {"id": "month_" + str(mon) + "_farbrengen_" + str(event)}) != None else None
        event_list.append(current_event)
        for e in event_list:
            if e != None:
                id_a = "month_" + str(mon) + "A" + "_farbrengen_" + str(event) + "_content"
                id = "month_" + str(mon) + "_farbrengen_" + str(event) + "_content"
                div = e.find('div', {'id': id_a }) if e.find('div', {'id': id_a}) != None else e.find('div', {'id': id})
                if div != None:
                    cls = div.find_all('button')
                    if cls != None:
                        print("\nThis is the month " + str(mon) + " and event " + str(event)+ "\n")
                        event_link_list = []
                        for cl in cls:
                            if cl.find_next_sibling('div') != None:
                                div_to_find = cl.find_next_sibling('div')
                                if div_to_find != None and div_to_find.get('class') != None and div_to_find.get('class')[0].startswith('farbrengen-detail-content'):    
                                    # print(div_to_find.get('class')[0])
                                    if div_to_find != None and div_to_find.get('class')[0].startswith('farbrengen-detail-content') and div_to_find.find('a') != None and formatString(div_to_find.find_previous_sibling('button').text.strip()) !="תוכן ענינים":
                                        lins = div_to_find.find_all('a')
                                        for l in lins:  
                                            if l.get('href') != None:
                                                event_link_list.append({formatString(div_to_find.find_previous_sibling('button').text.strip()): l.attrs['href']})
                            seen = set()
                            new_l = event_link_list
                            event_link_list = []
                            for k in new_l:
                                d = tuple(k.items())
                                if d not in seen:
                                    seen.add(d)
                                    event_link_list.append(k)
                        # event_link_list = [x for x in event_link_list if x != []]
                        # print(event_link_list)
                    print((event_link_list))
                        # e_link.append(event_link_list)
                        
        # print(e_link)
        # for e in event_links:
        #     print("This is the month" + str(mon) + "\n")
        #     print(e)
        #     print("\n\n\n")
        #                 # event_links.append(event_link_list)
        # print('\n\n')
# # print(soup.find(''))

    # for event in range(1, 15):.
    #     if mon == 6:
    #         if (soup.find('button', {'id': "month_"+str(mon)+ "A" +"_farbrengen_" + str(event) + "_content"}) == None):
    #             buttons = first_button_div.find(id='month_' + str(mon) + "_farbrengen_" + str(event) + "_content")
    #         else:
    #             buttons = first_button_div.find(id='month_' + str(mon) + "A" + "_farbrengen_" + str(event) + "_content")
    #         if(buttons != None):
    #             links = buttons.find_all('button')
            # for link in links:
                # print(formatString(link.text.strip()))
        # print('\n\n\n\n')


# buttons = first_button_div.find(id='month_1_farbrengen_1_content')
# links = buttons.find_all('button')
# for link in links:
#    print(formatString(link.text))

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
# list_of_lists = [event_titles, event_dates, event_links, month_titles]

# month_titles.append('null')

# list_length = []

# def getMaxLen(list):
#     max_list = []
#     for newList in list:
#         if len(newList) > len(max_list):
#             max_list = newList
#     return len(max_list)

# def equalList(list, max_len):
#     len_list = len(list)
#     short = max_len - len_list
#     for i in range(short):
#         list.append('null')
#     return list

# def trimList(_list):
#     present_list = _list
#     _list = []
#     for l in present_list:
#         l = list(set(l))
#         print(l)
#         print('\n')
#         _list.append(l)
#     return _list

# event_dates = trimList(event_dates)
# event_titles = trimList(event_titles)
# event_links = trimList(event_links)

# max_len = getMaxLen(list_of_lists)

# event_dates = equalList(event_dates, max_len)
# event_titles = equalList(event_titles, max_len)
# event_links = equalList(event_links, max_len)


# #Create the csv file
# df = pd.DataFrame({'Month': month_titles, 'Event': event_titles, 'Date': event_dates, 'Link': event_links})
# with open('./data.csv', 'a') as f:
#     con = df.to_csv(f, sep=',', index=False)
#     f.write(str(con))

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
