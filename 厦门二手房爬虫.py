import random
import time
from datetime import date
from bs4 import BeautifulSoup
import requests
import pandas as pd
pd.set_option('display.max_columns', None)


# 定义函数，生成网址
def make_urls(location, n):
    '''
    location：区域
    n：页面数量
    '''
    urls = []
    for i in range(1, n+1):
        url = 'https://xm.lianjia.com/ershoufang/{}/pg{}/'.format(location, i)
        urls.append(url)
    return urls

siming = make_urls('siming', 100)  # 思明有100个页面
huli = make_urls('huli', 100)  # 湖里有100个页面
jimei = make_urls('jimei', 100)  # 集美有100个页面
haicang = make_urls('haicang', 100)  # 海沧有100个页面
xiangan = make_urls('xiangan', 95)  # 翔安有95个页面
tongan = make_urls('tongan', 46)  # 同安有46个页面

# 所有网址汇总起来
xm_urls_list = siming + huli + jimei + haicang + xiangan + tongan


# 定义函数，用来处理User-Agent和Cookie
def ua_ck():
    '''
    网站需要登录才能采集，需要从Network--Doc里复制User-Agent和Cookie，Cookie要转化为字典
    '''

    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}

    cookies = 'select_city=350200; lianjia_uuid=c6bb527e-c73e-4c18-80a2-0e6c701d4f40; _smt_uid=5f649daa.382e09bd; UM_distinctid=174a107e3f6810-0ca2d4a8dbcaa8-333769-125f51-174a107e3f7c3e; _ga=GA1.2.1661642603.1600429486; _gid=GA1.2.527914271.1600429486; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1600429483,1600476524; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22174a107e556cb9-037ed71a329a2c-333769-1204049-174a107e557d11%22%2C%22%24device_id%22%3A%22174a107e556cb9-037ed71a329a2c-333769-1204049-174a107e557d11%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; lianjia_ssid=0857e41c-7ca8-24c2-7d18-e2b4b02e4d13; User-Realip=140.243.198.151; CNZZDATA1254525948=1557469094-1600424880-%7C1600525641; CNZZDATA1255847100=75444696-1600427554-%7C1600525837; CNZZDATA1255633284=1437618958-1600429218-%7C1600526300; CNZZDATA1255604082=1475741897-1600429003-%7C1600526307; _gat=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1600527516; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYTE5NzE1ZDYzZjIzMDQ0NTQ5NWUzYmFlOTQxYTI1Nzg0YWZlZjk5MDI4NDJjYjU5YWE1YjEyYTg5YzYzODM5ODU3YmJlNTc1NGU3OTlkODU3NzA1NGM2ZGRkY2YxNWYxMjdiMGYyNGQ3ZjEzNTdmOWM1NDRmMjgxYjRhM2NlYjU2MDBlZGUxZDA0YjgxMWFmZTRhODk2ZGM3YjRlMmEwMWVjNDQ4YjQ1NjJmODQ2MWM2MDRiM2Q1N2NlMjk1YmZkYzk0YTFjMjUzYzkyYTM2NDBjOWUzNzg3ZjkyOWI2MmE2MTRlMzVhNmU4NDJmMDlkNWNhNGM4MDM0Y2ZhNzMzYjBlZTViYzg4OTA2YWNmNWNjM2Y3YmQ1MjQwMTA4MDVmMGY4ZTE0OTAzNjNjMjVmZDcwN2RhNWU3YjIzMTE2ZTliM2QyYjM5ZTJmYjQ3NmJkMWQ5MTA0NDA4ZTMzMzJmZVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJkZmYxZTM4NVwifSIsInIiOiJodHRwczovL3htLmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0='

    # Cookie转化为字典
    cookies = cookies.split('; ')
    cookies_dict = {}
    for i in cookies:
        cookies_dict[i.split('=')[0]] = i.split('=')[1]

    return user_agent, cookies_dict


