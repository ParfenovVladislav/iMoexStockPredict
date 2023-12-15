from bs4 import BeautifulSoup
import requests
import datetime
import pandas as pd
from multiprocessing import Pool, Lock
from requests.adapters import HTTPAdapter, Retry

class NewsInformation:
    def __init__(self):
        self.date_list = []
        self.headers = {
            'Connection': 'close', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, '
            'like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        }

        self.url_archive = None
        self.data_list = []
        self.text_list = []
        #self.title_list = []
        #self.tag_list = []

    def generate_datalist(self):

        date_format = '%Y%m%d'
        step = datetime.timedelta(days=1)
        start_date = datetime.datetime.strptime("20230902", date_format)
        end_date = datetime.datetime.strptime("20231001", date_format)

        while start_date <= end_date:
            self.date_list.append(start_date.strftime(date_format))
            start_date += step

        for i in self.date_list:
            self.parsing_daily_news(i)
            print(i + ': DONE')


    def parse_single_page(self, url, data_day, page_number):
        session = requests.Session()
        retry = Retry(connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)

        self.url_archive = f"https://ria.ru/{url}/{data_day}/?page={page_number}"
        page = session.get(self.url_archive, headers=self.headers)
        response = page.status_code
        if response == 200:
            soup = BeautifulSoup(page.text, "html.parser")
            news = soup.find_all('a', class_="list-item__title color-font-hover-only")
            tags = soup.find_all('div', class_="list-item__tags-list")
            
            i_i = 0
            for dd in news:
                data = news[i_i]
                title = data.contents[0]
                tag = tags[i_i]
                tags_1 = [i.contents[0] for i in tag.find_all("span", class_="list-tag__text")]
                correct_tag = False
                for m_tag in tags_1:
                    if m_tag == 'Россия':
                        correct_tag = True
                #if correct_tag == False:
                #    pass

                #self.tag_list.append(tags_1)
                href = data["href"]
                        
                session1 = requests.Session()
                retry1 = Retry(connect=3, backoff_factor=0.5)
                adapter1 = HTTPAdapter(max_retries=retry1)
                session1.mount('https://', adapter1)
                page1 = requests.get(href, headers=self.headers)
                response = page1.status_code
                if response == 200:
                    soup1 = BeautifulSoup(page1.text, "html.parser")
                    text = soup1.find_all('div', class_="article__text")
                    text += soup1.find_all('div', class_="article_block")
                full_text = None    
                is_first = True
                for one_part in text:
                    if (is_first):
                        splitted_str = one_part.text.split(". ", 1)
                        if len(splitted_str) > 1:
                            full_text = splitted_str[1]
                        else: 
                            full_text = splitted_str[0]
                        is_first = False
                    else:
                        full_text += one_part.text
                if full_text != '':
                    self.text_list.append(full_text)
                    self.data_list.append(datetime.datetime.strptime(data_day, "%Y%m%d").date())
                else:
                    i = 3

                #self.title_list.append(title)
                i_i += 1     

            str1 = data_day + ' ' + url + ' page ' + str(page_number) + ': OK'
            print(str1)  
        else:
            pass
            str1 = data_day + ' ' + url + ' page ' + str(page_number) + ': NO PAGE'
            print(str1)  


    def parsing_daily_news(self, data_day):
        page_number = 5
        for i in range(1, page_number):
            m_page_number = i
            url_ec = 'economy'
            url_pol = 'politics'
            self.parse_single_page(url_ec, data_day, m_page_number)
            self.parse_single_page(url_pol, data_day, m_page_number)
            
            a = {
                "date": self.data_list,
                "text": self.text_list,
                #"tags": self.tag_list,
                #"title": self.title_list,
                }
            df = pd.DataFrame.from_dict(a, orient='index')
            df = df.transpose()
            df.to_csv('corpu09.csv', mode='a', header=False, index=False)
            self.data_list = []
            self.text_list = []
            #self.tag_list = []
            
if __name__ == "__main__":
    start = NewsInformation()
    start.generate_datalist()
