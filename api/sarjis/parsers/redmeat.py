from .common import Common
from bs4 import BeautifulSoup

class RedmeatParser():
    
    def parse(path, title_in_html=""):
        if path == "/":
            path = "/max-cannon/FreshMeat"
        page_html = Common.fetchPage("www.redmeat.com", path)

        soup = BeautifulSoup(page_html, features="lxml")

        if path == "/max-cannon/FreshMeat":
            link_attr = soup.find("link", attrs={"rel": "canonical"})
            perm_link = link_attr["href"].split("redmeat.com")[-1]
            return RedmeatParser.parse(perm_link)

        perm_link = path
        next_link_tag = soup.find("a", attrs={"class": "next"})
        prev_link_tag = soup.find("a", attrs={"class": "prev"})

        next_link = None
        prev_link = None
        if next_link_tag:
            next_link = next_link_tag["href"].split("redmeat.com")[-1]
        if prev_link_tag:
            prev_link = prev_link_tag["href"].split("redmeat.com")[-1]

        img_div = soup.find("div", attrs={"class": "comicStrip"})
        img_url = img_div.find("img")["src"]
        img_file = Common.saveImage(img_url)

        date_publish = soup.find("meta", attrs={"name": "date"})["content"].split(" ")[0]

        return {'perm_link': perm_link,
                'img_url': img_url,
                'img_file': img_file,
                'title': "",
                'alt': "",
                'date_publish': date_publish,
                'prev_link': prev_link,
                'next_link': next_link,
                'display_source': 'redmeat.com',
                'display_name': "Red Meat"
                }
