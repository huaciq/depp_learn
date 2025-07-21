import os
import re
import json
import urllib.parse
import requests
from time import sleep
from random import uniform

# 配置参数
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36'
}

# 搜索关键词
keyword = '电瓶车载人'
# 编码关键词以拼接 URL
encoded_keyword = urllib.parse.quote(keyword)

# 保存路径
save_dir = './baidu_images'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 爬取数量
num_images = 50  # 总共爬取多少张图片
per_page = 30    # 每次请求返回多少张图片（一般最大为30）

# 遍历分页
image_count = 0
for page in range(0, num_images, per_page):
    print(f'正在爬取第 {page // per_page + 1} 页...')

    # 百度图片搜索的 API 请求 URL（不是正式 API，是网页异步加载数据的接口）
    url = f'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=undefined&ipn=rj&ct=201326592&is=&fp=result&queryWord={encoded_keyword}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={encoded_keyword}&pn={page}&rn={per_page}&gsm=1e'

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        data = json.loads(response.text)
        if 'data' not in data:
            print("返回数据格式异常")
            break

        for item in data['data']:
            if 'thumbURL' in item:
                image_url = item['thumbURL']
                try:
                    img_data = requests.get(image_url, headers=headers, timeout=10).content
                    file_name = os.path.join(save_dir, f'{image_count + 1}.jpg')
                    with open(file_name, 'wb') as f:
                        f.write(img_data)
                    print(f'成功保存：{file_name}')
                    image_count += 1
                    if image_count >= num_images:
                        break
                    sleep(uniform(0.5, 1.2))  # 防止过快被封IP
                except Exception as e:
                    print(f'图片下载失败：{e}')
        sleep(uniform(1, 2))  # 分页间也加延时
    except Exception as e:
        print(f'请求失败：{e}')

print(f'共下载 {image_count} 张图片。')
