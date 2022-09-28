from .common import Common
from bs4 import BeautifulSoup
import logging

log = logging.getLogger('sarjis')

class LuontoParser:

    def parse(path, title_in_html=""):
        # Always fetch page from base path "/aihe/Kamala_luonto".
        # If given path is "/" look for the first article class="card card--scrollable-image".
        # If another path is given search for it in the list at "/".
        # In both cases find prev link info from the next card.
        # TODO: A plan for traversing comics back further than page 1.
        page_html = Common.fetchPage("www.ksml.fi", "/aihe/Kamala_luonto")

        soup = BeautifulSoup(page_html, features="lxml")

        grid_column = soup.find("h1", text=title_in_html, attrs={'class': 'diks-title'}).find_parent("div")

        if path == "/":
            first_card = grid_column.find('article', attrs={'class': 'diks-card diks-card--scrollable-image'})
            perm_link = first_card.find('a', attrs={'class': 'diks-card__link'})['href']
            return LuontoParser.parse(perm_link, title_in_html)

        perm_link = path
        this_card = grid_column.find('a', href=path, attrs={'class': 'diks-card__link'}).find_parent('article', attrs={'class': 'diks-card diks-card--scrollable-image'})

        older_card = None
        newer_card = None
        try:
            older_card = this_card.find_next_sibling('article', attrs={'class': 'diks-card diks-card--scrollable-image'})
            newer_card = this_card.find_previous_sibling('article', attrs={'class': 'diks-card diks-card--scrollable-image'})
        except AttributeError as ae:
            log.error("Finding sibling for card: ", this_card)
            log.error(ae)

        next_link = None
        prev_link = None

        if newer_card is not None:
            next_link = newer_card.find('a', attrs={'class': 'diks-card__link'})['href']
        if older_card is not None:
            prev_link = older_card.find('a', attrs={'class': 'diks-card__link'})['href']

        date_publish = this_card.find('time')['datetime'].split('T')[0]

        img_url = this_card.find("img", attrs={"class": "diks-card__image"})["src"]
        img_file = Common.saveImage(img_url)

        return {'perm_link': perm_link,
                'img_url': img_url,
                'img_file': img_file,
                'title': "",
                'alt': "",
                'prev_link': prev_link,
                'next_link': next_link,
                'date_publish': date_publish,
                'display_source': 'ksml.fi',
                'display_name': "Kamala luonto"
                }
