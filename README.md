# Oscar Winning Films: AJAX and Javascript - Walkthrough
> walkthrough for the web-scrapping exercise found on https://www.scrapethissite.com
## Step 0: Install necessary dependencies
### - Step 0.1: Create a virtual environment:
```bash 
python -m venv venv
```


### - Step 0.2: Activate the virtual environment:

***Windows***:	
```bash
venv\Scripts\activate
```

***Mac/Linux***:
```bash
source venv/bin/activate
```
### - Step 0.3: Install dependencies:
```bash
pip install requests beautifulsoup4
```
* * *
## Step 1: Get the Webpage HTML
Start by fetching the HTML content of the target webpage. We'll use the `requests` library to do this.

```python
import requests

# Define the URL of the webpage
url = 'https://www.scrapethissite.com/pages/ajax-javascript/'

# Send a GET request to fetch the webpage content
response = requests.get(url)

# Extract the HTML content from the response
html_content = response.text
```
* * *
## Step 2: Spot HTML Patterns

Inspect the HTML structure for any recurring patterns. It appears that each movie year is contained within `<a>` elements having the class ``"year-link"``.

```html
<div class="col-md-12 text-center">
  <h3>
    Choose a Year to View Films
  </h3>
  <a href="#" class="year-link" id="2015">2015</a>
  <a href="#" class="year-link" id="2014">2014</a>
  <a href="#" class="year-link" id="2013">2013</a>
  <a href="#" class="year-link" id="2012">2012</a>
  <a href="#" class="year-link" id="2011">2011</a>
  <a href="#" class="year-link" id="2010">2010</a>
</div>
<!--.col-->
```
* * *
## Step 3: Parse the HTML

We'll use ``BeautifulSoup``, to parse the HTML content and make it ready for extraction.

```python
from bs4 import BeautifulSoup

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')
```
* * *
## Step 4: Extract the Data

Having identified the pattern, we can gather all `<a>` elements with the class ``"year-link"`` as individual datasets. Then, we'll GET movie data for each year; from which we'll extract details like movie title, nominations, awards, etc...

```python
# Find all <a> elements with the class "year-link"
years_tags = soup.select('a.year-link')

movie_data = []

# Iterate through each <a> element for data extraction
for years_tag in years_tags:
  
    # Extract Year
    year = years_tag.text.strip()
    
    # Send a GET request to fetch the webpage content
    response = requests.get(url, params={ 'ajax': 'true', 'year': year})

    # Extract the JSON content from the response
    movie_data.extend(response.json)
```

* * *
### Put it all together:
```python
import json
import requests
from bs4 import BeautifulSoup


def fetch_movie_data(url):

    # Send a GET request to fetch the webpage content
    response = requests.get(url)

    # Extract the HTML content from the response
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Return the BeautifulSoup object
    return soup


def extract_movie_data(soup, url):

    # Select all <a> tags with class 'year-link'
    years_tags = soup.select('a.year-link')

    movie_data = []

    # Iterate through each <a> tag containing year data
    for year_tag in years_tags:
        # Extract year from the text of the <a> tag
        year = year_tag.text.strip()

        # Send a GET request to fetch the webpage content for the given year
        response = requests.get(url, params={'ajax': 'true', 'year': year})

        # Extract JSON content from the response
        json_content = response.json()

        # Add extracted movie data to the list
        movie_data.extend(json_content)

    return movie_data



url = 'https://www.scrapethissite.com/pages/ajax-javascript/'

soup = fetch_movie_data(url)

movie_data = extract_movie_data(soup, url)

print(json.dumps(movie_data[:5], indent=4))
```
### Outputs:
```json
[
    {
        "title": "Spotlight  ",
        "year": 2015,
        "awards": 2,
        "nominations": 6,
        "best_picture": true
    },
    {
        "title": "Mad Max: Fury Road ",
        "year": 2015,
        "awards": 6,
        "nominations": 10
    },
    {
        "title": "The Revenant   ",
        "year": 2015,
        "awards": 3,
        "nominations": 12
    },
    {
        "title": "Bridge of Spies",
        "year": 2015,
        "awards": 1,
        "nominations": 6
    },
    {
        "title": "The Big Short  ",
        "year": 2015,
        "awards": 1,
        "nominations": 5
    }
]
```
