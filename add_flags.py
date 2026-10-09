import requests
import time
import re
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

def get_country(ip):
    try:
        # 清理 IPv6 方括号和端口
        clean_ip = re.sub(r'[\[\]]', '', ip.split(':')[0] if not ip.startswith('[') else ip.split(']:')[0].strip('[]'))
        if ip.startswith('['):
            clean_ip = ip.split(']:')[0].strip('[]')
        else:
            clean_ip = ip.split(':')[0]
            
        resp = requests.get(f"http://ip-api.com/json/{clean_ip}?fields=countryCode", timeout=8)
        data = resp.json()
        return data.get("countryCode", "XX")
    except Exception as e:
        print(f"查询失败 {ip}: {e}")
        return "XX"

def process_file(input_file="ipv6.txt"):
    results = []
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            results.append(line)
            continue

        # 已经有 # 备注的跳过
        if "#" in line:
            results.append(line)
            continue

        ip_part = line.strip()
        country = get_country(ip_part)
        flag = FLAG_MAP.get(country, "🏳️")
        
        new_line = f"{ip_part}#{country} {flag}"
        results.append(new_line)
        print(f"✓ {new_line}")
        
        time.sleep(1.3)  # 免费接口限速

    # 加上更新时间
    header = f"# Updated at {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC\n"
    with open(input_file, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(results) + "\n")
    
    print(f"\n完成！已更新 {input_file}")

if __name__ == "__main__":
    process_file("ipv6.txt")
