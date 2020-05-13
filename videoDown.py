#!/usr/bin/env python3
import requests,urllib
from bs4 import BeautifulSoup
import os
import subprocess

pwd = os.path.split(os.path.realpath(__file__))[0]

headers = {
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
    'cookie': "has_js=1; minVersion={\"experiment\":1570672462,\"minFlavor\":\"new_vermi-1.13.7.11.js100\"}; minUniq=%7B%22minUID%22%3A%22bb80328a30-e8cdeb4d55-9a314411d2-aff4bb11a6-4aa23e3779%22%7D; minDaily=%7B%22testMode%22%3Atrue%2C%22dailyUser%22%3Atrue%7D; __gads=ID=b6eee23a8df86f72:T=1588041695:S=ALNI_MYCQR1Bf2fq53bqISIZBy8kIgI9oA; minBuffer=%7B%22minAnalytics%22%3A%22%7B%5C%22clicks%5C%22%3A%5B%5D%2C%5C%22clicksDelay%5C%22%3A%5B%5D%7D%22%2C%22_minEE1%22%3A%22%5B%5D%22%7D; minSession=%7B%22minSID%22%3A%227f32fd50ab-88cc4cf6f3-68d284cdee-1faeb65c08-c5966d76ac%22%2C%22minSessionSent%22%3Atrue%2C%22hadImp%22%3Atrue%2C%22sessionUniqs%22%3A%22%7Btime%3A1588053248571%2Clist%3A%5B11206251nt0%5D%7D%22%7D; OptanonConsent=landingPath=NotLandingPage&datestamp=Tue+Apr+28+2020+13%3A55%3A33+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=3.6.24&AwaitingReconsent=false&groups=1%3A1%2C101%3A0%2C2%3A0%2C0_132429%3A0%2C3%3A0%2C4%3A0%2C0_132431%3A0%2C104%3A0%2C106%3A0%2C111%3A0%2C114%3A0%2C120%3A0%2C124%3A0%2C126%3A0%2C130%3A0%2C133%3A0%2C134%3A0%2C144%3A0%2C145%3A0%2C146%3A0%2C147%3A0%2C150%3A0%2C151%3A0%2C157%3A0%2C162%3A0%2C173%3A0%2C0_126679%3A0%2C0_137695%3A0%2C0_132361%3A0%2C0_132391%3A0; GED_PLAYLIST_ACTIVITY=W3sidSI6Ijh5clQiLCJ0c2wiOjE1ODgwNTMzNDksIm52IjowLCJ1cHQiOjE1ODgwNTMzMzMsImx0IjoxNTg4MDUzMzM3fV0.",
    'cache-control': "no-cache"}

def read_file(filepath):
    listOfLines  =  list()
    with  open  (filepath,  "r")  as  myfile:
        for  line in  myfile:
            listOfLines.append(line.strip())
    return listOfLines

def write_txt(item,file_name):
    with open(file_name, 'a+') as f:
        f.write('\t'.join([str(r) for r in item])+'\n')

def get_video_id(url,videoNameToUrlMap,videoNameToIdMap):
    response = requests.request("GET", url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    videoId = soup.find_all('video', class_="video-js")[0]['data-video-id']
    title = soup.find_all('h1', class_="video-player__title")[0].contents[0]
    videoNameToIdMap[title] = videoId
    exists(videoId,videoNameToUrlMap[url])
    videoList = soup.find_all('li', class_="video-playlist__item")
    print(videoId,title)
    print(len(videoList))
    # for video in videoList:
    #     videoNameToIdMap[video.find_all('a')[0].contents[0]] = video['data-video-id']
    #     print(video['data-video-id'])
    #     print(video.find_all('a')[0].contents[0])
    #     exists(video['data-video-id'])
    return videoNameToIdMap

def get_m3u8_url(id):
    url = "https://secure.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId={}&secure=true".format(id)
    response = requests.request("GET", url, headers=headers)
    return response.text.split("\n")[-2]

def exists(id,name):
    name = name.replace("/","_")
    filename = '{}.mp4'.format(name)
    filePath = pwd + "/downLownVideo2/" +filename
    if os.path.exists(filePath):
        print("exists",id)
        return
    else:
        m3u8_url = get_m3u8_url(id)
        download(m3u8_url,filePath)

def download(m3u8_url,filePath):
    # here \" and \" is important！
    cmd_str = 'ffmpeg -i \"' + m3u8_url + '\" ' + '-acodec copy -vcodec copy -absf aac_adtstoasc "' + filePath+'"'
    print(cmd_str)
    subprocess.call(cmd_str,shell=True)

if __name__ == '__main__':
    httpFileName = pwd + "/TGUK官网视频下载清单.csv"
    # outFileName = pwd + "/TGUK官网视频下载清单out.csv"
    idFileName = pwd + "/TGUK官网视频下载清单id.csv"
    listOfLines = read_file(httpFileName)
    videoNameToUrlMap = dict()
    videoNameToIdMap = dict()
    for line in listOfLines:
        strs = line.split('\t')
        # print(strs)
        if len(strs) > 1:
            videoNameToUrlMap[strs[1]] = strs[0]
        else:
            print(line)
    for url in set(videoNameToUrlMap.keys()):
        print(url)
        if len(url) > 0:
            videoNameToIdMap = get_video_id(url,videoNameToUrlMap,videoNameToIdMap)
    for name in videoNameToIdMap.keys():
        try:
            id = videoNameToIdMap[name]
            m3u8_url = get_m3u8_url(id)
            params = (name,id,m3u8_url)
            write_txt(params,idFileName)
        except Exception as e:
            print(id)
            print(e)