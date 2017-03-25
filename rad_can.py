import copy
import itertools
import json
import random

import requests


_theme_articles = []


def is_valid_article(article):
    if article['contentType']['name'] == 'Nouvelle':
        return True
    return False


def get_articles(max_number):
    global _theme_articles
    articles = []
    for i in itertools.cycle(range(len(_theme_articles))):
        try:
            articles.append(next(_theme_articles[i]['generator']))
            print('got article')
        except StopIteration:
            _theme_articles[i]['generator'] = \
                get_theme_articles(_theme_articles[i]['href'])
        if len(articles) == max_number:
            break
        if not list(filter(lambda x: x is not None, _theme_articles)):
            break
    return articles


def get_theme_articles(href):
    r = requests.get(href)
    print(href)
    for article in r.json()['pagedList']['items']:
        if is_valid_article(article):
            yield article
        else:
            print('not valid')
    if r.json()['pagedList'].get('nextPageLink'):
        yield from get_theme_articles(r.json()['pagedList']['nextPageLink']['href'])


def load_theme_lineups():
    global _theme_articles
    _theme_articles = []

    with open('themes.json') as f:
        themes = json.load(f)['themes']

    random.shuffle(themes)

    for theme in themes:
        _theme_articles.append({
            'href': theme['lineupLink']['href'],
            'generator': get_theme_articles(theme['lineupLink']['href']),
        })
