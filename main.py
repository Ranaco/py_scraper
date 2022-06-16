import csv
import json
import re
import time
from venv import create
from bs4 import BeautifulSoup
import requests
import ndjson
import pandas as pd

year_response = requests.get("https://www.mafteiach.app/all/by_year/5711/")
year_content = year_response.content

this_soup = BeautifulSoup(year_content, 'html.parser')

#List of years till year "5742"
list_of_years = []

years_list = this_soup.find('div', {'id': "years"})

list_of_years = years_list.find_all("button", {"class": re.compile(r'year')})

year_dummy = list_of_years
list_of_years = []

for i in year_dummy:
    k = i.attrs['id']
    list_of_years.append(k)

remove_list = list_of_years
list_of_years = []
for r in remove_list:
   l = r.replace("year_", "")
   list_of_years.append(l)

for year in list_of_years:
    url = "https://www.mafteiach.app/all/by_year/" + str(year) + "/"
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
    #Get the year
    year_div = soup.find('button', {'class': 'year side-nav-item pure-material-button-contained f4 button active scroll_me_in_to_view'})
    year = soup.find('button', {'class': 'year side-nav-item pure-material-button-contained f4 button active scroll_me_in_to_view'}).text.strip()
    year_num = year_div.attrs['id']
    #---------------------------------------------------------------------------------------------------------------------
    # #Get the event dates
    # for mon in range(1, 13):
    #     link_list = []
    #     event_a = []
    #     event_b = []
    #     link = []
    #     a = True
    #     for event in range(1, 15):
    #         id_a = "month_" + str(mon) + "A" + "_farbrengen_" + str(event) + "_button"
    #         id = "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"
    #         id_b = "month_" + str(mon) + "B" + "_farbrengen_" + str(event) + "_button"
    #         if (soup.find(id = id_a) == None):
    #             button = soup.find('button', {"id": id})
    #             if(button != None):
    #                 link_list.append(button.a.attrs['href'].removeprefix('/').replace('all/', ''))
    #         elif (soup.find(id = id_a) != None ):
    #             button_a = soup.find('button', {"id": id_a})
    #             button_b = soup.find('button', {"id": id_b})
    #             if(button_a != None):
    #                 event_a.append(button_a.a.attrs['href'].removeprefix('/').replace('all/', ''))
    #             if(button_b != None):
    #                 event_b.append(button_b.a.attrs['href'].removeprefix('/').replace('all/', ''))
    #     event_dates.append(event_a)
    #     event_dates.append(event_b)
    #     event_dates.append(link_list)
    # event_dates = [x for x in event_dates if x]
    #---------------------------------------------------------------------------------------------------------------------
    # # Get the month titles
    # for mon in range(1, 14):
    #     id = "month_" + str(mon) + "_button"
    #     id_a = "month_" + str(mon) + "A" + "_button"
    #     id_b = "month_" + str(mon) + "B" + "_button"
    #     if soup.find('button', {'id': id_a}) != None:
    #         month_titles.append({"name": soup.find('button', {'id': id_a}).text.strip(), "value": id_a})
    #         month_titles.append({"name": soup.find('button', {'id': id_b}).text.strip(), "value": id_b})
    #     elif soup.find('button', {'id': id}) != None:
    #         month_titles.append({"name": soup.find('button', {'id': id}).text.strip(), "value": id})
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
                       "eventTitle":
                        formatString(soup.find('button', {'id': "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"}).text.strip()),
                        "monthId":(re.sub('m.*?_', "", re.sub( '_b.*?on',formatString(""), string=soup.find('button', {'id': "month_" + str(mon) + "_button"}).attrs['id'].strip()))),
                        "yearId": int(re.sub('y.*?_' ,"", formatString(year_num).strip())),
                        "eventId": int(re.sub('_b.*?on', '', re.sub('m.*?gen_', '', formatString(soup.find('button', {'id': "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"}).attrs['id'].strip()).strip()))),
                        }))
            else:
                if(soup.find('button', {'id': "month_" + str(mon) + "A" + "_farbrengen_" + str(event) + "_button"}) != None):
                    event_a.append(({
                       "eventTitle":
                        formatString(soup.find('button', {'id': "month_" + str(mon) + "A" + "_farbrengen_" + str(event) + "_button"}).text.strip()),
                        "monthId":(re.sub('m.*?_', "", re.sub('_b.*?on' , formatString(""), string=soup.find('button', {'id': "month_" + str(mon) + "A" + "_button"}).attrs['id'].strip()))),
                        "yearId": int(re.sub('y.*?_' ,"", formatString(year_num).strip())),
                        "eventId": int(re.sub('_b.*?on', '', re.sub('m.*?gen_', '', formatString(soup.find('button', {'id': "month_" + str(mon) + "A"+ "_farbrengen_" + str(event) + "_button"}).attrs['id'].strip()).strip()))),
                        }))
                if (soup.find('button', {'id': "month_" + str(mon) + "B" + "_farbrengen_" + str(event) + "_button"}) != None):
                    event_b.append(({
                       "eventTitle":
                        formatString(soup.find('button', {'id': "month_" + str(mon) + "B" + "_farbrengen_" + str(event) + "_button"}).text.strip()),
                        "monthId":(re.sub('m.*?_', "", re.sub('_b.*?on', formatString(""), string=soup.find('button', {'id': "month_" + str(mon) + "B" + "_button"}).attrs['id'].strip()))),
                        "yearId": int(re.sub('y.*?_' ,"", formatString(year_num).strip())),
                        "eventId":  int(re.sub('_b.*?on', '', re.sub('m.*?gen_', '', formatString(soup.find('button', {'id': "month_" + str(mon) + "B"+ "_farbrengen_" + str(event) + "_button"}).attrs['id'].strip()).strip()))),
                        }
                        ))
        event_titles.append(event_a)
        event_titles.append(event_b)
        event_titles.append(current_event)  
    event_titles = [x for x in event_titles if x]
    # for e in event_titles:
    #     print(e)
    #     print('\n')
    # # ---------------------------------------------------------------------------------------------------------------------
    # #Get the event links
    # base_url = 'https://www.mafteiach.app'
    # for mon in range(1, 14):
    #     link_list = []
    #     link_a = []
    #     link_b = []
    #     for event in range(1, 15):
    #         toSearch_a = "month_" + str(mon) + "A"+ "_farbrengen_" + str(event) + "_button"
    #         toSearch_b = "month_" + str(mon) + "B"+ "_farbrengen_" + str(event) + "_button"
    #         if (soup.find(id='month_' + str(mon) + "A" + "_farbrengen_" + str(event) + "_button")) == None:
    #             toSearch = "month_" + str(mon) + "_farbrengen_" + str(event) + "_button"
    #             button = soup.find('button', {'id': toSearch})
    #             if(button != None):
    #                 link = {'title': formatString(button.text.strip()),}
    #                 link_list.append(link)
    #         else:
    #             if (soup.find(id='month_' + str(mon) + "A" + "_farbrengen_" + str(event) + "_button")) != None:
    #                 event_a = soup.find('button', {'id': toSearch_a})
    #                 if(event_a != None ):
    #                     link_a.append({'title': formatString(event_a.text.strip())})
    #             if (soup.find(id='month_' + str(mon) + "B" + "_farbrengen_" + str(event) + "_button")) != None:
    #                 event_b = soup.find('button', {'id': toSearch_b})
    #                 if(event_b != None):
    #                     link_b.append({'title': formatString(event_b.text.strip())})
    #     event_links.append(link_a)
    #     event_links.append(link_b)
    #     event_links.append(link_list)
    # event_links = [x for x in event_links if x] 
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
                    button_norm = content_norm.find_all('button', {'class': re.compile(r'has-content button')})
                    for b in button_norm:
                        cont = b.find_next_sibling('div', {'class': re.compile(r'-content hidden')})
                        if(b.find_next_sibling('div', {'class': re.compile(r'-content hidden')}) != None):
                            cont_list_norm = cont.find_all('a')
                            for con in cont_list_norm:
                                content.append( {"link": con.attrs['href'].strip(), "title": formatString(con.text.strip()), "button_text": b.text.strip(), "event_id": int(re.sub('_b.*?on', '', re.sub('m.*?en_', '', but_norm.attrs['id'].strip())))})
                        else:
                                content.append( {"link": None, "title": None})
            else:
                if(soup.find(id=event_a) != None):
                    cont_a = soup.find('div', id = event_a)
                    but_a = soup.find('button', id = "month_" + str(mon) + "A" + "_farbrengen_" + str(event) + "_button")
                    if(soup.find('div', id = event_a) != None):
                        button_a = cont_a.find_all('button', {'class': re.compile(r'has-content button')})
                        for b in button_a:
                            cont = b.find_next_sibling('div', {'class': re.compile(r'-content hidden')})
                            if(b.find_next_sibling('div', {'class': re.compile(r'-content hidden')}) != None):
                                cont_list_a = cont.find_all('a')
                                for con in cont_list_a:
                                    content_a.append({"link": con.attrs['href'].strip(), "title": formatString(cont.text.strip()), "button_text": b.text.strip(), "event_id": int(re.sub('_b.*?on', '', re.sub('m.*?en_', '', but_a.attrs['id'].strip())))})
                            else:
                                    content_a.append({"link": None, "title": None})
                if(soup.find(id=event_b) != None):
                    cont_b = soup.find('div', id = event_b)
                    but_b = soup.find('button', id = "month_" + str(mon) + "B" + "_farbrengen_" + str(event) + "_button")
                    if(soup.find('div', id = event_b) != None):
                        button_b = cont_b.find_all('button', {"class": re.compile(r'has-content button')})
                        for b in button_b:
                            cont = b.find_next_sibling('div', {'class': re.compile(r'-content hidden')}) 
                            if(b.find_next_sibling('div', {'class': re.compile(r'-content hidden')}) != None):
                                cont_list_b = cont.find_all('a')
                                for con in cont_list_b:
                                    content_b.append({"link": con.attrs['href'].strip(), "title": formatString(con.text.strip()), "button_text": b.text.strip(), "event_id": int(re.sub('_b.*?on', '', re.sub('m.*?en_', '', but_b.attrs['id'].strip())))})
                            else:
                                    content_b.append({"link": None, "title": None})
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
            if not i[j]['link'] in n_urls:
                new_dict.append(i[j])
                n_urls.add(i[j]['link'])
        i = new_dict
        event_items.append(i)
    #----------------------------------------------------------------------------------------------------------------------
    #Parse and format the data

    list_of_lists = [event_titles, event_dates, event_links, month_titles]
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
    max_len = getMaxLen(list_of_lists)
    event_titles = equalList(event_titles, max_len)
    event_items = equalList(event_items, max_len)

    for i in range(len(event_titles)):
        for k in range(len(event_titles[i])):
            event_titles[i][k] = {**event_titles[i][k], "eventContent": event_items[i],}
            # print('\n\n\n')
            # print(event_items[i])
            # print('\n\n\n')
            
    # for i in range(len(event_titles)):
    #     for k in range(len(event_titles[i])):
    #            print(event_titles[i][k])
    #            print('\n\n\n')
    #Create csv file for event_titles with the field name of event 
    df = pd.DataFrame({'Event': json.dumps(event_titles, ensure_ascii=False) }, index=[0])
    con = df.to_csv('./csv/' + str(year_num) + '_event_titles.csv', sep=',',)