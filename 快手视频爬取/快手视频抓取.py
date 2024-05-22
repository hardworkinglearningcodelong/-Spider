import requests
import os
class Ksspider (object):
    os_path=os.getcwd()+'/快手视频/'
    if not os.path.exists(os_path):
        os.mkdir(os_path)
    #准备数据
    def __init__(self):
        self.start_url='https://www.kuaishou.com/graphql'
        self.headers={'content-type':'application/json',
                      'Cookie':'kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did=web_9c7c33965e67ef58b49aa6b9d2b4acdf',
                      'Host':'www.kuaishou.com',
                      'Origin':'https://www.kuaishou.com',
                      'Referer':'https://www.kuaishou.com/brilliant',
                      'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

        self.data={"operationName":"brilliantTypeDataQuery","variables":{"hotChannelId":"00","page":"brilliant"},"query":"fragment photoContent on PhotoEntity {\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  __typename\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nfragment photoResult on PhotoResult {\n  result\n  llsid\n  expTag\n  serverExpTag\n  pcursor\n  feeds {\n    ...feedContent\n    __typename\n  }\n  webPageArea\n  __typename\n}\n\nquery brilliantTypeDataQuery($pcursor: String, $hotChannelId: String, $page: String, $webPageArea: String) {\n  brilliantTypeData(pcursor: $pcursor, hotChannelId: $hotChannelId, page: $page, webPageArea: $webPageArea) {\n    ...photoResult\n    __typename\n  }\n}\n"}

    def parse_start_url(self):
    #发送请求，获得响应
        for page in range(5):
            response=requests.post(self.start_url,headers=self.headers,json=self.data)
            """在类中，调用其他函数方法，需要加上self"""
            self.parse_response_data(response)

    def parse_response_data(self,response):
    #解析响应，数据提取
        json_data=response.json()
        data_list=json_data['data']['brilliantTypeData']['feeds']
        for data_dict in data_list:
            count_like= int(data_dict['photo']['realLikeCount'])
            if count_like>20000:
                title=data_dict['photo']['caption']
                mp4_url=data_dict['photo']['coverUrl']
                data=requests.get(mp4_url).content
                """调用保存函数方法"""
                self.parse_save_data(title,data )

    def parse_save_data(self,title,data):
    #保存数据
        with open ('os_path'+'title'+'.mp4','wb')as f:
            f.write(data)
        print(f"{title}================采集ok")

if __name__=='__main__':
    K=Ksspider()
    K.parse_start_url()



























