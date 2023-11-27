import subprocess
from bs4 import BeautifulSoup
from openpyxl import Workbook

url = "https://www.peeringdb.com/ix/ID"

curl_command = f'curl -s "{url}"'
html_content = subprocess.check_output(curl_command, shell=True, encoding='utf-8')  # Spécifier l'encodage

soup = BeautifulSoup(html_content, "html.parser")

members = []

for item in soup.find_all("div", class_="row item operational"):
    member_info = {
        "name": item.find("div", class_="peer").get_text(strip=True),
        "asn": item.find("div", class_="asn").get_text(strip=True),
        "speed": item.find("div", class_="speed").get_text(strip=True),
        "policy": item.find("div", class_="policy").get_text(strip=True),
        "ip4": item.find("div", class_="ip4").get_text(strip=True),
        "ip6": item.find("div", class_="ip6").get_text(strip=True),
    }
    members.append(member_info)

wb = Workbook()
ws = wb.active

headers = ["Name", "ASN", "Speed", "Policy", "IPv4", "IPv6"]
ws.append(headers)

for member in members:
    ws.append([member["name"], member["asn"], member["speed"], member["policy"], member["ip4"], member["ip6"]])

wb.save("membres_ixp.xlsx")
