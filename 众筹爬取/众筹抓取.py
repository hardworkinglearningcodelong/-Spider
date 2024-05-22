# 导入相关模块
import pandas as pd
# 因为是异步加载因此导入json模块
# 导入相关模块
import time
import requests
from datetime import datetime
import os
# 因为是异步加载因此导入json模块
df=pd.DataFrame()
page_num=1
while True:
    print(f'爬取的参数为{page_num}页')
    url = 'https://www.indiegogo.com/private_api/graph/query?operation_id=discoverables_query'
    params = {"variables": {"category_main": None, "category_top_level": None, "feature_variant": "none", "page_num": page_num,
                            "per_page": 12, "project_timing": "all", "project_type": "campaign", "q": None,
                            "sort": "trending", "tags": []}}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/118.0.0.0 Safari/537.36'
    }
    try:
        response = requests.post(url, json=params, headers=headers)
        json_data = response.json()['data']['discoverables']
    except:
        print('No Element')
        print('爬取完毕~')
        break
    # if not json_data:
    #     # 如果返回的数据为空，表示没有更多的页可用，循环结束
    #     break
    for json_datum in json_data:
        titles = json_datum['title']
        prices = json_datum['funds_raised_amount']
        project_ids = json_datum['project_id']
        image_urls = json_datum['image_url']
        open_dates = json_datum['open_date']
        close_dates = json_datum['close_date']
        funds_raised_percents = json_datum['funds_raised_percent']
        funds_raised_amounts = json_datum['funds_raised_amount']
        print(titles)
        print(prices)
        temp_df = pd.DataFrame(
            {'title': [titles], 'prices': [prices], 'project_ids': [project_ids], 'open_dates': [open_dates],
             'image_urls': [image_urls]})

        # 将临时DataFrame与主DataFrame连接起来
        df = pd.concat([df, temp_df], ignore_index=True)
    page_num += 1
    time.sleep(1)

current_date = datetime.now().strftime('%Y-%m-%d')

# 将 DataFrame 写入 csv 文件，文件名为当前日期
filename = f'{current_date}.csv'
df.to_csv(filename, index=False)
folder_path = 'data/'

# 如果文件夹不存在，则创建它
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
# 将CSV文件移动到指定的文件夹中
os.replace(filename, os.path.join(folder_path, os.path.basename(filename)))
