import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import csv
import re


headers = None
proxies = None

def fetch_page_content(url, proxy, payload):
    #fake user agent信息
    ua = UserAgent()
    # 设置代理
    proxies = {
        "http": proxy,
        "https": proxy
    }
    if (len(proxy) == 0):
        proxies = None

    headers = {
        "User-Agent": ua.random,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # 创建会话对象
    session = requests.Session()

    # 发送POST请求
    try:
        response = session.post(url, data=payload, proxies=proxies, headers=headers,verify= False)

        # 检查请求是否成功
        if response.status_code == 200:
            print(f"请求成功！payload: {payload}")
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            # 提取 "亚" url
            extract_links(soup)
            text_content = soup.get_text(separator='\n', strip=True)
            process_text_content(text_content)
        else:
            print(f"请求失败，状态码: {response.status_code}, payload: {payload}")

    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}, payload: {payload}")

"""


"""

def extract_links(soup):
    # 查找所有<tr>标签
    rows = soup.find_all('tr')
    for row in rows:
        # 在每一行中查找包含 "亚" 文本的<a>标签
        asian_link = row.find('a', text='亚')
        if asian_link:
            href = asian_link.get('href')
            print(f"亚 链接: {href}")


def visit_link(href, session, proxies):
    try:

        response = session.get(href, proxies=proxies)
        if response.status_code == 200:
            print(f"访问 {href} 成功")
            # 这里你可以处理HTML内容，例如解析、保存等
            html_content = response.text
            # 例如，打印前500个字符
            print(html_content[:500])
        else:
            print(f"访问 {href} 失败，状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"访问 {href} 出错: {e}")

def process_text_content(text):
    lines = text.split('\n')
    records = []
    record = []

    # 时间格式正则表达式（根据实际格式调整）
    time_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}')

    for line in lines:
        if time_pattern.match(line):
            if record:
                records.append(record)
            record = [line]
        elif line.endswith("析"):
            record.append(line)
            records.append(record)
            record = []
        elif record:
            record.append(line)

    # 写入CSV文件
    with open('records.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['时间', '主队', '比分', '客队', '半场', '让球', '类型', '结尾'])
        for record in records:
            writer.writerow(record)

    print("数据已写入 records.csv")