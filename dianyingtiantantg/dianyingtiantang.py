import requests
from bs4 import BeautifulSoup
import re
import csv
import _thread
import time

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
#url格式：https://www.ygdy8.com/html/gndy/dyzz/list_23_(页码).html

def get_movie(page):
    response = requests.get(url =  "https://www.ygdy8.com/html/gndy/dyzz/list_23_{}.html".format(page),headers = headers)
    #查看网页的head标签中,找到网页的charset=gb2312,即为网站编码
    response.encoding = "gb2312"
    
    html = response.text

    movie_names = []
    movie_urls = []
    
    bs = BeautifulSoup(html,"html.parser")
    #找到电影名称的位置在class=co_content8的div标签内,如果有多个co_content标签时将返回列表
    bc = bs.findAll(class_="co_content8")
    #进一步观察，名称位置在class为ulink的a标签内,获得一页全部电影的列表
    #浏览html页面发现一页中只有一个class = "co_content8"的div标签，故直接取index为0
    bc = bc[0].findAll(class_ = "ulink")
    
    #开始对电影列表循环，获取电影名称等信息
    for i in range(len(bc)):
        #获取电影名称，get_text获取的a标签的文本
        name = bc[i].get_text()
        #获取每个电影跳转的详情页面链接，在class为ulink的href中,
        # 因此接上前半段构成完整的详情页面的url
        msg_href = "https://www.ygdy8.com/"+bc[i].get("href")
        #打印电影名称
        print(bc[i].get_text())

        time.sleep(1)
        msg_resp = requests.get(url = msg_href,headers = headers)
        
        msg_resp.encoding = "gb2312"
        #获取html代码
        msg_html = msg_resp.text
        
        msg_bs = BeautifulSoup(msg_html,"html.parser")
        #找到下载链接位置
        msg_bc = msg_bs.find("tbody").find_next("td").find_next("a")
        #获取下载链接
        download_url = msg_bc.get("href")
        
        #print(download_url)
        
        movie_names.append(name)
        movie_urls.append(download_url)
    
    return movie_names,movie_urls


def get_whole_pages(url):
    resp = requests.get(url = url,headers = headers)
    resp.encoding = "gb2312"
    
    pattern = re.compile(r'(\d{3})页')#直接获取总页数
    #获取匹配页数，total类型为列表，total中的元素是页数的str类型
    total = pattern.findall(resp.text)
    
    return int(total[0])

def write_into_csv(movie_name,download_url):
    
    with open("最新电影.csv","a+",encoding = "utf-8") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([movie_name,download_url])
    
def run(start_page,end_page):    
    for page in range(start_page,end_page):
        movie_list,download_list = get_movie(page)
        for i in range(0,len(movie_list)):
            write_into_csv(movie_list[i],download_list[i])
        time.sleep(3) #避免频繁请求

if __name__ == "__main__":
    # all_pages=get_whole_pages("https://www.ygdy8.com/html/gndy/dyzz/list_23_1.html")
    # end = all_pages//8

    #print(end)
    run(1,2)
    # try:
    #     _thread.start_new_thread(run,(1,end))
    #     _thread.start_new_thread(run,(end+1,end*2))
    #     _thread.start_new_thread(run,(end*2+1,end*3))
    #     _thread.start_new_thread(run,(end*3+1,end*4))
    #     _thread.start_new_thread(run,(end*4+1,end*5))
    #     _thread.start_new_thread(run,(end*5+1,end*6))
    #     _thread.start_new_thread(run,(end*6+1,end*7))
    #     _thread.start_new_thread(run,(end*7+1,end*8))
    # except:
    #     print("Error:启动线程失败")


        
    
    
            
                 
    
        
    
    