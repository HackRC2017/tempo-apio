import copy
import itertools
import json
import os
import random

import requests


_articles = []
ARTICLES_FILE = 'articles.json'
THEMES_BLACKLIST = [14, 16, 21, 23]


def _is_valid_article(article):
    if article['contentType']['name'] == 'Nouvelle':
        return True
    return False


def load_articles(number=100, from_file=False):
    global _articles
    if from_file and os.path.isfile(ARTICLES_FILE):
        with open(ARTICLES_FILE) as f:
            _articles = json.load(f)
        return len(_articles)
    themes = _get_theme_lineups()
    loaded_number = 0
    for i in itertools.cycle(range(len(themes))):
        try:
            _articles.append(next(themes[i]['generator']))
            loaded_number += 1
            print(loaded_number)
        except StopIteration:
            themes[i]['generator'] = _get_theme_articles(themes[i]['href'])
        if len(_articles) == number:
            break
        if not list(filter(lambda x: x is not None, themes)):
            break
    with open(ARTICLES_FILE, 'w') as f:
        json.dump(_articles, f)
    return loaded_number


def _get_theme_articles(href):
    print(href)
    r = requests.get(href)
    for article in r.json()['pagedList']['items']:
        if _is_valid_article(article):
            yield article
    if r.json()['pagedList'].get('nextPageLink'):
        yield from _get_theme_articles(r.json()['pagedList']['nextPageLink']['href'])


def _get_theme_lineups():
    theme_lineups = []
    with open('themes.json') as f:
        themes = json.load(f)['themes']
    random.shuffle(themes)
    themes = [t for t in themes if t['id'] not in THEMES_BLACKLIST]
    for theme in themes:
        theme_lineups.append({
            'href': theme['lineupLink']['href'],
            'generator': _get_theme_articles(theme['lineupLink']['href']),
        })
    return theme_lineups


def get_articles(number):
    global _articles
    if not _articles:
        load_articles(number=number, from_file=False)
    articles = _articles[:number]
    _articles = _articles[number:]
    return articles
