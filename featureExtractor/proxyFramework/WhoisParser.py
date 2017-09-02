import bs4
import re

class WhoisParser(object):

    def __init__(self):
        pass

    def parse(self,text):
        # create soup
        soup = bs4.BeautifulSoup(text, "html.parser")
        return self.num_ip(soup),self.reg_time(soup),self.country(soup),self.registrar(soup)

    def num_ip(self,soup):
        # find number of ip addresses
        return len(soup.find_all('a', href=re.compile('ip-address')))

    def find(self,soup,name):
        # method of finding
        tag = soup.find('div',text=name)
        attr = ''
        if tag:
            attr = tag.find_next_sibling().text
        return attr

    def reg_time(self,soup):
        # find registration time
        return self.find(soup,'Registered On')

    def country(self,soup):
        # find country
        return self.find(soup,'Country')

    def registrar(self,soup):
        # find registrar
        return self.find(soup,'Name').lower()
