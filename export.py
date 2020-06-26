import time
import csv
import requests
from bs4 import BeautifulSoup

def export_csv(idlist,memo):
    # ファイルオープン
    f_name = "output_"+memo+".csv"
    f = open(f_name, 'w')

    # header を設定
    fieldnames = ['URL','案件名','単価','契約形態','最寄り駅','業界/職種・ポジション','職務内容','求めるスキル','扱う技術','精算','現場の環境','おすすめポイント','担当者コメント']
    writer_h = csv.DictWriter(f, fieldnames=fieldnames)
    writer_h.writeheader()

    writer = csv.writer(f, lineterminator='\n')

    # 新着の出力/detailid内へ移動して
    for detail in idlist:
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
        row2 = pjtSummary.find_all("p",class_="pjtSummary__row__desc")

        # 詳細項目の取得
        if "単価" in pjtSummary.text:
            price = pjtSummary.find("em",class_ = "js-yen")
            export.append("〜"+price.text.strip())
        else:
            export.append("単価は取得できませんでした")

        if "契約形態" in pjtSummary.text:
            export.append(row2[1].text.strip())
        else:
            export.append("契約形態は取得できませんでした")
        
        if "最寄り駅" in pjtSummary.text:
            export.append(row2[2].text)
        else:
            export.append("最寄り駅は取得できませんでした")

        if "職種・ポジション" in pjtSummary.text or "業界" in pjtSummary.text :
            rows = pjtSummary.find_all("div",class_="pjtSummary__row")
            for item in rows:
                if "職種・ポジション" in item.text or "業界" in item.text:
                    positions = item.find_all("a",class_="pjtTag")
                    position_list = list()
                    for position in positions:
                        position_list.append(position.text.strip())
                        position_export = '・'.join(position_list)        
                    export.append(position_export)
        else:
            export.append("業界/職種は取得できませんでした")

        # 案件詳細の取得
        detail_table = soup.find("div",class_="pjtDetail")
        detail_row = detail_table.find_all("div",class_="pjtDetail__row")

        if "職務内容" in detail_table.text:
            for detail in detail_row:
                if "職務内容" in detail.text:
                    export.append(detail.text)
        else:
            export.append("職務内容は取得できませんでした")

        if "求めるスキル" in detail_table.text:
            for detail in detail_row:
                if "求めるスキル" in detail.text:
                    export.append(detail.text)
        else:
            export.append("求めるスキルは取得できませんでした")    
        
        if "この会社が扱う技術" in detail_table.text:
            for detail in detail_row:
                if "この会社が扱う技術" in detail.text:
                    export.append(detail.text)
        else:
            export.append("この会社が扱う技術は取得できませんでした")
        
        if "精算・お支払い" in detail_table.text:
            for detail in detail_row:
                if "精算・お支払い" in detail.text:
                    export.append(detail.text)
        else:
            export.append("精算・お支払いは取得できませんでした")

        if "現場の環境" in detail_table.text:
            for detail in detail_row:
                if "現場の環境" in detail.text:
                    export.append(detail.text)
        else:
            export.append("現場の環境は取得できませんでした")

        if "おすすめポイント" in detail_table.text:
            for detail in detail_row:
                if "おすすめポイント" in detail.text:
                    export.append(detail.text)
        else:
            export.append("おすすめポイントは取得できませんでした")
        
        job_comment = soup.find("p",class_="pjtComment__detail__txt")
        if job_comment:
            export.append(job_comment.text.strip())
        else:
            export.append('担当者コメントは取得できませんでした')
            
        #書き込み
        writer.writerow(export)
        time.sleep(0.5)

    # ファイルクローズ
    f.close()