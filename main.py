# coding: utf-8

#--------------------------------------------------------------
#
#   Python3系で作成
#   idとclass名の取得・csvへの書き込み、該当idとclassの座標取得
#
#--------------------------------------------------------------

#use csv
import csv
import pandas as pd
#get screenshot
import os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary #firefox使用のため
#read html
from bs4 import BeautifulSoup
import re
#OpenCV
import cv2

### 定数
CSV_INPUT_PATH = './input/web-list.csv'
SCREEN_W = 1280
SCREEN_H = 900
SCREEN_H_REAL = 900
THRESHOLD_PICTORIAL = 0.7
THRESHOLD_TEXT = 0.3

# CSVの行数をカウントする関数
def count_row_csv(file_path):
    # return sum(1 for line in open(file_path)) - 1
    return 100



# 画像サイズを縮小して返す関数
def resize_image(screenshot):
    height_resize = screenshot.shape[0] / (screenshot.shape[1] / SCREEN_W)
    SCREEN_H_REAL = height_resize
    size = (int(SCREEN_W), int(height_resize))
    return cv2.resize(screenshot, size)

# 分析全体をする関数
def analyze_page(driver, originalId, category, title, url):
    driver.get(url) # 検証ページをオープン

    # ページ読み込み完了まで待機
    input("アニメーション等の読み込みが完了したらEnterを押してください\n")

    driver.save_screenshot('./output/screenshot/' + str(originalId) + '-' + title +'.png') # スクショ取得

    screenshot = cv2.imread('./output/screenshot/' + str(originalId) + '-' + title +'.png', 1)
    screenshot = resize_image(screenshot)

    cv2.imwrite('./output/resize/' + str(originalId) + '-' + title +'.png', screenshot ) #Save


# main
if __name__ == '__main__':
    # csvの読み込み
    tag_list_num = count_row_csv(CSV_INPUT_PATH)
    csv_web_list = pd.read_csv(CSV_INPUT_PATH)

    print('行数: ' + str(tag_list_num))

    binary = FirefoxBinary('/Applications/Firefox.app/Contents/MacOS/firefox')
    binary.add_command_line_options('-headless')
    driver = webdriver.Firefox(firefox_binary=binary)
    driver.set_window_size(SCREEN_W, SCREEN_H)


    for i in range(tag_list_num):
        print('解析対象' + str(csv_web_list.iat[i, 0]) + ': ' + str(csv_web_list.iat[i, 2]))
        analyze_page(driver ,csv_web_list.iat[i, 0] , csv_web_list.iat[i, 1] , csv_web_list.iat[i, 2], csv_web_list.iat[i, 3])

    # Close Web Browser
    driver.quit()
