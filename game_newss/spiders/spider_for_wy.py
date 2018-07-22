#!/user/bin/env python3
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
from game_news.spider.models_for_tx_news import WangYiNews


def get_soup(url):

    headers = {
        'user-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Host': 'game.163.com',
        'Cookie': '__gads=ID=d831733be75093d0:T=1525003721:S=ALNI_MbcW2cqC5yAvFGkcM5A0NgJIlv7Wg; '
                  'UM_distinctid=163114e1e48ab9-0a33df8647781e-33607f06-13c680-163114e1e4968f; '
                  'vjuids=42c452901.163114e2167.0.d435635373802; vjlast=1525003723.1525003723.30; _'
                  'ntes_nnid=12ef853b0e9e1f960b9c691cd5088fbe,1525003723116; _ntes_nuid=12ef853b0e9e1f960b9c691cd5088fbe; '
                  'vinfo_n_f_l_n3=be379f0dfb41694e.1.0.1525003723127.0.1525003725270'

}
    demo = requests.get(url, headers=headers)
    demo.encoding = 'gb2312'
    soup = BeautifulSoup(demo.content, 'lxml')
    return soup


# 获取数据
def get_data(soup):
    response = soup.find('div', class_='news-list')
    results = response.find_all('li', class_='isotope-item')
    for result in results:
        url = result.find('a').get('href')
        # 有的新闻不是原创，而是直接转向另一个标签，所以排除掉此类新闻
        if url.startswith('//game.163.com/news/'):
            content = get_detail(url)
            if content:
                content_photo = ','.join(content[0])
                content_character = ''.join(content[1]).replace('\u3000', '').strip()
        else:
            # 跳过此次循环执行下一次
            continue
        title = result.find('a').find('span').text
        time = result.find('p', class_='time').text
        remark = result.find('p', class_='remark').text
        dict = {
            'title': title,
            'time': time,
            'remark': remark,
            'content_photo': content_photo,
            'content_character': content_character
        }
        WangYiNews.save_with_item(dict)


# 获取新闻详情
def get_detail(url):
    list1 = []
    list2 = []
    content = []
    soup = get_soup('http:'+url)
    response = soup.find('div', class_='artText')
    if response:
        results = response.find_all('p')
        for result in results:
            if result.find('img'):
                src = result.find('img').get('src')
                list1.append(src)
            else:
                list2.append(result.text)
        content.append(list1[-1:])
        content.append(list2)
    else:
        content = None
    return content


# 获取前20页的url
def get_url():
    list = []
    for x in range(1, 20):
        if x == 1:
            url = 'http://game.163.com/news/index.html'
            list.append(url)
        elif x != 6:
            url = 'http://game.163.com/news/index_{}.html'.format(x)
            list.append(url)
    return list


# 主函数
def main():
    for url in get_url():
        soup = get_soup(url)
        get_data(soup)


if __name__ == '__main__':
    main()
