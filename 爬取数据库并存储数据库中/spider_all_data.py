import requests
from lxml import etree
import pymysql

class Spiderqinghua():
    def __init__(self):
        '''数据库配置信息改成自己的'''
        # 连接数据       用户名              密码       数据库名
        self.db = pymysql.connect(user='root', password='admin', database='spider', charset='utf8')
        self.cursor = self.db.cursor()  # 获取操作游标

    # 发起请求
    def get_data(self, url):
        response = requests.get(url)
        response.encoding = response.apparent_encoding # 获取网页本身编码
        return response.text

    # 获取所有类别url  # 获取入口为：http://www.ainicr.cn/tab/ 不清楚页面的可以访问这个链接去看看
    def get_all_url(self, data):
        xml_data = etree.HTML(data)
        # global names
        all_urls = xml_data.xpath('//ul[@class="tj_two"]/li/a/@href')
        all_names = xml_data.xpath('//ul[@class="tj_two"]/li/a/text()')
        print(all_urls,all_names)
        return all_urls, all_names

    # 获取列表页url
    def get_list_url(self, url):
        all_html = self.get_data(url)
        xml = etree.HTML(all_html)
        hrefs = xml.xpath('//div[@class="item"]/div/a/@href')  # 获取列表页详情url
        return hrefs

    # 解析每个列表页url的情话详情内容
    def parse_data(self, url):
        qinghua_html = self.get_data(url)  # 请求每个url，以获取网页文本
        xml = etree.HTML(qinghua_html)
        contents = xml.xpath('//div[@class="stbody "]/p[1]/text()|//div[@class="stbody first"]/p[1]/text()')
        for content in contents:
            print(content)
            print('-----' * 10)
            # print(names)
            self.create_table(names, content)

    # 建表 提交数据
    def create_table(self, name, qinghua):
        # 1.使用命令创建表
        c_sql = 'create table {}(id int not null auto_increment,text longtext not null,primary key(id))'.format(name)
        try:
            self.cursor.execute(c_sql)  # mysql是不可以创建重复表名的 所以交给异常处理捕捉
        except Exception as e:
            print("表名重复，未重复创建，具体以报错编码为准：case: %s" % e)

        # 2.使用命令写入数据
        sql = 'insert into %s(text) values("%s")'  # sql语句
        # self.cursor.execute(sql % (name, str(qinghua)))  # 执行SQL语句（常规写法）
        '''
        按照常规写法执行56行代码会出现如下报错信息：
        pymysql.err.ProgrammingError: (1064, 'You have an error in your SQL syntax; check 
        the manual that corresponds to your MySQL server version for the right syntax to use
         near \'我爱你"。")\' at line 1')
         
        这是因为要保存的数据本身也采用了多重引号，导致sql出现语法错误,escape_string()函数进行特殊字符的转义处理（见65行）
        '''
        self.cursor.execute(sql % (name, self.db.escape_string(str(qinghua))))  # 执行SQL语句
        self.db.commit()  # 提交

    def main(self):
        all_data = self.get_data(url)
        all_urls, all_names = self.get_all_url(all_data)  # 获得类别对应的详情URL
        global names  # 将类别名声明成全局变量，方便create_table方法调用的时候传实参
        for urls, names in zip(all_urls, all_names):
            print('=======类别名字{}，url为{}'.format(names, urls))
            list_links = self.get_list_url(urls)  # 获得每个类别的所有一级列表栏URL
            for links in list_links:
                # 类别页面访问的端午节链接访问不了，找出正确链接替换上去即可
                if 'indexnew.php' in links:
                    links = 'http://www.ainicr.cn/index.php?s=80&module=sentence&view=tab&cm=view&aid=405'
                # http://www.ainicr.cn/indexnew.php?s=80&module=sentence&view=label&cm=view&aid=6441
                # 端午节正确链接：http://www.ainicr.cn/index.php?s=80&module=sentence&view=tab&cm=view&aid=405
                print("列表栏URL:", links)
                self.parse_data(links)

if __name__ == '__main__':
    abc = Spiderqinghua()
    url = 'http://www.ainicr.cn/tab/'
    abc.main()
