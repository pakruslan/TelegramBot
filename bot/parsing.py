import requests
from bs4 import BeautifulSoup
import csv


main_url = 'https://kaktus.media/' 
number = 0



def get_html(url):
    response = requests.get(url)
    return response.text

def make_soup(html):
    soup = BeautifulSoup(html,'html.parser')
    return soup




def find_news(soup):
    items_list = soup.find('ul', class_='topic_list view_lenta 1').find_all('li', class_='topic_item clearfix')
    main_list = []
    for item in items_list:
        try:
            title = item.find('div', class_='t f_medium').find('span', class_="n").text.strip()
        except:
            title = ''

        try:
            url = item.find('div', class_='t f_medium').find('a').get('href')
            
        except:
            url = ''
                
        data = {'title':title,'url':url}
        ex =  [data['title'], data['url']]
        main_list.append(ex)
    return main_list
    
def write_csv1(data):
    with open("/home/emina/Documents/bootcamp/Hackathon/newnews.csv", "w") as file:
        writer = csv.writer(file)
        for i in data:
            writer.writerow(i) 
        
            
    

def call_title_url(num):
    with open("/home/emina/Documents/bootcamp/Hackathon/newnews.csv", "r") as file:
        content = file.readlines()[int(num)-1].strip()
        ind = content.index('h')
        url = content[ind:]
        return url

def find_descr(soup):
    descr = []
    try:
        d = soup.find('div',itemprop="articleBody").find_all('p')
        for i in d:
            descr.append(i.text)
        desc = ' '.join(descr)   
    except:
        desc = ""

    try:
        photo = soup.find('img', style='display:none;').get('src')
    except:
        photo = ""

    data = {'desc':desc, 'photo':photo}
    return data

def write_csv2(data):
    with open("/home/emina/Documents/bootcamp/Hackathon/descr.csv" ,'a') as file:
        writer = csv.writer(file)
        writer.writerow([data['desc'], data['photo']])


def call_descr():
    with open("/home/emina/Documents/bootcamp/Hackathon/descr.csv", "r") as file:
        content = file.readlines()
        return content[-1]



def parse_main_page():
    html_text = get_html(main_url)
    soup = make_soup(html_text)
    main_list = find_news(soup)
    write_csv1(main_list)


def parse_title_page(number):
    title_url = call_title_url(number)
    html_text = get_html(title_url)
    soup = make_soup(html_text)
    data = find_descr(soup)
    write_csv2(data)

# parse_main_page()
# for i in range(1,21):
#     parse_title_page(i)