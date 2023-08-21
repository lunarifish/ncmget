
import re
import requests
import wget
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions




def handle_302(src: str) -> str:
    resp = requests.get(src, timeout=(3, 7))
    if len(resp.history) > 0:
        location_url = resp.history[len(resp.history) - 1].headers.get('Location')
    return location_url



# 构建外链/歌曲链接 outer=True则构建外链 outer=False则构建歌曲链接
def build_url(arg: str, outer: bool) -> str:
    # arg是歌曲链接
    if "music.163.com/song?id=" in arg:
        song_id_start = arg.find("song?id=") + 8    # song id开始的位置

        # 遍历字符串寻找song id结束的位置
        for i in range(song_id_start, len(arg)):
            if not arg[i].isdigit():
                song_id = arg[song_id_start:i]
                break
        else:
            song_id = arg[song_id_start]
        
        return handle_302(f"http://music.163.com/song/media/outer/url?id={song_id}.mp3") if outer else f"https://music.163.com/song?id={song_id}"

    # arg是song id
    elif arg.isnumeric():
        return handle_302(f"http://music.163.com/song/media/outer/url?id={arg}.mp3") if outer else f"https://music.163.com/song?id={arg}"

    else:
        print("E: Illegal argument")
        return None


def get_song_information(src: str, webdriver_engine: str) -> str:
    if webdriver_engine == "Chrome":
        print("webdriver=chrome")
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=chrome_options)
    elif webdriver_engine == "Firefox":
        print("webdriver=firefox")
        firefox_options = FirefoxOptions()
        firefox_options.add_argument('--headless')
        driver = webdriver.Firefox(options=firefox_options)

    driver.get(src)

    time.sleep(2)
    html = driver.page_source
    driver.close()

    pattern = r'<title>(.*?)</title>'
    title_html = re.findall(pattern,html,re.S|re.M)[0][:-13]
    return title_html



def download(src: str, filename: str):
    wget.download(src, filename)

