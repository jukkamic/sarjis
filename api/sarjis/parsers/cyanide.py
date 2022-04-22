from .common import Common
from bs4 import BeautifulSoup

class CyanideParser():
    def parse(path, title_in_html=""):
        if path == "/":
            path = "/comics/latest/"
        page_html = Common.fetchPage("explosm.net", path)
        soup = BeautifulSoup(page_html, features="lxml")

        if path == "/comics/latest/":
            link_element = soup.find("a", attrs={"id": "comic-social-link"})
            if not link_element:
                raise Exception("Element for permalink was not found.") 
            perm_link = link_element["href"]
            return CyanideParser.parse(perm_link)

        perm_link = path

        link_container = soup.find("div", attrs={"id":"comic-under"})
        next_link_tag = link_container.find("a", attrs={"class": "nav-next"})
        prev_link_tag = link_container.find("a", attrs={"class": "nav-previous"})

        next_link = None
        prev_link = None
        if next_link_tag and next_link_tag.has_attr('href'):
            next_link = next_link_tag["href"]
        if prev_link_tag and prev_link_tag.has_attr('href'):
            prev_link = prev_link_tag["href"]

        img_url = soup.find("img", attrs={"id": "main-comic"})["src"]
        img_url = "http:" + img_url.split('?')[0]
        img_file = Common.saveImage(img_url)

        return {'perm_link': perm_link,
                'img_url': img_url,
                'img_file': img_file,
                'title': "",
                'alt': "",
                'prev_link': prev_link,
                'next_link': next_link,
                'display_source': 'explosm.net',
                'display_name': "Cyanide and Happiness"
                }
