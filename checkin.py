import requests
import os
import json
from datetime import datetime

# ============================================================
# 配置区域
# 方式一：直接在此处填写 Cookie（本地运行时使用）
# 方式二：设置环境变量 GLADOS_COOKIE（GitHub Actions 时使用）
# ============================================================
COOKIE = os.environ.get("GLADOS_COOKIE")

CHECKIN_URL = "https://glados.cloud/api/user/checkin"
STATUS_URL  = "https://glados.cloud/api/user/status"

HEADERS = {
    "cookie": COOKIE,
    "content-type": "application/json;charset=UTF-8",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "referer": "https://glados.cloud/console/checkin",
    "origin": "https://glados.cloud",
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "accept-encoding": "gzip, deflate",
    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
}


def checkin():
    """执行 Check-In"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始 Check-In...")

    if COOKIE == "your_cookie_here":
        print("错误：请先填写你的 Cookie！")
        return

    try:
        resp = requests.post(
            CHECKIN_URL,
            headers=HEADERS,
            json={"token": "glados.cloud"},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()

        message = data.get("message", "无返回信息")
        points  = data.get("list", [{}])[0].get("change", "?") if data.get("list") else "?"
        print(f"Check-In 结果：{message}（获得 {points} 积分）")

    except requests.exceptions.RequestException as e:
        print(f"请求失败：{e}")
        return

    # 查询账号状态（剩余天数）
    try:
        resp2 = requests.get(STATUS_URL, headers=HEADERS, timeout=15)
        resp2.raise_for_status()
        status = resp2.json()

        data2    = status.get("data", status)  # 兼容嵌套和非嵌套两种结构
        email    = data2.get("email", "未知")
        days     = data2.get("leftDays", "未知")
        vip_level = data2.get("vip", "未知")
        print(f"账号：{email} | 剩余天数：{days} 天 | 等级：{vip_level}")

    except requests.exceptions.RequestException as e:
        print(f"查询状态失败：{e}")


if __name__ == "__main__":
    checkin()
