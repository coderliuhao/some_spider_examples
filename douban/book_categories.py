import requests
from lxml import etree
import re
import random
from openpyxl import Workbook
import urllib.parse
import time


def bookkinds_transfer(name):
    """[转化汉字为url编码]

    Args:
        name ([str]): [书籍类型(中文)]

    Returns:
        [str]: [转码后的书籍类型]
    """
    #name = name.encode("gb2312")
    name = urllib.parse.quote(name)
    return name

def pages_num(url):

    """[获取某类型书籍的总页数]

    Returns:
        [int]: [总页数值]
    """
    resp = requests.get(url = url,headers=headers)
    resp.encoding = resp.apparent_encoding
    html = etree.HTML(resp.text)
    page = html.xpath("//div[@class='paginator']/a/text()")[-1]
    page_num = int(page)

    return page_num

def url_process(url,page=1):
    
    """[根据参数逻辑生成url]

    url来自get_all_categories()函数返回值
    url=https://book.douban.com/tag/%E6%BC%AB%E7%94%BB?start=20&type=T
    分析参数:每页是20本书，第二页的start参数是20,且第一页的start=0
    因此认为start参数= (当前页数-1)*20
    type参数不用变

    Returns:
        [str]: [起始页的url]
    """
    processed_url = url + "?start={}&type=T".format(str(20*(page-1)))
    return processed_url

def get_all_categories():
    
    url = "https://book.douban.com/tag/"
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
    #获取所有的类型
    all_kinds = html.xpath("//table[@class='tagCol']/tbody/tr/td/a/text()")
    #转码后的url
    url_list = [url+bookkinds_transfer(kind) for kind in all_kinds]
    #创建书籍类型与url的映射关系，注意这里的url需要作为返回值传递给process_url函数
    kind_url_dict = {k:v for k,v in zip(all_kinds,url_list)}
    print(all_kinds)
    print("==============================="*4)
    interest_kind = input("请从上面类别中选择感兴趣的书籍类型:")
    interest_url = kind_url_dict[interest_kind]

    return interest_kind,interest_url

def get_book_msg(kind,kind_url):

    """
    kind参数来自get_all_categories()的返回值 interest_kind
    kind_url:来自get_all_categories的返回值 interest_url
    
    """
    wb = Workbook()
    sheet = wb.active
    sheet.title = f"{kind}全部图书信息"
    sheet["A1"] = "书名"
    sheet["B1"] = "作者"
    sheet["C1"] = "出版日期"
    sheet["D1"] = "书籍链接"
    sheet["E1"] = "评论数"
    sheet["F1"] = "豆瓣评分"

    #处理url
    processed_url = url_process(kind_url)
    #获取总页数
    pages = pages_num(processed_url)

    for i in range(1,pages):

        page_url = url_process(kind_url,page = i)
        time.sleep(1)
        resp = requests.get(url=page_url,headers=headers)
        time.sleep(5)
        resp.encoding = resp.apparent_encoding


        html = etree.HTML(resp.text)
        print(f"正在获取第{i}页书籍信息....")
        #获取书名
        a_tags0 = html.xpath("//div[@class='info']/h2/a")
        book_names = [tag.get("title") for tag in a_tags0]
        #获取作者,出版年月
        others = html.xpath("//div[@class='pub']/text()")
        authors = [au.split("/")[0].strip() for au in others]
        dates = [dt.split("/")[-2].strip() for dt in others]
        #获取书籍链接
        a_tags = html.xpath("//div[@class='info']/h2/a")
        book_urls = [href.get("href") for href in a_tags]
        #获取评论数，score
        book_comms = html.xpath("//span[@class='pl']/text()")
        comm_nums = [int(re.findall(r"(\d+)",comm)[0]) for comm in book_comms]

        book_scores = html.xpath("//span[@class='rating_nums']/text()")
        print(f"第{i}页信息抓取完成")

        for book_name,author,date,book_url,comm_num,book_score in zip(book_names,authors,dates,book_urls,comm_nums,book_scores):
            sheet.append([book_name,author,date,book_url,comm_num,book_score])

        print(f"第{i}页书籍信息保存成功")
        
    filename = kind+"类书籍信息"+".xlsx"
    wb.save(filename)


if __name__ == "__main__":

    kind,kind_url = get_all_categories()
    get_book_msg(kind,kind_url)




















    


    




