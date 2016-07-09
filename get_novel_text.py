import urllib.request
from bs4 import BeautifulSoup
import re

def del_ruby_tag(s):
    if not '<ruby>' in s:
        return s
    else: 
        while '<ruby>' in s:
            s = s.replace('<ruby><rb>', '', 1)
            index1 = s.find('</rb><rp>')
            index2 = s.find('</rp></ruby>') + 12
            rm_text = s[index1:index2]
            s = s.replace(rm_text, '')
        return s
       #<ruby><rb>長保</rb><rp>（</rp><rt>ちょうほう</rt><rp>）</rp></ruby>

pattern = r'^<p id=.*>「(.*)」</p>$'
repatter = re.compile(pattern)

html = urllib.request.urlopen('https://kakuyomu.jp/works/4852201425154922583').read()
soup = BeautifulSoup(html)

lists = soup.find('ol', {'class':'widget-toc-items test-toc-items'})

urls = []
for l in lists.find_all('a'):
    urls.append('https://kakuyomu.jp' + l.get('href'))

for url in urls:
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html)
    
    text = soup.find('div', {'class':'widget-episodeBody js-episode-body'})

    for t in text.find_all('p'):
        try:
            print(del_ruby_tag(repatter.match(str(t)).group(1)))
        except:
            pass
    


