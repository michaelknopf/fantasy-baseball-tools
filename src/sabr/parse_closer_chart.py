import requests
from bs4 import BeautifulSoup

closer_chart_url = "https://www.espn.com/fantasy/baseball/flb/story?page=REcloserorgchart"


def get_closer_soup():
    closer_chart_html = requests.get(closer_chart_url).content
    return BeautifulSoup(closer_chart_html, 'html.parser')

def get_closers():
    soup = get_closer_soup()
    closers = {'closer': [], 'setup': []}
    for division in range(10):
        division_closers = get_pitchers(soup, column_selector(True, division))
        division_nexts = get_pitchers(soup, column_selector(False, division))
        closers.get('closer').extend(division_closers)
        closers.get('setup').extend(division_nexts)
    return closers

def column_selector(is_closer, division):
    col = 2 if is_closer else 4
    return f"#article-feed table > tbody tr:nth-child({division}) td:nth-child({col}) > div > a"

def get_pitchers(soup, col_selector):
    closer_ahrefs = soup.select(col_selector)
    return [{
        'link': ahref.get("href"),
        'name': ahref.text
    } for ahref in closer_ahrefs]

# article-feed > article:nth-child(1) > div > div.article-body > video1:nth-child(7) > aside > table > tbody
# article-feed > article:nth-child(1) > div > div.article-body > video1:nth-child(7) > aside > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > a
# article-feed > article:nth-child(1) > div > div.article-body > video1:nth-child(7) > aside > table > tbody > tr:nth-child(1) > td:nth-child(4) > div > a
