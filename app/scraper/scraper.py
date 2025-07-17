# 注意
# - スクリプトの実行は自己責任
# - スクリプトを実行する際は、time.sleep(t)のtを長めに設定しサーバーへの負担を最小限に抑えること

import os
import time
import zipfile
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# 保存ディレクトリの指定
download_dir_path = Path("../data/zip_data").resolve()
download_dir_path.mkdir(exist_ok=True)
download_dir = str(download_dir_path.resolve())

# オプション
options = webdriver.ChromeOptions()
options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": download_dir,
        "plugins.always_open_pdf_externally": True,
    },
)

chuo_shijou_url = "https://www.seisen.maff.go.jp/seisen/bs04b040md001/BS04B040UC020SC001-Evt007.do"

# Chrome Webドライバー の インスタンスを生成
driver = webdriver.Chrome(options=options)

# Webドライバーで中央卸売市場ページを起動
driver.get(chuo_shijou_url)

years = [str(y) for y in range(2015, 2025)]
months = [str(m).zfill(2) for m in range(1, 13)]
tendays = ["1", "2", "3"]  # 1:上旬, 2:中旬, 3:下旬

def download_zip(year: str, month: str, tenday: str) -> None:
    """Download CSV for the specified period."""
    # 年を指定
    year_element = driver.find_element(By.NAME, "s027.year")
    select = Select(year_element)
    select.select_by_value(year)

    # 月を指定
    month_element = driver.find_element(By.NAME, "s027.month")
    select = Select(month_element)
    select.select_by_value(month)

    # 期間を指定
    tendays_element = driver.find_element(By.NAME, "s027.tendays")
    select = Select(tendays_element)
    select.select_by_value(tenday)

    # ダウンロード (CSVボタンを押す)
    csv_button = driver.find_element(By.NAME, "CSV")
    csv_button.click()

t = 10
# Iterate over all year/month/ten-day combinations and download each CSV
for y in years:
    for m in months:
        for t in tendays:
            download_zip(y, m, t)
            time.sleep(t)

# 終了処理
driver.quit()

# zipファイルを解凍して移動
for file_name in os.listdir("../data/zip_data"):
    if file_name.endswith(".zip"):
        zip_path = os.path.join("../data/zip_data", file_name)
        mv_path = os.path.join("../data/csv_data", os.path.splitext(file_name)[0])

        # zipファイルの解凍
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(mv_path)

        print(f"解凍完了: {file_name} -> {mv_path}")
