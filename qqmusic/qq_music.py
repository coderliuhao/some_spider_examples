import requests
import json
import openpyxl
import re
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
#url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=58570138342066459&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&w=%E5%91%A8%E6%9D%B0%E4%BC%A6&g_tk_new_20200303=5381&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0"
# response = requests.get(url = url,headers = headers)
# resp_json = response.json()

#通过逐层解读Previews中的json结构，获取到歌曲信息的上一层
# msgs= resp_json["data"]["song"]["list"]
# print(msgs)
#遍历打印歌曲信息
# for msg in msgs:
#     print("歌名: ",msg["name"])
#     print("所在专辑: ",msg["album"]["name"])
#     #点击歌曲观察歌曲播放的url构成
#     #https://y.qq.com/n/yqq/song/0039MnYb0qxYhV.html，包含了msgs中mid的信息
#     print("播放链接: https://y.qq.com/n/yqq/song/"+msg["mid"]+".html\n\n")
    

#根据需求选择歌手爬取歌曲链接
#找到不带参数的url
#get_music获取指定歌手部分歌曲的全部信息



def get_music_rank():
    url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
    singer = input("输入需要查询的歌手姓名:")
    pages = int(input("输入需要查询的歌曲页数:"))

    num_songs = 987
    per_page = 20

    if pages==0 or pages > num_songs//per_page + 1:
        print('超出最大页数范围,请输入页数在1~46之间')

    #把歌曲信息写入excel
    wb = openpyxl.Workbook()
    sheet =wb.active
    sheet.title = "歌曲详情"

    sheet["A1"] = "歌曲名"
    sheet["B1"] = "所属专辑"
    sheet["C1"] = "播放链接"

    name_ls = []
    urls_ls = []
    id_ls=[]
    for i in range(pages):
        params = {
        'ct': '24',
        'qqmusic_ver': '1298',
        'new_json': '1',
        'remoteplace': 'txt.yqq.song',
        'searchid': '63312576811446985',
        't': '0',
        'aggr': '1',
        'cr': '1',
        'catZhida': '1',
        'lossless': '0',
        'flag_qc': '0',
        'p': str(i+1),
        'n': str(per_page),
        'w': singer,
        'g_tk_new_20200303': '5381',
        'g_tk': '5381',
        'loginUin': '0',
        'hostUin': '0',
        'format': 'json',
        'inCharset': 'utf8',
        'outCharset': 'utf-8',
        'notice': '0',
        'platform': 'yqq.json',
        'needNewCode': '0'
        }
        time.sleep(1)
        response = requests.get(url=url,params = params,headers = headers)
        resp_json = response.json()
        msgs = resp_json["data"]["song"]["list"]

        for msg in msgs:
            names = msg["name"]
            name_ls.append(names)
            print(names)
            id = msg["id"]
            id_ls.append(id)
            albums = msg["album"]["name"]
            play_urls = "https://y.qq.com/n/yqq/song/" + str(msg["mid"]) + ".html\n\n"
            urls_ls.append("https://y.qq.com/n/yqq/song/" + str(msg["mid"]) + ".html")
            sheet.append([names, albums, play_urls])

    # 20是参数param["n"]中传入的一页显示的歌曲数
    wb.save(singer + "歌曲top" + str(pages * per_page) + ".xlsx")
    print()
    print("爬取完成")

    return name_ls,urls_ls,id_ls


#TODO:找到lasthotcommentid与歌名的联系
#TODO: 找到comments = response_json["comment"]["commentlist"]为空的原因
def get_hot_comments(songs,urls,ids):
    #songs,urls = get_music_rank()
    pages = 20
    perpage = 25
    song = input("请输入歌名以查询评论: ")
    #name_url_dict = {k : v for k in songs for v in urls}
    name_id_dict = {k : v for k in songs for v in ids}
    url= "https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg"

    for i in range(pages):
        params = {
            'g_tk_new_20200303': '5381',
            'g_tk': '5381',
            'loginUin': '0',
            'hostUin': '0',
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'GB2312',
            'notice': '0',
            'platform': 'yqq.json',
            'needNewCode':'0',
            'cid': '205360772',
            'reqtype': '2',
            'biztype': '1',
            'topid': name_id_dict[song],
            'cmd': '8',
            'needmusiccrit': '0',
            'pagenum': str(i+1),
            'pagesize':str(perpage),
            'lasthotcommentid':"song_97773_1207094353_1489594872",
            'domain': 'qq.com',
            'ct':'24',
            'cv':"10101010"
        }

        response = requests.get(url= url,headers = headers,params = params)
        #response.encoding = "gb2312"
        response_json = response.json()
        print(type(response_json))
        #print(response_json)
        comments = response_json["comment"]["commentlist"]
        print(comments)
        #print(comments)
        filename = song + "_top{perpage*pages}热评"+".txt"
        with open(filename,"a",encoding="utf-8") as f:
            for d in comments:
                comment = d["rootcommentcontent"]+"\n-----------------------\n"
                f.writelines(comment)
    print("评论爬取完成")

if __name__ == '__main__':
    #get_music_rank()
    songs,urls,ids = get_music_rank()
    #print(ids)
    get_hot_comments(songs,urls,ids)
























