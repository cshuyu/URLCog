import bs4

def get_ip(html):
    soup = bs4.BeautifulSoup(html,"html.parser")
    try:
        ip = soup.find('td',text='A').next_sibling.next_sibling.next_sibling.text
    except Exception as e:
        print(str(e))
        ip = None
    return ip
    
