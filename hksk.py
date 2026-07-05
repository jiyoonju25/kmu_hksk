from bs4 import BeautifulSoup
import requests
from datetime import datetime

url = "https://kookmin.ac.kr/user/unLvlh/lvlhSpor/todayMenu/index.do"

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

weekday_names = ["월", "화", "수", "목", "금", "토", "일"]

weekday = datetime.today().weekday()

print(f" ## {weekday_names[weekday]}요일 학식 ##")


column_map=[2,3,4,5,6,7,1]
column = column_map[weekday]

print("=" * 50)

# 식당별 섹션 순회
for section in soup.select("div.cont_section"):

    title = section.select_one("p.cont_subtit")

    if title:
        print(f"{title.get_text(strip=True)}")
        print("=" * 50)

    table = section.find("table")

    if not table:
        continue

    for tr in table.find_all("tr"):

        tds = tr.find_all("td")

        # 식당명 + 일~토
        if len(tds) != 8:
            continue

        restaurant = tds[0].get_text(" ", strip=True)
        menu = tds[column].get_text("\n", strip=True)

        if not menu:
            continue

        
        if "￦" not in menu:
            continue

        print(f"[{restaurant}]")
        print(menu)
        print("-" * 50)