import time
import csv
import requests
from fake_useragent import UserAgent
from datetime import datetime, timedelta
import sys
import warnings
warnings.filterwarnings("ignore")


# 构建请求的URL和参数
url = "https://webapi.sporttery.cn/gateway/jc/football/getMatchResultV1.qry"
subUrl = "https://webapi.sporttery.cn/gateway/jc/football/getFixedBonusV1.qry"

params = {
    "matchPage": 1,
    "matchBeginDate": "2024-07-31",
    "matchEndDate": "2024-07-31",
    "leagueId": "",
    "pageSize": 30,
    "pageNo": 1,
    "isFix": 0,
    "pcOrWap": 1
}

proxies = {
    "http": "http://127.0.0.1:33210",  # 本地HTTP代理地址
    "https": "http://127.0.0.1:33210",  # 本地HTTPS代理地址
}
ua = UserAgent()
headers = {
    "User-Agent": ua.random,
    "Content-Type": "application/json"
}


def processOneLink(id):
    bounus_set = {}
    subParams = {
        "clientCode": 3001,
        "matchId": id
    }
    subResponse = requests.get(url = subUrl, params = subParams, verify= False, proxies= proxies, headers= headers)
    if subResponse.status_code == 200:
        tableData = subResponse.json()
        tableData = tableData["value"]["oddsHistory"]
        bounus_set["总进球赔率"] = tableData["ttgList"]
        bounus_set["半场赔率"] = tableData["hafuList"]
        bounus_set["全场赔率"] = tableData["hadList"]
        bounus_set["比分赔率"] = tableData["crsList"]
        bounus_set["让球赔率"] = tableData["hhadList"]
    else:
        print(f"请求失败，状态码: {subResponse.status_code}")
    return bounus_set
def processClues(data):
    fieldnames = ["比赛Id", "客队", "主队", "胜", "平", "负", "半场比分", "全场比分",
                  "总进球赔率", "半场赔率", "全场赔率", "比分赔率", "让球赔率"]
    with open('比赛数据.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            raw_data = {
                "比赛Id": item["matchId"],
                "客队": item["allAwayTeam"],
                "主队": item["allHomeTeam"],
                "胜": item['h'],
                "平": item['d'],
                "负": item['a'],
                "半场比分": item["sectionsNo1"],
                "全场比分": item["sectionsNo999"],
            }
            bounus_set = processOneLink(item["matchId"])
            raw_data.update(bounus_set)
            writer.writerow(raw_data)
            print("add 1 row")
            time.sleep(0.3)


# 爬虫开始日期
start_date = input("开始日期：")
end_date = input("结束日期：")
try:
    datetime.strptime(start_date, "%Y-%m-%d")
except ValueError:
    print(f"'{start_date}' 不符合 YYYY-MM-DD 格式，程序终止。")
    sys.exit(1)
try:
    datetime.strptime(end_date, "%Y-%m-%d")
except ValueError:
    print(f"'{end_date}' 不符合 YYYY-MM-DD 格式，程序终止。")
    sys.exit(1)
start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

# 循环遍历日期范围
current_date = start_date_obj
while current_date <= end_date_obj:
    date_str = current_date.strftime("%Y-%m-%d")
    params["matchBeginDate"] = date_str
    params["matchEndDate"] = date_str
    response = requests.get(url, params=params, verify=False, proxies=proxies, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # data['value']['matchResult']
        processClues(data['value']['matchResult'])
    else:
        print(f"请求失败，状态码: {response.status_code}")
    current_date += timedelta(days=1)



