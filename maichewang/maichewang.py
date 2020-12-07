import re
import requests
import urllib.parse
from lxml import etree
import openpyxl



"""
    url = "http://www.buycar.cn/search.php?chid=2&ccid1=&searchword=%B1%F0%BF%CB&page=1"
    
    params:
    searchword：搜索的车名，需要把车名转为gb2312编码
    page:资讯的页码
    
"""

#main url
main_url = "http://www.buycar.cn/search.php?chid=2&ccid1=&"


#车名编码
def carname_transfer(name):

    """

    :param name: 车品牌名(中文)
    :return: 中文经过转码后的字符串
    """
    name = name.encode("gb2312")
    name = urllib.parse.quote(name)
    return name
#获取将车名转码后的新闻链接
def get_news_url(name,url=main_url,page=1):

    """

    :param name: 车品牌名
    :param url:  不带参数的url
    :param page: 起始页码，新闻首页
    :return: 将车品牌名转码后作为url中的searchword参数，添加page参数
    """
    t_name = carname_transfer(name)
    news_url = main_url + "searchword={0}&page={1}".format(t_name,page)
    return news_url
#获得该车新闻总页数
def get_pagesNum(url):

    """

    :param url: 新闻页面完整的url,带参数
    :return: 获取当前车品牌下的新闻页数，每页条新闻
    """

    response = requests.get(url=url,headers = headers).text
    html = etree.HTML(response)
    redirect = html.xpath("//a[@class='p_redirect']")
    page_num = [red.get("href") for red in redirect][-1]
    pages = page_num[-2:]
    pages = int(pages)
    return pages
# 处理编码
def process_ec_dc(text):
    try:
        newtext = text.encode("ISO-8859-1").decode("utf-8")
    except:
        try:
            newtext = text.encode("ISO-8859-1").decode("gbk")
        except:
            newtext = text
    return newtext

def get_news(name,start,end):

    """

    :param name: 车品牌名
    :param start: 起始新闻页数
    :param end: 终止页数
    :return: None
    """

    global headers
    headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "汽车新闻"

    sheet["A1"] = "发布日期"
    sheet["B1"] = "新闻链接"
    sheet["C1"] = "新闻标题"

    # 获取指定车名的新闻url和新闻总页数
    
    url = get_news_url(name)
    #print(url)
    pages = get_pagesNum(url)
    #print(pages)
# 找到各个新闻的标题，链接和发布日期
# 遍历页数
    for i in range(start,end):
# 获取每页新闻的url
        newpage_url = get_news_url(name,page=i)
        #print(newpage_url)
# 解析每页新闻的url
        response = requests.get(url=newpage_url,headers = headers)
        response.encoding = "gbk"
        response = response.text
        html = etree.HTML(response)
# 获取当前页每条新闻的标题、链接和发布日期
        titles = html.xpath("//div[@class='sosoCon pL15']/ul/li/em/a/text()")
        new_as = html.xpath("//div[@class='sosoCon pL15']/ul/li/em/a")
        urls_list = [url.get("href") for url in new_as]
        news_dates = html.xpath("//div[@class='sosoCon pL15']/ul/li/p/span/text()")

        news_dates.sort(reverse = True)
# 10*(end-1)一页里包含10条新闻
    for date,url,title in zip(news_dates,urls_list,titles):
        sheet.append([date, url, title])
    filename = name+"recent"+str(10*(end-1))+"news"+".xlsx"
    wb.save(filename)
    # carnews = pd.DataFrame({"日期": news_dates,
    #                 "新闻链接": urls_list,
    #                 "新闻标题": titles
    #                 })
    print(filename+"保存成功")

    pattern_p = "<p>(.*?)</p>"
    content_list = []
    for url in urls_list:
        resp = requests.get(url=url,headers = headers)
        resp.encoding = 'gb2312'
        resp = resp.text
        #process_ec_dc(resp)
        content = re.findall(pattern_p,resp)
        for i in range(len(content)):
            content[i] = re.sub('<.*?>','',content[i])
        while '' in content:
            content.remove('')
        content = '\n'.join(content)  #变成字符串
        #content_list.append(content)

        txt_file = name + str(10*(end-1)) + "news_content"+".txt"
        with open(txt_file,"a",encoding="utf-8") as f:
            f.writelines(content)
    print(txt_file+"保存成功")


# # 遍历获取到的所有新闻链接，获取新闻正文
#     content_list = []
#     for newurl in urls_list:
#         time.sleep(1)
#         news_content = requests.get(url=newurl,headers = headers).text
#         news_content=process_ec_dc(news_content)
#         cont = etree.HTML(news_content)
#
#         texts = cont.xpath("//div[@class='con_c_content']/p/text()")
#         print(texts)
#         # content_list = []
#         # for text in texts:
#         #     content_list.append(text[:-1])

#    return content_list

if __name__ == '__main__':

    get_news("别克",1,2)







    



        
        












   
         



