from bs4 import BeautifulSoup
import requests

count = 0
i = 10

while i < 53:
    url = "https://www.mafteiach.app/all/by_year/57" + str(i)

    response = requests.get(url)

    htmlContent = response.text

    soup = BeautifulSoup(htmlContent, 'html.parser')

    links = soup.find_all('a')


    for link in links:
        href = link.get('href')
        with open('./57'+ str(i) +'.txt', 'a') as f:
            if count == 0:
                f.write("internal" + "\t" * 10 + "drive\n" )
            elif href[0] == '/':
                string_to_write =  "\n\n" + "https://mafteiach.app" + href
                f.write(string_to_write + "\t" * 3)
            else:
                f.write(href + "\n")
                f.write('\t' * 12)
            count += 1
    count = 0
    i = i + 1
