from lxml import html
import requests

def improve(strng):
    return strng.replace('\n', '').replace('\r', '').strip()

cookies = {'PHPSESSID': '<PASTE PHPSESSID>'}
url = 'https://ficbook.net/home/liked_fanfics?p={}'
#url = 'https://ficbook.net/collections/9593?p={}'

result = []
for p in range(1, 262):
    page = requests.get(url.format(p), cookies=cookies)
    tree = html.fromstring(page.content)

    books = tree.xpath('//div[@class="description"]')
   
    for book in books:
        info = book.xpath('.//dl[@class="info"]')[0]
        authors = book.xpath('.//span[@class="author"]/a/text()')
        authors_str = improve(', '.join([author.strip() for author in authors])).strip(', ')

        record = {
            'author': authors_str,
            'name': book.xpath('.//a[@class="visit-link"]/text()')[0],
            'fanfiction': ', '.join(info.xpath('.//dd[1]/a/text()')),
            'pairing': ', '.join(info.xpath('.//dd[2]/a/text()')),
            'description': improve(book.xpath('.//div[@class="fanfic-description"]/div/text()')[0])
        }

        result.append(record)

record_str = '{} - {} #ficbook {} \r ({}) \r {}'
fanf_str = '#fanfiction ({})'

with open('f-likes.txt', 'w', encoding="utf-8") as f:
    for record in result:
        fanfiction = '' if 'Ориджиналы' in record['fanfiction'] else fanf_str.format(record['fanfiction'])
        f.write(record_str.format(record['author'], record['name'], fanfiction, record['pairing'], record['description']) + '\n') 