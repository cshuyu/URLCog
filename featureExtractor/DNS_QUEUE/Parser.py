import bs4
import codecs

def parser(html):
    dic = {}
    soup = bs4.BeautifulSoup(html, 'html.parser')
    for result in soup.select('div.result'):
        for br in result.findAll('br'):
            br.extract()
        for ip in result.children:
            if ip != '-':
                dic[ip] = 1
    return len(dic)
