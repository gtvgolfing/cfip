import requests
import time
from datetime import datetime

FLAG_MAP = {
    "US": "🇺🇸", "HK": "🇭🇰", "SG": "🇸🇬", "JP": "🇯🇵", "KR": "🇰🇷",
    "TW": "🇹🇼", "DE": "🇩🇪", "NL": "🇳🇱", "GB": "🇬🇧", "CA": "🇨🇦",
    "AU": "🇦🇺", "MO": "🇲🇴", "FR": "🇫🇷", "IT": "🇮🇹", "ES": "🇪🇸",
    "SE": "🇸🇪", "FI": "🇫🇮", "NO": "🇳🇴", "DK": "🇩🇰", "CH": "🇨🇭",
    "AT": "🇦🇹", "BE": "🇧🇪", "IE": "🇮🇪", "PT": "🇵🇹", "PL": "🇵🇱",
    "CZ": "🇨🇿", "HU": "🇭🇺", "RO": "🇷🇴", "BG": "🇧🇬", "GR": "🇬🇷",
    "TR": "🇹🇷", "RU": "🇷🇺", "UA": "🇺🇦", "IN": "🇮🇳", "BR": "🇧🇷",
    "MX": "🇲🇽", "AR": "🇦🇷", "CL": "🇨🇱", "ZA": "🇿🇦", "EG": "🇪🇬",
    "AE": "🇦🇪", "SA": "🇸🇦", "IL": "🇮🇱", "TH": "🇹🇭", "VN": "🇻🇳",
    "MY": "🇲🇾", "ID": "🇮🇩", "PH": "🇵🇭", "NZ": "🇳🇿", "CN": "🇨🇳",
}


def get_country(ip, session):
    try:
        # 同时兼容 IPv4、IPv6 和带端口的地址
        if ip.startswith("["):
            clean_ip = ip.split("]")[0].strip("[]")
        elif ip.count(":") > 1:
            # 不带方括号的 IPv6 地址
            clean_ip = ip
        else:
            # IPv4 或 IPv4:端口
            clean_ip = ip.split(":")[0]

        resp = session.get(
            f"http://ip-api.com/json/{clean_ip}?fields=countryCode",
            timeout=8
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("countryCode", "XX")
    except Exception as e:
        print(f"查询失败 {ip}: {e}")
        return "XX"


def process_file(input_file, session):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"跳过：文件不存在 {input_file}")
        return
    except OSError as e:
        print(f"读取失败 {input_file}: {e}")
        return

    results = []

    for line in lines:
        line = line.strip()

        if not line or line.startswith("#"):
            results.append(line)
            continue

        # 去掉已有备注，重新查询国家
        ip_part = line.split("#", 1)[0].strip()

        if not ip_part:
            results.append(line)
            continue

        country = get_country(ip_part, session)
        flag = FLAG_MAP.get(country, "🏳️")

        new_line = f"{ip_part}#{country} {flag}"
        results.append(new_line)
        print(f"✓ [{input_file}] {new_line}")

        time.sleep(1.3)

    header = (
        f"# Updated at "
        f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC"
    )

    try:
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(header + "\n" + "\n".join(results) + "\n")

        print(f"\n完成！已更新 {input_file}\n")
    except OSError as e:
        print(f"写入失败 {input_file}: {e}")


def main():
    with requests.Session() as session:
        for filename in ("ipv6.txt", "ip.txt"):
            process_file(filename, session)

    print("全部处理完毕！")


if __name__ == "__main__":
    main()
