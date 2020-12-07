import requests
from lxml import etree
import re
import random
import subprocess as sp


def parser_ip(url):

    resp = requests.get(url = url,headers=headers)
    resp.encoding = resp.apparent_encoding
    html = etree.HTML(resp.text)
    #ip内容
    br_tags = html.xpath("//div[@class='cont']/text()")
    #print(br_tags)
    #按照字符串方式提取ip
    ips = [tag.split("@")[0].replace("\n","").replace("\t","") for tag in br_tags][:-1]
    #pattern = re.compile(r"(\d+\.\d+\.\d+\.d+:\d{4})@")
    #对每个br标签的内容提取ip,一个br标签只有一个ip,所以取下标0
    #ips = [pattern.findall(tag)[0] for tag in br_tags]

    return ips


def get_proxy():

    url = "http://www.xsdaili.cn"

    UserAgent_List = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
    global headers
    headers = {'User-Agent': random.choice(UserAgent_List)}

    response = requests.get(url=url,headers=headers)
    response.encoding = response.apparent_encoding
    html = etree.HTML(response.text)

    #获取代理所在链接
    a_tags = html.xpath("//div[@class='title']/a")
    #print(a_tags)

    #当天的国内最新ip代理和国外ip代理所在的url和最新日期
    newest_proxy_urls = [url+tag.get("href") for tag in a_tags][0:2]
    #print(newest_proxy_urls)
    recent_dates = html.xpath("//div[@class='title']/a/text()")[0:2]
    #print(recent_dates)
    #print(recent_date)

    #国内外最新ip分别爬取
    inner_ip = parser_ip(newest_proxy_urls[0])
    external_ip = parser_ip(newest_proxy_urls[1])

    return inner_ip,external_ip,recent_dates

def check_ip(ip,lose,time):

    """

    :param ip: 代理的ip地址
    :param lose: 丢包数
    :param time: 连接时间
    :return: 代理ip平均耗时
    """
    cmd = "ping -n 3 -w 3 %s"
    p = sp.Popen(cmd % ip,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
    out = p.stdout.read().decode("gbk")
    #丢包数
    lose = lose.findall(out)

    if len(lose) == 0:
        lose = 3
    else:
        lose = int(lose[0])

    if lose > 2:
        return False
    else:
        avg_time = time.findall(out)
        if len(avg_time) == 0:
            return 1000
        else:
            avg = int(avg_time[0])

            return avg

def time_pattern():
    lose = re.compile(u"丢失 = (\d+)",re.I)
    time = re.compile(u"平均 = (\d+)",re.I)
    return lose,time



if __name__ == "__main__":

    lose,time = time_pattern()
    inner_ip,external_ip ,recent_dates = get_proxy()

    while True:
        proxy = random.choice(inner_ip)
        avg_time = check_ip(proxy,lose,time)

        if avg_time > 200:
            #去掉不能使用的ip
            inner_ip.remove(proxy)
            print("连接超时，重新选择ing...")
        if avg_time < 200:
            break

    inner_ip.remove(proxy)
    print("可用ip:",inner_ip)

    with open(recent_dates[0]+".txt","a") as f:
        inner_ip = "\n".join(inner_ip)
        for i in inner_ip:
            f.writelines(i)



            



    





        

    







