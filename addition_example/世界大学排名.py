#文章链接:https://mp.weixin.qq.com/s/V_fpPN62Kdf0bz6zgFpVCg

import requests
from lxml import etree
from collections import defaultdict
import pandas as pd

def get_university_rank():

    url = "https://www.compassedu.hk/qs_2021"
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }

    response = requests.get(url=url,headers=headers)
    response.encoding = response.apparent_encoding

    html = etree.HTML(response.text)

    table_heads = html.xpath("//tr[@class='header']/th/text()")[:10]
    print(table_heads)

    print(len(table_heads))
    university_msgs = html.xpath("//table[@id='rk']/tbody/tr[@class='odd']")
    msg_rows = []

    items = "./td/text()"

    for uu in university_msgs:
        # print(len(uu.xpath(items)))
        # print(uu.xpath(items))
        # break
        if len(uu.xpath(items)) == 9:
            msg_row = {table_heads[0]: uu.xpath(items)[0],
                       table_heads[1]: "".join(uu.xpath('./td/a/text()')[0]),
                       table_heads[2]: uu.xpath(items)[1],
                       table_heads[3]: uu.xpath(items)[2],
                       table_heads[4]: uu.xpath(items)[3],
                       table_heads[5]: uu.xpath(items)[4],
                       table_heads[6]: uu.xpath(items)[5],
                       table_heads[7]: uu.xpath(items)[6],
                       table_heads[8]: uu.xpath(items)[7],
                       table_heads[9]: uu.xpath(items)[8]
                       }
        else:
            msg_row = {table_heads[0]: uu.xpath(items)[0],
                       table_heads[1]: uu.xpath(items)[1],
                       table_heads[2]: uu.xpath(items)[3],
                       table_heads[3]: uu.xpath(items)[4],
                       table_heads[4]: uu.xpath(items)[5],
                       table_heads[5]: uu.xpath(items)[6],
                       table_heads[6]: uu.xpath(items)[7],
                       table_heads[7]: uu.xpath(items)[8],
                       table_heads[8]: uu.xpath(items)[9],
                       table_heads[9]: uu.xpath(items)[10]}
        msg_rows.append(msg_row)
    print(msg_rows[0])
    msgs = defaultdict(list)
    for msg in msg_rows:
        for k,v in msg.items():
            msgs[k].append(v)

    rank = pd.DataFrame(msgs)
    rank.to_excel("university_rank.xlsx",index=False)

if __name__ == '__main__':
    get_university_rank()
    



