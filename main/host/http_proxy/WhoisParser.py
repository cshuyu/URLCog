import bs4
import re
import time

class WhoisParser(object):

    def __init__(self):
        pass

    def to_string(self,text):
        num_ip,reg_time,country,registrar=self.parse(text)
        return str(num_ip)+','\
               +str(reg_time)+','\
               +str(country)+','\
               +str(registrar)


    def parse(self,text):
        # returns num_ip,reg_time,country
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
        time_str = self.find(soup,'Registered On')
        return time_str

    def country(self,soup):
        # find country
        return self.find(soup,'Country').upper()

    def registrar(self,soup):
        # find registrar
        text = self.find(soup,'Name').upper()
        text = text.replace(',','')
        return text