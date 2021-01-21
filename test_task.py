import os
import requests
from bs4 import BeautifulSoup
import csv


def parse_html_file(html_file_name):
    """ This function parse html file with films top"""

    with open(html_file_name) as fp:
        soup = BeautifulSoup(fp, 'lxml')

    films_info = soup.find_all('td', class_='titleColumn')

    films_top = {}
    for n, f in enumerate(films_info, start=1):
        film_name = f.find('a').text

        films_top.update({n: f'{film_name}'})
    return films_top


def name_to_params(name):
    """Replace spaces, colons for params required format"""
    params_str = name.replace(' ', '+').replace(':', '%3A')
    return params_str


def get_json_films_detail(films):
    """This function get films detail,
       unfortunately here is the synchronous code,
       the best solution is to use aiohttp, and get requests asynchronously"""

    params = {'apikey': os.getenv('APIKEY') or 'd5f853ed'}

    json_data = []
    for number, name in films.items():
        url = "http://www.omdbapi.com/?t=" + f'{name_to_params(name)}'

        res = requests.get(url, params=params)

        if res.status_code != 200:
            print('Error, API service is not available')
            continue
        film_detail = res.json()
        film_detail.update({'Order': number})

        json_data.append(film_detail)

    return json_data


def write_to_csv(json_data):
    """This function write films detail data to csv file"""

    with open("test.csv", 'w') as out_file:
        csv_w = csv.writer(out_file)

        # Code below write header for csv file
        csv_w.writerow([key for key in json_data[0].keys()])

        for i in json_data:
            csv_w.writerow([i[key] for key in i.keys()])


if __name__ == '__main__':

    print('Start')
    films_top = parse_html_file(os.getenv('HTML_FILE_PATH') or
                                'imdb_most_popular_movies_dump.html')

    print('Requesting for details, it will take 1-2 minute')
    detail_films = get_json_films_detail(films_top)

    write_to_csv(detail_films)
    print('All is done, open csv file in current dir')
    print('Have a nice day!')
