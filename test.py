import re
import requests
import time
import csv
from bs4 import BeautifulSoup

# ファイルオープン
f = open('output.csv', 'w')
writer = csv.writer(f, lineterminator='\n')

project_page = "https://freelance.levtech.jp/project/detail/44838/"
r = requests.get(project_page)
soup = BeautifulSoup(r.content, "html.parser")

# 案件概要の取得
proposition = soup.find("h2",class_="pjt__ttl")
# pjtSummary = soup.find("div",class_="pjtSummary")
# price = pjtSummary.find("em",class_ = "js-yen").text.strip()
# type_c = pjtSummary.find("a",class_ = "pjtTag").text.strip()
#     # 最寄り
# rows = pjtSummary.find_all("div",class_="pjtSummary__row")
#     # 欲しい情報を文字列検索しながら変数に代入
# for item in rows:
#     if "最寄り駅" in item.text:
#         station = item.find_all("p",class_="pjtSummary__row__desc")
#     if "職種・ポジション" in item.text:
#         positions = item.find_all("a",class_="pjtTag")
#         position_list = list()
#         for position in positions:
#             position_list.append(position.text.strip())
#             position_export = '・'.join(position_list)

# # 案件詳細の取得
# detail_table = soup.find_all("div",class_="pjtDetail__row")
# for detail in detail_table:
#     if "職務内容" in detail.text:
#         job_content = detail.text.strip()
#     if "求めるスキル" in detail.text:
#         job_skill = detail.find("p",class_="descDetail__txt").text.strip()
#     if "この会社が扱う技術" in detail.text:
#         job_tech = detail.find("p",class_="descDetail__txt").text.strip()
#     if "精算・お支払い" in detail.text:
#         job_pays = detail.find_all("p",class_="descDetail__txt")
#         pay_list = list()
#         for job_pay in job_pays:
#             pay_list.append(job_pay.text.strip())
#             pay_export = '・'.join(pay_list)            
#     if "おすすめポイント" in detail.text:
#         job_point = detail.find("a",class_="pjtTag").text.strip()

# job_comment = soup.find("p",class_="pjtComment__detail__txt").text.strip()

# listの作成
export=list()
export.append(' '.join(proposition.text.strip().splitlines()))
# export.append("〜"+price)
# export.append(type_c)
# export.append(station[1].text.strip())
# export.append(position_export)
# export.append(job_content)
# export.append(job_skill)
# export.append(job_tech)
# export.append(pay_export)
# export.append(job_point)
# export.append(job_comment)

#書き込み
writer.writerow(export)

# ファイルクローズ
f.close()