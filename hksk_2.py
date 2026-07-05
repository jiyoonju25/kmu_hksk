from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
import json
import os

url = "https://kookmin.ac.kr/user/unLvlh/lvlhSpor/todayMenu/index.do"

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")


day_map = {
    "일":1,
    "월":2,
    "화":3,
    "수":4,
    "목":5,
    "금":6,
    "토":7
}

def is_price(text):
    return re.match(r".*￦\s?\d+",text)

def parse_menu (menu_list):
    sets=[]
    current_items = []
    current_name = None


    for item in menu_list:
        if item.startswith("[") and item.endswith("]"):
            continue
        if "￦" in item:
            match = re.search(r"￦\s?(\d+)",item)
            
            if not match : continue

            price = int(match.group(1))
            
            clean_item = re.sub(r"￦\s?\d+","",item).strip()
            if clean_item:
                current_items.append(clean_item)
            
            sets.append({
                "name":current_name or (current_items[0] if current_items else "메뉴"),
                "price":price,
                "items":current_items.copy()
            })
            

            current_items=[]
            current_name = None
            continue
        
        current_items.append(item)
    return sets


result = {}

for day,column in day_map.items():

    result[day]=[]

    for section in soup.select("div.cont_section"):

        title = section.select_one("p.cont_subtit")
        table = section.find("table")

        if not table:
            continue

        for tr in table.find_all("tr"):
            tds = tr.find_all("td")

            if len(tds)<= column:
                continue

            restaurant = tds[0].get_text(" ", strip=True)
            menu_text = tds[column].get_text("\n", strip=True)

            if not menu_text:
                continue

            if "￦" not in menu_text:
                continue

            menu_lines = [
                m.strip()
                for m in menu_text.split("\n")
                if m.strip()
            ]        

            parsed = parse_menu(menu_lines)

            menu_lines = [m for m in menu_lines if m is not None]
            result[day].append({
                "category" : title.get_text(strip=True).split("(")[0],
                "restaurant" : restaurant,
                "sets" : parsed
            })

base = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base, "menu.json")

with open(path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(os.getcwd())

