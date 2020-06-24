import time
import csv
import requests
from bs4 import BeautifulSoup

def export_csv(idlist,idlist_new):

    # ファイルオープン
    f = open('output.csv', 'w')

    # header を設定
    fieldnames = ['URL','案件名','単価','契約形態','最寄り駅','業界','職種・ポジション','職務内容','求めるスキル','扱う技術','精算','現場の環境','担当者コメント']
    writer_h = csv.DictWriter(f, fieldnames=fieldnames)
    writer_h.writeheader()

    writer = csv.writer(f, lineterminator='\n')

    # 新着の出力/detailid内へ移動して
    for detail in idlist_new:
        export=list()
        project_page = "https://freelance.levtech.jp" + detail
        r = requests.get(project_page)
        soup = BeautifulSoup(r.content, "html.parser")

        if project_page:
            export.append(project_page)
        else:
            export.append('URLを取得できませんでした')

        # 案件概要の取得
        projectname = soup.find("h2",class_="pjt__ttl")
        if projectname:
            export.append(' '.join(projectname.text.strip().splitlines()))
        else:
            export.append('案件名取得できませんでした')

        # 詳細全体の取得
        pjtSummary = soup.find("div",class_="pjtSummary")
        # 詳細項目の取得
        price = pjtSummary.find("em",class_ = "js-yen")
        type_c = pjtSummary.find("a",class_ = "pjtTag")
        rows = pjtSummary.find_all("div",class_="pjtSummary__row")

        if price:
            export.append("〜"+price.text.strip())
        if type_c is not None:
            export.append(type_c.text.strip())

        # 最寄り

        # 欲しい情報を文字列検索しながら変数に代入
        for item in rows:
            if "最寄り駅" in item.text:
                station = item.find_all("p",class_="pjtSummary__row__desc")
                if station[1] is not None:
                    export.append(station[1].text.strip())
                else:
                    export.append('取得できませんでした')
                continue
            
            if "職種・ポジション" in item.text or "業界" in item.text:
                positions = item.find_all("a",class_="pjtTag")
                position_list = list()
                for position in positions:
                    position_list.append(position.text.strip())
                    position_export = '・'.join(position_list)

                if position_export is not None:
                    export.append(position_export)
                else:
                    export.append('取得できませんでした')
                continue
            else:
                export.append('この項目は存在しません/最寄り・職種、業界')

        # 案件詳細の取得
        detail_table = soup.find_all("div",class_="pjtDetail__row")
        for detail in detail_table:
            if "職務内容" in detail.text:
                job_content = detail.text.strip()
                if job_content is not None:
                    export.append(job_content)
                else:
                    export.append('取得できませんでした')
                continue
            
            if "求めるスキル" in detail.text:
                job_skill = detail.find("p",class_="descDetail__txt").text.strip()
                if job_skill is not None:
                    export.append(job_skill)
                else:
                    export.append('取得できませんでした')
                continue

            if "この会社が扱う技術" in detail.text:
                job_tech = detail.find("p",class_="descDetail__txt").text.strip()
                if job_tech is not None:
                    export.append(job_tech)
                else:
                    export.append('取得できませんでした')
                continue

            if "精算・お支払い" in detail.text:
                job_pays = detail.find_all("p",class_="descDetail__txt")
                pay_list = list()
                for job_pay in job_pays:
                    pay_list.append(job_pay.text.strip())
                    pay_export = '・'.join(pay_list)

                if pay_export is not None:
                    export.append(pay_export)
                else:
                    export.append('取得できませんでした')
                continue

            if "おすすめポイント" in detail.text:
                job_point = detail.find("a",class_="pjtTag").text.strip()
                if job_point is not None:
                    export.append(job_point)
                else:
                    export.append('取得できませんでした')
            else:
                export.append('この項目は存在しません/detail部')    
                continue    
    
        job_comment = soup.find("p",class_="pjtComment__detail__txt").text.strip()
        if job_comment is not None:
            export.append(job_comment)
        else:
            export.append('取得できませんでした')
            
        #書き込み
        writer.writerow(export)
        time.sleep(0.5)

    # ファイルクローズ
    f.close()