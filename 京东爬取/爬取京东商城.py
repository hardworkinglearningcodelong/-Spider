from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait  #等待页面加载完毕，寻找某些元素
from selenium.webdriver.support import expected_conditions as EC  ##等待指定标签加载完毕
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd
from bs4 import BeautifulSoup
import sys
class Spider():
    def __init__(self):
        self.url = 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F%3Fcu%3Dtrue%26utm_source%3Dbaidu-pinzhuan%26utm_medium%3Dcpc%26utm_campaign%3Dt_288551095_baidupinzhuan%26utm_term%3D0f3d30c8dba7459bb52f2eb5eba8ac7d_0_d6d6256224af475b8e9e1934c6ee4956'
        # 设置无头模式
        self.opt = webdriver.ChromeOptions()  # 配置文件对象
        self.opt.add_experimental_option('excludeSwitches', ['enable-automation'])  # 写入参数
        self.browser = webdriver.Chrome(options=self.opt)
    def get_jd(self):
        self.browser.get(self.url)
        #选择qq登录
        self.browser.find_element(By.XPATH,'//*[@id="kbCoagent"]/ul/li[1]/a/span').click()
        # time.sleep(2)
        ###  页面嵌套
        # self.browser.switch_to.frame('ptlogin_iframe')
        # self.browser.find_element(By.XPATH,'//*[@id="switcher_plogin"]').click()#点击密码登录
        # user_text=self.browser.find_element(By.XPATH,'//*[@id="u"]')
        # password_text=self.browser.find_element(By.XPATH,'//*[@id="p"]')
        # user_text.send_keys('3035340572@qq.com')
        # password_text.send_keys('long459751')
        # self.browser.find_element(By.XPATH, '//*[@id="login_button"]').click()
        time.sleep(5)
        # 等待事件
        wait = WebDriverWait(self.browser, 280)
        wait.until(EC.presence_of_element_located((By.ID, 'key')))

        text_input=self.browser.find_element(By.ID,'key')
        text_input.clear()
        text_input.send_keys('美食')
        text_input.send_keys(Keys.ENTER)
        time.sleep(1.5)

    def get_data(self):
        page_idex = 1
        while True:
            self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(1.5)
            print("当前下载第{}页".format(page_idex))
            print(self.browser.current_url)  # 链接
            data = self.browser.page_source  # 获取源码
            # print(data)
            self.parse_data(data)

            # 等待翻页按钮
            wait = WebDriverWait(self.browser, 280)
            wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="pn-next"]/em')))

            try:
                # 开始翻页
                self.browser.find_element(By.XPATH, '//a[@class="pn-next"]/em').click()  # 点击
            except NoSuchElementException as e:
                print(e)
                print('爬取完毕~')
                sys.exit(0)  # 正常退出
            page_idex += 1

            # page_index+=1


    def parse_data(self,data):
        soup=BeautifulSoup(data,'lxml')
        name=soup.select('.gl-i-wrap a em')
        price=soup.select('.gl-i-wrap .p-price strong i')
        shop_name=soup.select('.gl-i-wrap .J_im_icon a')
        for names,prices,shop_names in zip(name,price,shop_name):
            name=names.get_text()
            price=prices.get_text()
            shop_name=shop_names['title']
            df=pd.DataFrame({
                'name':[name],'price':[price],'shop_name':[shop_name]
            })
            df.to_csv('data.csv',mode='a',header=False,index=False)
if __name__ == '__main__':
    spider = Spider()
    spider.get_jd()
    spider.get_data()