# 定义函数，获取房源链接
def get_urls(url, u_a, c_d):
    '''
    url：每一个页面的链接
    u_a：User-Agent
    c_d：cookies
    '''
    
    html = requests.get(url, headers=u_a, cookies=c_d)
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find('ul', class_='sellListContent').find_all(
        'div', class_='info clear')
    hrefs = []
    for item in items:
        href = item.find('div', class_='title').find('a')['href']
        hrefs.append(href)
    return hrefs

def get_info(url, u_a, c_d):
    '''
    url：每一个页面的链接
    u_a：User-Agent
    c_d：cookies
    '''
    
    html = requests.get(url, headers=u_a, cookies=c_d)
    html.encoding = html.apparent_encoding  # 解决乱码的万金油方法
    soup = BeautifulSoup(html.text, 'html.parser')

    results = []
    info = {}

    a = soup.find('div', class_='overview').find('div', class_='content')
    info['房源链接'] = url
    info['总价'] = a.find('div', class_='price').find(
        'span', class_='total').text
    info['总价单位'] = a.find('div', class_='price').find(
        'span', class_='unit').text
    info['单价'] = a.find('div', class_='price').find('div', class_='text').find(
        'div', class_='unitPrice').find('span', class_='unitPriceValue').text
    info['小区名称'] = a.find('div', class_='aroundInfo').find(
        'div', class_='communityName').find('a').text
    info['所在大区'] = a.find('div', class_='aroundInfo').find(
        'div', class_='areaName').find('span', class_='info').find_all('a')[0].text
    info['所在详细区域'] = a.find('div', class_='aroundInfo').find(
        'div', class_='areaName').find('span', class_='info').find_all('a')[1].text

    b = soup.find('div', class_='m-content').find('div', class_='introContent')

    # 基本属性
    items1 = b.find('div', class_='base').find_all('li')
    for item in items1:
        info[item.text[:4]] = item.text[4:]

    # 交易属性
    items2 = b.find('div', class_='transaction').find_all('li')
    for item in items2:
        info[item.find_all('span')[0].text] = item.find_all('span')[1].text

    results.append(info)
    return results


# 开始采集数据
login = ua_ck()
u_a = login[0]
c_d = login[1]

house_urls = []  # 保存房源链接
error_url = []  # 保存采集失败的页面链接
for url in xm_urls_list:
    try:
        href = get_urls(url, u_a, c_d)
        house_urls.extend(href)
    except:
        error_data.append(url)
    time.sleep(random.random()*4)  # 设置时间间隔
    
    print('已采集{}条数据'.format(len(house_urls)))  # 监控采集进度

print('房源链接采集完成！！！总共采集了{}条链接'.format(len(house_urls)))

# 把链接先保存起来
save_list = pd.DataFrame({'url': house_urls})
save_list.to_excel(r'厦门二手房源链接_{}.xlsx'.format(date.today()))

data = []  # 保存房源详细信息
error_data = []  # 保存采集失败的链接

# 采集前3000条
for house_url in house_urls[:3000]:
    try:
        info = get_info(house_url, u_a, c_d)
        data.extend(info)
    except:
        error_data.append(house_url)
        print('采集失败{}条'.format(len(error_data)))
    time.sleep(random.random()*3)  # 设置时间间隔
    
    print('已采集{}条数据'.format(len(data)))  # 监控采集进度

print('房源信息采集完成！！！总共采集了{}条数据'.format(len(data)))

time.sleep(200)  # 间隔200秒

# 采集剩下的信息
for house_url in house_urls[3000:]:
    try:
        info = get_info(house_url, u_a, c_d)
        data.extend(info)
    except:
        error_data.append(house_url)
        print('采集失败{}条'.format(len(error_data)))
    time.sleep(random.random()*3)
    
    print('已采集{}条数据'.format(len(data)))

print('房源信息采集完成！！！总共采集了{}条数据'.format(len(data)))


# 保存为本地Excel文件，文件名包含采集时间
df = pd.DataFrame(data)
df.to_excel(r"厦门链家网二手房爬虫数据_{}.xlsx".format(date.today()))