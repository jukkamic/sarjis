from .common import Common
from bs4 import BeautifulSoup

class PbfParser():
    
    def parse(path, title_in_html=""):
        if path != "/":
            path = "/comics/" + path.split("/")[-2] + "/"
        page_html = Common.fetchPage("pbfcomics.com", path)

        soup = BeautifulSoup(page_html, features="lxml")

        nav_tag = soup.find("div", attrs={"id": "pbf-bottom-pagination"})

        if path == "/":
            perm_link = nav_tag.find("a", attrs={"rel": "latest"})["href"]
            return PbfParser.parse(perm_link)

        title = soup.find("meta", {"property": "og:title"})["content"]

        perm_link = path
        next_link_tag = nav_tag.find("a", attrs={"rel": "next"})
        prev_link_tag = nav_tag.find("a", attrs={"rel": "prev"})

        next_link = None
        prev_link = None
        if next_link_tag:
            next_link = next_link_tag["href"]
        if prev_link_tag:
            prev_link = prev_link_tag["href"]

        img_url = soup.find("meta", attrs={"property": "og:image"})["content"]
        img_file = Common.saveImage(img_url)

        return {'perm_link': perm_link,
                'img_url': img_url,
                'img_file': img_file,
                'title': title,
                'alt': "",
                'prev_link': prev_link,
                'next_link': next_link,
                'display_source': 'pbfcomics.com',
                'display_name': "The Perry Bible Fellowship"
                }
