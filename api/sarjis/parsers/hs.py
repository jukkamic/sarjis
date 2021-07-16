from .common import Common
from bs4 import BeautifulSoup

class HsParser():
    
    def parse(path, comicTitle:str):
        if path == "/":
            path = "/sarjakuvat/"
        page_html = Common.fetchPage("www.hs.fi", path)

        soup = BeautifulSoup(page_html, features="lxml")

        if path == "/sarjakuvat/":
            perm_link = getPermLinkFromHS(soup, comicTitle)
            return HsParser.parse(perm_link, comicTitle)

        perm_link = path

        next_link, prev_link = handleLinksInHS(soup)

        figure_tag = soup.find("figure", attrs={"class": "cartoon image scroller"})
        if not figure_tag:
            figure_tag = soup.find("figure", attrs={"class": "cartoon image"})        
        
        img_url= "https:" + figure_tag.find("img")["data-srcset"]
        img_url=img_url.split(" ")[0]
        img_file = Common.saveImage(img_url)

        date_publish = figure_tag.find("meta", attrs={"itemprop": "datePublished"})["content"]

        return {'perm_link': perm_link,
                'img_url': img_url,
                'img_file': img_file,
                'title': "",
                'alt': "",
                'prev_link': prev_link,
                'next_link': next_link,
                'date_publish': date_publish,
                'display_source': 'hs.fi',
                'display_name': comicTitle
                }

def handleLinksInHS(soup):
    next_link = soup.find("a", attrs={"class": ["next"]})["href"]
    if next_link == "#":
        next_link = None

    prev_link = soup.find("a", attrs={"class": ["prev"]})["href"]
    if prev_link == "#":
        prev_link = None
    return next_link,prev_link

def getPermLinkFromHS(soup, comicTitle:str):
    cartoons = soup.find("div", attrs={"id": "page-main-content"})
    fp_div = cartoons.find('span', text=comicTitle, attrs = {"class": "title"}).find_parent("div")
    perm_link = fp_div.find(('a'))['href']
    return perm_link