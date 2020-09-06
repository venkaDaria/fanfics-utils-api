from lxml import html
import requests

def improve(strng):
    return strng.replace('\n', '').replace('\r', '').strip()

cookies = {
    'pf': '<PASTE pf>',
    'cookie_pf_user': '<PASTE cookie_pf_user>'
}

#url = 'https://fanfics.me/favorite?action=subscribed_fics'
#url = 'https://fanfics.me/favorite?action=haveread&sort=date_mark'

result = []
#page = requests.get(url, cookies=cookies)
#tree = html.fromstring(page.content)
tree = html.parse('example.html')
books = tree.xpath('//table[@class="FicTbl"]')

for book in books:
    info = book.xpath('.//td[@class="FicTbl_meta"]')[0]
    authors = info.xpath('.//a[@class="user"]/text()') # './/a[contains(@href,"ftf_author")]/text()'
    authors_str = improve(', '.join([author.strip() for author in authors])).strip(', ')

    record = {
        'author': authors_str,
        'name': book.xpath('.//div[@class="FicTable_Title"]/h4/a/text()')[0],
        'fanfiction': ', '.join(info.xpath('.//span[@data-show-fandom]/a/text()')), # './/a[contains(@href,"ftf_fandom")]/text()'
        'pairing': ', '.join(info.xpath('.//span[@class="FicTable_Paring"]/text()')), # .//span[@class="FicTable_Paring"]/text()
        'description': improve(book.xpath('.//td[@class="FicTbl_sammary"]/text()')[0])
    }

    result.append(record)

record_str = '{} - {} #fanfics {} \r ({}) \r {}'
fanf_str = '#fanfiction ({})'

with open('f-likes.txt', 'w', encoding="utf-8") as f:
    for record in result:
        fanfiction = '' if 'Ориджиналы' in record['fanfiction'] else fanf_str.format(record['fanfiction'])
        f.write(record_str.format(record['author'], record['name'], fanfiction, record['pairing'], record['description']) + '\n') 