import json
import requests
from bs4 import BeautifulSoup


def fetch_movie_data(url):

    response = requests.get(url)

    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    return soup


def extract_movie_data(soup, url):

    year_tags = soup.select('a.year-link')

    movie_data = []

    for year_tag in year_tags:

        year = year_tag.text.strip()

        response = requests.get(url, params={'ajax': 'true', 'year': year})

        json_content = response.json()

        movie_data.extend(json_content)

    return movie_data


if __name__ == "__main__":

    url = 'https://www.scrapethissite.com/pages/ajax-javascript/'

    soup = fetch_movie_data(url)

    movie_data = extract_movie_data(soup, url)

    print(json.dumps(movie_data[:5], indent=4))