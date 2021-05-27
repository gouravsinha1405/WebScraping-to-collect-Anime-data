from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import time
import random
def create_anime_list(page_limit = 5, page_no = 1):
    anime_data = []
    while page_no <= page_limit:
        url = f'https://www.imdb.com/search/keyword/?keywords=anime&sort=moviemeter,asc&mode=detail&page={page_no}&ref_=kw_nxt'
        anime_text = requests.get(url).text
        soup = BeautifulSoup(anime_text,'lxml')
        # print(soup.prettify())
        anime_list = soup.find_all('div',class_ = 'lister-item mode-detail')
        for anime in anime_list:
            title = anime.find('h3',class_='lister-item-header').a.text
            link = anime.find('h3',class_='lister-item-header').a['href']
            year_span = anime.find('span', class_='lister-item-year text-muted unbold')
            pattern = re.compile(r"\d{4}")
            try:
                years = re.findall(pattern,year_span.text.split()[0])
                start_year = 'NA'
                end_year = 'No Finale yet'
                if len(years) == 1:
                    start_year = years[0]
                if len(years) == 2:
                    start_year = years[0]
                    end_year = years[1]
            except:
                print(f"Problem with {title}")
                print(years,title)
                pass
            p = anime.find_all('p',class_='text-muted text-small')
            pre_prod = 'No'
            try:
                certificate = p[0].find('span', class_='certificate').text
                runtime = p[0].find('span', class_='runtime').text
                genre = ",".join(p[0].find('span', class_='genre').text.split(',')[1:])
                ratings = anime.find('div', class_ = 'inline-block ratings-imdb-rating').text.strip()
                review = anime.find('p', class_='').text.strip()
                stars = ",".join(a.text for a in p[1].find_all('a'))
                votes = p[2].find('span',{'name':'nv'}).text
            except:
                pre_prod = 'Yes'
                certificate = 'NA'
                runtime = 'NA'
                genre = 'NA'
                ratings = 'NA'
                review = 'NA'
                stars = 'NA'
                votes = 'NA'
            finally:
                anime_data.append([title,pre_prod,link,start_year,end_year,certificate,runtime,genre,ratings,review,stars,votes])
        page_no += 1
        # d = pd.DataFrame(anime_data, columns = ['Title','Pre-Production','Link','start_year','end_year','certificate','runtime','genre','ratings','review','stars','votes'])
        # print(d.head())


        # print("Time delay : ")
        # time.sleep(random.randint(100,360))
    df = pd.DataFrame(anime_data, columns = ['Title','Pre-Production','Link','start_year','end_year','certificate','runtime','genre','ratings','review','stars','votes'])
    df.to_csv('Animes.csv')
if __name__ == '__main__':
    create_anime_list()
