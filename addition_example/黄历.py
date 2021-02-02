# -*- coding: utf-8 -*- 
# @Time : 2021/1/28 21:34
# @Version: 3.8.5
# @Author : liu hao 
# @File : 黄历.py

#文章链接:https://mp.weixin.qq.com/s/BJVophyTigIqPdJpnxEHlQ

import requests
import json
import datetime
from zhdate import ZhDate
import re


def get_json(year):

    url = 'https://staticwnl.tianqistatic.com/Public/Home/js/api/yjs/{}.js'.format(year)
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    response = requests.get(url=url,headers=headers)
    response.encoding = response.apparent_encoding
    json_ = response.text

    #处理json数据中的干扰字符串
    noise_str_start = f'lmanac["{year}"] ='
    #只有在当年而非year时，返回的json数据中的尾部字符串最后的分号在大括号外
    #tips: 网页中的json字符串，内部键值用双引号，外部单引号
    cur_year_end = ';if(typeof(lmanac_2345)!="undefined"){lmanac_2345()};'
    #当年之外的其他年份的尾部字符串分号在大括号里面
    other_year_end = ';if(typeof(lmanac_2345)!="undefined"){lmanac_2345();}'
    #用json_s表示头部字符串处理结果
    json_s = json_.replace(noise_str_start,"")
    #获取当前时间的年份
    cur_year = datetime.datetime.now().year
    #json_se表示尾部字符串处理
    if cur_year == year:
        json_se = json_s.replace(cur_year_end,"")
    else:
        json_se = json_s.replace(other_year_end,"")
    return json_se

def json_resolver(year,json_se,custom):

    json2dic = json.loads(json_se)
    print(f"宜{custom}的日期:")
    for day in json2dic.keys():
        fitting = json2dic[day]['y']
        month = int(day[1:3])
        day = int(day[3:])

        if custom in fitting:

            solar_date = datetime.datetime(year,month,day)
            sd_format = solar_date.strftime("%Y-%m-%d")
            ludar_date = ZhDate.from_datetime(solar_date)

            #将该zhdate对象强转为字符串，提取到天数
            ludar_date = str(ludar_date)
            gs = re.findall("(\d+)",ludar_date)
            assert len(gs) == 3
            date = datetime.datetime(int(gs[0]),int(gs[1]),int(gs[2]))
            ld_format = date.strftime("%Y-%m-%d")
            if int(gs[2]) % 2 == 0:
                print(f"公历日期: {sd_format}, 农历日期: {ld_format}")
            else:
                continue


if __name__ == "__main__":
    year = datetime.datetime.now().year
    json_se = get_json(year)

    json_resolver(year,json_se,"嫁娶")













