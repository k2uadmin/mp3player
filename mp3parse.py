from fileinput import filename

import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import subprocess

# Fetch and parse content page
foler_path = r'L:\vsCode\webpageMP3'
file = 'mp3_urls.csv'
file_path = os.path.join(foler_path, file)
save_folder = r'L:\budda_mp3'
#mp3download = 'mp3_download.csv'
mp3_filesource = 'L:/vsCode/webpageMP3/mp3_download.csv'
content_url = "http://www.namoamitabha.net/namo_mp3/yuan_series/content.htm"
prefix_url = "http://www.namoamitabha.net/namo_mp3/yuan_series/"
#response = requests.get(content_url)
#response.encoding = 'big5'  # Ensure correct encoding
#soup = BeautifulSoup(response.text, "html.parser")
mp3_data = []
mp3_download = []
def get_url(prefix_url=prefix_url, mp3_data=mp3_data):
    for link in soup.find_all("a", href=True):
        if '第' in link.get_text():
            urls = prefix_url + link['href']
            text = link.get_text()
            page = requests.get(urls) 
            page.encoding = 'big5'
            page_soup = BeautifulSoup(page.text, "html.parser")
            for mp3_link in page_soup.find_all("a", href=True):
                if mp3_link['href'].endswith('.mp3'):
                    mp3_url = prefix_url + mp3_link['href']
                    mp3_title = mp3_link.get_text()
                    mp3_data.append({'Collection': text, 'Title': mp3_title, 'MP3_URL': mp3_url})
                
def download_mp3(mp3_url, mp3_titil, save_folder=save_folder):
    try:
        response = requests.get(mp3_url, stream=True)
        response.raise_for_status()
        save_file = mp3_url.split('/')[-1]
        save_path = os.path.join(save_folder, save_file)
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {save_path}")
        mp3_download.append({'Title': mp3_titil, 'Save_Path': save_path})
    except Exception as e:
        print(f"Failed to download {mp3_url}: {e}")

def play_mp3(save_folder=save_folder):
    
    try:
        subprocess.run(['ffplay', '-nodisp', '-autoexit', save_folder], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to play {file_path}: {e}")


if __name__ == "__main__":
    # get_url(prefix_url=prefix_url)
    # df_main = pd.DataFrame(mp3_data, columns=['Collection', 'Title', 'MP3_URL'])
    # df_main.to_csv(file_path, encoding='utf-8-sig')
    # df = pd.read_csv(file_path)
    # for index, row in df.iterrows():
    #     mp3_url = row['MP3_URL']
    #     mp3_title = row['Title']
    #     download_mp3(mp3_url, mp3_title, save_folder=save_folder)
    # df_download = pd.DataFrame(mp3_download, columns=['Title', 'Save_Path'])
    # download_file = 'mp3_download.csv'  
    # df_download.to_csv(os.path.join(foler_path, download_file), encoding='utf-8-sig', index=False)
   
    df = pd.read_csv(mp3_filesource)
    #file_path = df['Save_Path'].tolist()
    # for index, row in df.iterrows():
    #     print(index, row['Title'], row['Save_Path'])
    #     save_folder = row['Save_Path']

    #     play_mp3(save_folder=save_folder)

    file_mp3 = df['Save_Path'][300]
    print(file_mp3)
    subprocess.run(['ffplay', '-nodisp', '-autoexit', file_mp3], check=True)
