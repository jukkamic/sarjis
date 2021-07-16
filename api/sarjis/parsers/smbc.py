from .common import Common
from bs4 import BeautifulSoup

class SmbcParser():

    def parse(path, title_in_html=""):
        if path != "/":
            path = "/comic/" + path.split('/')[-1]
        page_html = Common.fetchPage("www.smbc-comics.com", path)

        soup = BeautifulSoup(page_html, features="lxml")

        full_title = soup.find('title').contents[0]
        title = full_title[len("Saturday Morning Breakfast Cereal -"):]

        alt = soup.find('div', {"id":"cc-comicbody"}).find('img')['title']

        perm_link = soup.find('input', {"id":"permalinktext"})['value']
        perm_link = "https://" + perm_link.split("//")[-1]

        img_url = soup.find('div', {"id":"cc-comicbody"}).find('img')['src']
        img_file = Common.saveImage(img_url)

        prev_element = soup.find('a', {"class":"cc-prev"})
        next_element = soup.find('a', {"class":"cc-next"})

        if prev_element is not None:  
            prev_link = prev_element['href']
        else:
            prev_link = None

        if next_element is not None:  
            next_link = next_element['href']
        else:
            next_link = None

        return {'perm_link': perm_link,
                'img_url': img_url,
                'img_file': img_file,
                'title': title,
                'alt': alt,
                'prev_link': prev_link,
                'next_link': next_link,
                'display_name': 'Saturday Morning Breakfast Cereal',
                'display_source': 'smbc-comics.com'}
