import argparse
import time
from spider_logic import fetch_page_content


def main():
    parser = argparse.ArgumentParser(description="使用代理发送HTTP请求")

    #代理服务器 为 vpn设置的port
    parser.add_argument('--proxy', type=str, required=False, default='',
                        help="代理服务器地址，例如：http://user:pass@proxyserver:port")
    args = parser.parse_args()

    url = "https://saishi.zgzcw.com/summary/liansaiAjax.action"

    season_list = [i for i in range(2004,2025)]
    round_list = [i for i in range(1,36)]
    # test case
    season_list = [2024]
    round_list = [1]
    #
    # 遍历参数组合
    for season in season_list:
        for round in round_list:
            payload = {
                "source_league_id": 60,
                "currentRound": round,
                "season": season,
                "seasonType": ""
            }
            fetch_page_content(url, args.proxy, payload)
            time.sleep(2)  # 延迟2秒


if __name__ == "__main__":
    main()
