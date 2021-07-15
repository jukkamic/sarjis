from .common import Common
from bs4 import BeautifulSoup

class XkcdParser():
    def parse(path):
        page_html = Common.fetchPage("xkcd.com", path)
            
        start_perm_link = page_html.find("Permanent link to this comic:") + 30
        end_perm_link = page_html.find("<br", start_perm_link)
        perm_link = page_html[start_perm_link:end_perm_link]
        
        start_img = page_html.find("Image URL (for hotlinking/embedding):") + 38
        end_img = page_html.find(".png", start_img)

        img_url = page_html[start_img:end_img + 4]
        img_file = Common.saveImage(img_url)

        soup = BeautifulSoup(page_html, features="lxml")

        title = soup.find('div', {"id":"ctitle"}).contents[0]
        alt = soup.find('div', {"id":"comic"}).find('img')['title']

        prev_element = soup.find('ul', {"class":"comicNav"}).find('a', {"rel":"prev"})
        if prev_element is not None:
            prev_link = prev_element['href']
        else:
            prev_link = None

        next = soup.find('ul', {"class":"comicNav"}).find('a', {"rel":"next"})['href']
        if next == "#":
            next_link = None
        else:
            next_link = next

        return {'perm_link': perm_link,
                'img_url': img_url,
                'img_file': img_file,
                'title': title,
                'alt': alt,
                'prev_link': prev_link,
                'next_link': next_link,
                'display_name': 'xkcd',
                'display_source': 'xkcd.com'}
