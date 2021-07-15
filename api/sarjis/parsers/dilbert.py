from .common import Common
from bs4 import BeautifulSoup

class DilbertParser:

    def parse(path, title_in_html=""):
        page_html = Common.fetchPage("dilbert.com", path)

        soup = BeautifulSoup(page_html, features="lxml")

        meta_tag = soup.find("div", attrs={"class": "meta-info-container"})

        if path == "/":
            first_link = meta_tag.find('a', attrs={'class': 'img-comic-link'})
            perm_link = first_link['href']
            return DilbertParser.parse(perm_link)

        perm_link = path
        next_link = None
        prev_link = None

        next_link_tag = soup.find("a", attrs={"class": "js-load-comic-newer"})
        prev_link_tag = soup.find("a", attrs={"class": "js-load-comic-older"})
        if next_link_tag:
            next_link = next_link_tag["href"]
        if prev_link_tag:
            prev_link = prev_link_tag["href"]

        span_tag = meta_tag.find("span", attrs={"class": "comic-rating"})
        date_publish = span_tag.find("div")["data-date"]

        img_url = meta_tag.find("img", attrs={"class": "img-responsive img-comic"})["src"]
        img_file = Common.saveImage(img_url)

        return {'perm_link': perm_link,
                'img_url': img_url,
                'img_file': img_file,
                'title': "",
                'alt': "",
                'prev_link': prev_link,
                'next_link': next_link,
                'date_publish': date_publish,
                'display_source': 'dilbert.com',
                'display_name': "Dilbert"
                }
