# coding:utf-8


import sys

VER = 3
if sys.version_info < (3, 0):
    VER = 2

if VER == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')
    import urllib
else:
    import urllib.parse as urllib
import requests
import lxml.etree
import re
import sqlite3
import datetime


def get_data(url, params=None):
    '''提供url,返回数据'''
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
    }
    proxies = {
        # "http": "127.0.0.1:4541",
        # "https": "127.0.0.1:4541",
    }
    try:
        r = requests.get(url, headers=headers, params=params, proxies=proxies)
    # r.encoding = "GBK"
        data = r.text
    except:
        data = []
    return data


def get_photo_detail(url):
    """
    url
    :return:[name:url]
    """
    name = url.split('/')[-1]
    data = get_data(url)
    html = lxml.etree.HTML(data)
    url = html.xpath('''//*[@id="file"]/a/@href''')
    if not url:
        return []
    url = urllib.unquote(url[0])
    name = html.xpath('''// *[ @ id = "firstHeading"]/text()''')

    # print(url)
    return [name[0], url]


def format_abs(abs):
    _abstract = [n.strip('\n') for n in abs]
    _abstract.append('')
    abstract = []
    cc = ''
    for n in _abstract:
        if n == "" and cc != "":
            abstract.append(cc)
            cc = ''
        else:
            cc += n
    return abstract


def get_date_detail(url):
    print(u'开始分析页面')
    data = get_data(url)
    html = lxml.etree.HTML(data)

    url_tab = html.xpath(
        '''//table[@class="infobox vevent"]//a[@class="image"]/@href
        |//table[@class="infobox vcard"]//a[@class="image"]/@href
        |//table[@class="infobox geography vcard"]//a[@class="image"]/@href
        |//table[@class="infobox geography vcard vevent"]//a[@class="image"]/@href''')

    _abstract_tab = []
    for u in url_tab:
        cc = html.xpath('''//td//a[@href="''' + str(u) + '''"]/@title''')
        if not cc:
            cc = html.xpath('''//td//a[@href="''' + str(u) + '''"]/..//text()''')
        if not cc:
            cc = [u'暂无']
        cc = format_abs(cc)[0]
        _abstract_tab.append(cc)
    assert len(_abstract_tab) == len(url_tab), u'_abstract_tab 数目不对'

    # 爬gallery
    url_gal = html.xpath('''//*[@class="gallery mw-gallery-traditional"]/li/div[1]/div[1]//a/@href''')

    _abstract_gal = html.xpath('''//*[@class="gallery mw-gallery-traditional"]/li//div[@class="gallerytext"]//text()''')
    _abstract_gal = format_abs(_abstract_gal)
    assert len(_abstract_gal) == len(url_gal), u'_abstract_gal 数目不对'


    # 爬thumbinner
    _abstract_thu = []
    url_thu = html.xpath("""//*[@class="thumbinner"]/a/@href""")
    for u in url_thu:
        uu = html.xpath('''//*[@class="thumbinner"]//a[@href="''' + str(u) + '''"]/..//text()''')
        uu = format_abs(uu)[0]
        _abstract_thu.append(uu)
    assert len(_abstract_thu) == len(url_thu), u'_abstract_gal 数目不对'


    # 合并处理
    url = url_tab + url_thu + url_gal

    # 获取照片具体信息
    url_data = []
    for u in url:
        u = 'https://zh.wikipedia.org' + u
        url_data.append(get_photo_detail(u))

    # 合并处理
    abstract = _abstract_tab + _abstract_thu + _abstract_gal

    abstract = [re.sub(r'\[\d+\]', '', n) for n in abstract]

    assert len(abstract) == len(url_data), u'数目不对'

    photo_data = []
    for i in url_data:
        c = abstract.pop(0)
        i.append(c)
        photo_data.append(i)

    return photo_data


def save_data(data, type, pid):
    '''
    保存数据库
    :param data:[[name,url,abstract]...]
    :param type:
    :param pid:
    :return:
    '''
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    for d in data:
        if len(d) < 3:
            continue
        d[0] = d[0].replace("'", "")
        d[1] = d[1].replace("'", "")
        d[2] = d[2].replace("'", "")
        # print(d)
        sql = '''select id from war_photo where name='%s' and type=%s and relation=%s ''' % (d[0], type, pid)
        c.execute(sql)
        a = c.fetchall()
        if a:
            continue
        time = datetime.datetime.now()
        sql = """insert into war_photo (name,type,relation,url,abstract,add_time) VALUES ('%s','%s','%s','%s','%s','%s')""" % (
            d[0], type, pid, d[1], d[2], time)
        c.execute(sql)
        conn.commit()
        print('=====save one photo=====')
    conn.close()


def up_table(type):
    table = TYPE[type]

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    sql = """select id,name from %s """ % table
    c.execute(sql)
    names = c.fetchall()
    for n in names:
        print(n)
        url = "https://zh.wikipedia.org/wiki/" + str(n[1])
        data = get_date_detail(url)
        save_data(data, type, n[0])


if __name__ == '__main__':
    tt = [
        (1, u'国家'),
        (2, u'人物'),
        (3, u'事件'),
        (4, u'装备')
    ]

    TYPE = {
        1: 'war_country',
        2: 'war_personage',
        3: 'war_event',
        4: 'war_armament'
    }

    # url = 'https://zh.wikipedia.org/wiki/%E4%B9%9D%E4%B8%80%E5%85%AB%E4%BA%8B%E8%AE%8A'


    c = up_table(1)
