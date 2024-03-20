# Created by ZDB in 2024/03/18
# Practice project to get myself familiar with basic functions of web scraping

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


# from the main page of students, get the student page,
# as well as the audio file page of each student
def get_student_page_urls():
    url = "https://bluearchive.wiki/wiki/Characters"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("div", class_="mw-parser-output")
    tbody = table.find("tbody")
    student_page_urls = []
    student_audio_list_page_urls = []
    if tbody:
        rows = tbody.find_all("tr")
        for row in rows:
            a_tag = row.find("a")
            if a_tag:
                student_page_url = "https://bluearchive.wiki" + a_tag["href"]
                student_page_urls.append(student_page_url)
                student_audio_list_page_url = student_page_url + "/audio"
                student_audio_list_page_urls.append(student_audio_list_page_url)

    return student_page_urls, student_audio_list_page_urls


# get student_audio_list_page_url like https://bluearchive.wiki/wiki/Akari_(New_Year)/audio
# and then return the list of all the audio file page for a student
def get_audio_download_page_url(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    audio_tags = soup.find_all('audio')
    audio_urls = []
    names = []
    for audio in audio_tags:
        sources = audio.find_all('source')
        for source in sources:
            if source.get('src') and source['src'].endswith('.mp3'):
                complete_link = "https:" + source['src']
                audio_urls.append(complete_link)
                name = complete_link.split('/')[-1]
                name = name.replace("%28", "(").replace("%29", ")")
                names.append(name)

    return audio_urls, names


# get an audio url such as https://static.miraheze.org/bluearchivewiki/c/cc/Miyu_Title.ogg,
# the destination folder name, and the filename of the voice file,
# then download file with the assigned filename to the specific folder
def download_and_save_audio(audio_url, foldername, filename):
    # Ensure the base audios directory and the specific foldername exist
    base_path = "audios"
    target_folder = os.path.join(base_path, foldername)
    os.makedirs(target_folder, exist_ok=True)

    # Define the full path for the file to save
    file_path = os.path.join(target_folder, filename)

    # Download the audio file
    response = requests.get(audio_url, headers=headers)

    # Save the audio file to the specified path
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"File saved to {file_path}")


def main():
    print(headers)
    input_url = input("------Please Paste the URL------\n"
                      "URL should be from bluearchive.wiki, in format of\n"
                      "https://bluearchive.wiki/wiki/student_name/audio\n"
                      "Example: https://bluearchive.wiki/wiki/Minori/audio\n"
                      "Paste the URL Here:\n")
    folder_name = input_url.split('/')[-2]
    print("Downloading voice cover for: " + folder_name)
    audio_download_page_urls, file_names = get_audio_download_page_url(input_url)
    for url, name in zip(audio_download_page_urls, file_names):
        download_and_save_audio(url, folder_name, name)
        print(name + "------downloaded")


if __name__ == '__main__':
    main()
