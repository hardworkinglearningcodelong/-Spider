import  requests
from lxml import etree
import pymysql
def get_data(url):
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
             }
    response=requests.get(url,headers=headers)

    return response.text

def parse_data(data):
    xml = etree.HTML(data)
    title=xml.xpath('//div[@class="title"]/a/text()')
    link=xml.xpath('//div[@class="title"]/a/@href')
    price=xml.xpath('//div[@class="totalPrice totalPrice2"]/span/text()')
    for titles,links,prices in zip (title,link,price):
        print(titles)
        print(links)
        print(prices+'万元')
        print(len(titles))
        create_tables(titles,links,prices)
        print('我是分隔符'.center(50,'&'))
def create_tables(title,link,price):
    db = pymysql.connect(user='root', password='123456', database='lianjia', charset='utf8')
    cursor = db.cursor()
    cursor.execute(
        "create table if not exists zufang (id int not null auto_increment,title longtext not null,link varchar(255) not null,price int not null)")
    cql='insert ignore into zufang(title,link,price) values (%s,%s,%s)'
    cursor.execute(cql,[str(title),link,price])
    db.commit()
    print('保存成功')
if __name__ == '__main__':
    for i in range(1,30):
        print('当前爬取第{}页'.format(i))
        URL=f'https://hz.lianjia.com/ershoufang/pg{i}/'
        html=get_data(URL)
        parse_data(html)

