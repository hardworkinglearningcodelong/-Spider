import requests
from jsonpath import jsonpath
import re
import sys
import time
import random
import json

'''
移动端访问链接：https://m.weibo.cn/detail/4813628149072458

一级评论接口：https://m.weibo.cn/comments/hotflow?id=4813628149072458&mid=4813628149072458&max_id_type=0
            -- 参数      id: 4813628149072458   # 博主ID
                        mid: 4813628149072458  # 博主ID
                        max_id_type: 0
                        max_id: 13883307764046392  # 翻页ID  从第2页开始出现的 （在上一页一级评论接口中可以找到）

二级：https://m.weibo.cn/comments/hotFlowChild?cid=4813628329693567&max_id=0&max_id_type=0
     -- 参数     cid: 4813628329693567  # 楼主（一级评论的跟评） （一级评论接口中可以找到）
                max_id: 0    #  二级翻页ID （上一页二级评论接口中可以找到）
                max_id_type: 0  

测试链接：https://m.weibo.cn/detail/4864041232896092
'''


class WeiBo():
    def __init__(self):
        self.one_url = 'https://m.weibo.cn/comments/hotflow'
        self.one_data = {
            'id': '4813628149072458',  # 博主ID
            'mid': '4813628149072458',  # 博主ID
            'max_id_type': '0',
            'max_id': None,  # 一级翻页ID 第一页的时候无值
        }

        self.two_url = 'https://m.weibo.cn/comments/hotFlowChild'
        self.two_data = {
            'cid': '4813628329693567',  # 楼主（一级评论的跟评） （一级评论接口中可以找到）
            'max_id': '0',  # 二级翻页ID （上一页二级评论接口中可以找到）
            'max_id_type': '0'  # 可变 规律同max_id相同
        }
        self.headers = {
            'referer': 'https://m.weibo.cn/detail/4813628149072458',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            # 登录后的cookie
            'Cookie': 'WEIBOCN_FROM=1110005030; __bid_n=188b7ef5179e6369a94207; FPTOKEN=crNJdsvZwwGF7dp2IPNpPQfcb8QXfJcGqmdrORkyZDx1InnMS5HmnAi2IuK/+GpaFRGA9SsxzhVt1I6QlRCtoWJsIFKbbc8//DeUCm0HH9ux6X85QM+Z3WBbGns26hiiQngHN+M5q+ErW1eifOLk++KasqWhbWrd12AHMF7vC/3qXfLfRN60SEVuv1ZGCnrBIc3lN1sba2e0UzVGEzYejWmJ/yzCNkUZ1qZHPSNvEzGfJlYhJGxDiyyBInzi/cTWyk1g988msn9UMRE3GBjWIcZXsqOl0HbbsOz5AYS+n1b86VqgY4eVk3EB/Dr9Fgkl2UBcstP5NcEJ9MXcHyZDfRsXbz/rGPbnYsrT7iZxjwGn4gnTqnzQ/HZsyaVvGf1gxf3oEB3SwBHvlflbg7KxXQ==|G4pgWxSL7Ti7lQoJilvXBEq0Vs37iI4r+CsQg3BKI2U=|10|6f811a8a83e72fbe3ec90c6845e372b0; _T_WM=22248193581; M_WEIBOCN_PARAMS=oid%3D4813628149072458%26luicode%3D20000061%26lfid%3D4813628149072458%26uicode%3D20000061%26fid%3D4813628149072458; MLOGIN=1; SCF=AkYYFk70crAYROKfk6SUopCK_fVD7Tu5nSTQdkf6622fe9ZFinqh_rcdybf7KKRzXpwYx4SRaQis4E1KLR2RTGs.; SUB=_2A25JjS7hDeRhGeFJ71UT8S_OwjqIHXVrcbKprDV6PUJbktAGLUnckW1Nf8RTnkyqITgJ8Sa9wouEZCxJoHI5Nn0D; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF_IbR1VnBGsR3IZdB7J.Ey5JpX5K-hUgL.FoMNShMEeK2E1Kq2dJLoIEnLxK-L1hqL1K.LxKMLB.zL1K.LxKnL1hMLB-2LxK-LBoMLBo27S05N; SSOLoginState=1686724273; ALF=1689316273; XSRF-TOKEN=65af2d; mweibo_short_token=d8dc535184'}
    # 1.1 爬取一级评论
    def get_one_data(self, url, data):
        response = requests.get(url=self.one_url, params=self.one_data, headers=self.headers)
        json_data = response.json()
        # 1.2 解析内容
        one_name = jsonpath(json_data, '$..data[0:19].user.screen_name')
        one_text = jsonpath(json_data, '$..data[0:19].text')
        # print(one_name)
        # print(one_text)

        # 3.3 解析跟评ID
        cid = jsonpath(json_data, '$..data[0:19].rootid')  # Flase
        # print("跟评ID:", cid)
        for one_names, one_texts, cids in zip(one_name, one_text, cid):
            content = re.sub('<.*?>', '', one_texts)
            print('------一级评论--------------')
            print(one_names)
            # print(one_texts)
            print(content)
            print("跟评ID:", cids)
            # 5.异常处理一下跟评（有些一级评论无跟评）
            try:
                # 3.4 切换跟评ID
                self.two_data['cid'] = cids
                # 3.5 调用二级请求的方法 获得二级评论
                self.get_two_data()
            except:
                self.two_data['max_id'] = 0
                print('当前一级评论已经无跟评~将继续爬取下一个一级评论')

        # by = response.text.encode()  # .decode("unicode_escape")
        # print(by.decode("unicode_escape"))
        # print(json.loads(response.text))

        # 2.1开始翻页（一级）
        # 2.2 经过分析 max_id为翻页参数 在上一页的健名为max_id里
        max_id = jsonpath(json_data, '$..data.max_id')[0]  # 解析翻页ID
        print("一级翻页的参数ID：", max_id)

        # 2.3 更改一级请求参数
        self.one_data['max_id'] = max_id
        # 2.5 判断翻页结束
        if max_id == 0:
            sys.exit('该用户的一级评论已经爬完~')
        else:
            # 2.4 递归调用 实现翻页
            self.get_one_data(self.one_url, self.one_data)
            time.sleep(2.5)

    # 3.1 获取二级评论
    def get_two_data(self):
        response = requests.get(url=self.two_url, params=self.two_data, headers=self.headers)
        json_data = response.json()
        # 3.2 解析内容
        two_name = jsonpath(json_data, '$..data..screen_name')
        two_text = jsonpath(json_data, '$..data..text')
        for two_names, two_texts in zip(two_name, two_text):
            content = re.sub('<.*?>', '', two_texts)
            print('\t\t', '------二级评论--------------')
            print('\t\t\t\t', two_names, content)
        # 4.1 开始二级翻页
        # 4.2 解析二级的翻页参数
        two_max_id = jsonpath(json_data, '$..max_id')[0]
        print('\t\t\t', "二级的翻页参数为：", two_max_id)
        if two_max_id == 0:
            print("参数", self.two_data)
            print('!!!!该二级评论爬取完~max_id为{}'.format(two_max_id))
            # 4.5 二级翻页结束之后将max_Id重新赋值为0，便于下一条一级评论的二级跟评爬取
            self.two_data['max_id'] = 0
            print("重置后的参数", self.two_data)
        else:
            # 4.3 修改参数
            self.two_data['max_id'] = two_max_id
            print("参数", self.two_data)
            # 4.4 递归调用 实现翻页
            self.get_two_data()
            t = random.randint(2, 6)
            time.sleep(t)

    def man(self):
        self.get_one_data(self.one_url, self.one_data)
        t = random.randint(2, 4)
        time.sleep(t)
if __name__ == '__main__':
    w = WeiBo()
    w.man()
