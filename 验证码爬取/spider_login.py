import requests
from lxml import etree
from chaojiying_Python.chaojiying import Chaojiying_Client

# https://www.chaojiying.com/
class spider():
    def __init__(self):
        # 首页接口
        self.index_url = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx'
        # 登录接口
        self.url = 'https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx'
        self.data = {
            '__VIEWSTATE': 'A+G/ReN+RY7tmb3dYfItqHuqG25SwG/AifW+y1AaffWF3imnSc7Wlxemcb/J2hbOivInLSprYtKGYxTfUCldX6XABbN4kxPegc2OEWWiTojLm+a9BPgpYPo5nognErTWUbSuHCSjYD+jmFgVC0VbK26alXg=',
            '__VIEWSTATEGENERATOR': 'C93BE1AE',
            'from': 'http://so.gushiwen.cn/user/collect.aspx',
            'email': '1067930631@qq.com',
            'pwd': 'admin123.',
            'code': 'Q429',  # 验证码
            'denglu': '登录',
        }
        self.header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }

        # 实例化
        self.s = requests.session()

    # 向首页发请求，获得图片链接
    def get_data(self):
        r = self.s.get(self.index_url, headers = self.header)
        # print(r.text)
        xml = etree.HTML(r.text)
        img_src = "https://so.gushiwen.cn/"+xml.xpath('//img[@id="imgCode"]/@src')[0]
        # print(img_src)
        img_data = self.s.get(img_src,headers = self.header).content
        with open('code.png', 'wb') as f:
            f.write(img_data)

        chaojiying = Chaojiying_Client('admin6715', 'admin6715.', '959760')
        im = open('code.png', 'rb').read()
        reslut = chaojiying.PostPic(im, 1004)
        # print('111',reslut['pic_str'])
        return reslut

    # 提交验证码给登录接口
    def post_img(self):
        result = self.get_data()
        # print('222',result)
        self.data['code'] = result['pic_str']
        long_data = self.s.post(url=self.url, headers = self.header,data=self.data).text
        print(long_data)

if __name__ == '__main__':
    s = spider()
    # s.get_data()
    s.post_img()

# 关联规则概念三本，





