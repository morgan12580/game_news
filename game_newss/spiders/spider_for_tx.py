#!/user/bin/env python3
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from game_newss.database.models.models_for_news import Mod_game, Images, Hot_news, Today_news, session_db,  QieVideo, \
    FirmNews, FirstVideo, GameVideo, ModPerson, ModALLGame, RecentGame, HotGameRank
import json
import time


# 请求网页数据
def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


# 热门游戏名单
def get_mod_games_name(soup):
    results = soup.find_all('div', class_="guide_item")
    for result in results:
        a_all = result.find_all('a', attrs={'target': '_blank'})
        for a in a_all:
            game_name = a.text
            class_value = a.get('class')
            game_url = a.get('href')
            game_dic = {
                'name': game_name,
                'url': game_url,
                'clss': class_value
            }
            print(game_dic)
            time.sleep(1)
            Mod_game.save_with_item(game_dic)


# 获取轮播图片信息
def get_images(soup):
    all_a = soup.find_all('a', attrs={'href': 'javascript:;'})
    for a in all_a[1:-2]:
        image_text = a.find('img').get('alt')
        image_url = a.find('img').get('src')
        image_dic = {
            'text': image_text,
            'url': image_url
        }
        # print(image_dic)
        time.sleep(1)
        Images.save_with_item(image_dic)


# 获取轮播图片信息
def get_images2(soup):
    div = soup.find('div', attrs={'id': 'focus_img_box', 'class':'focus_img_box'})
    all_li = div.find_all('li')
    for li in all_li[:10]:
        image_alt = li.find('img').get('alt')
        image_url = li.find('img').get('src')
        new_url = li.find('a').get('href')
        dic = {
            'image_alt': image_alt,
            'image_url': image_url,
            'new_url': new_url
        }
        time.sleep(1)
        print(dic)
        Images.save_with_item(dic)


# 获取当前界面hot news
def get_hot_news(soup):
    div = soup.find('div', class_='hot_news')
    values = div.find_all('li')
    for value in values:
        dic = {
            'content': value.find('a', attrs={'target': "_blank"}).text,
            'url': value.find('a', attrs={'target': "_blank"}).get('href'),
            'data': value.find('p').text
        }
        print(dic)
        time.sleep(1)
        Hot_news.save_with_item(dic)


# 获取当前游戏最新新闻

def get_today_news(soup):
    divs = soup.find_all('div', class_='pic_txt_list t_news_list')
    for div in divs:
        a = div.find('a', class_="pic")
        alt = a.find('img').get('alt')
        src = a.find('img').get('src')
        new_url = a.get('href')
        news_dic = {
                'news_text': alt,
                'news_image': src,
            }
        span = div.find('span', class_="source").text
        news_dic['news_author'] = span
        if new_url.startswith("http://new.qq.com"):
            result = get_detail_for_other(new_url)
            # 将list转换为str 存入数据库 list不能直接存入数据库
            # 还可以考虑 序列化。
            news_dic['content'] = ''.join(result[0])
            news_dic['img'] = ','.join(result[1])
        print(news_dic)
        time.sleep(1)
        Today_news.save_with_item(news_dic)


# 获取非腾讯原创的新闻详情
# 上面函数已经将此函数运行 main函数中不需要在运行
def get_detail_for_other(url):
    list = []
    content = []
    image = []
    soup = get_soup(url)
    ps = soup.find_all('p', class_='one-p')
    for p in ps:
        if p.text:
            content.append(p.text.replace('\u3000', '').strip())
        if p.find('img'):
            image.append('http:'+p.find('img').get('src'))
    list.append(content)
    list.append(image)
    return list


# 获取当前界面企鹅电竞的视频信息
def get_qie_video(soup):
    div = soup.find('div', class_='mod_bd mod_list_pic')
    results = div.find_all('a', class_='mod_poster')
    for result in results:
        video_url = result.get('href')
        img = result.find('img', attrs={'name': 'page_cnt_1'})
        video_name = img.get('alt')
        video_picture = img.get('_src')
        video_dic = {
             'video_name': video_name,
             'video_picture': video_picture,
             'video_url': video_url
         }
        print(video_dic)
        time.sleep(1)
        QieVideo.save_with_item(video_dic)


# 获取厂商新闻
# (每个新闻主页模版不同，暂时不爬取新闻，直接获取url)
def get_firm_news(soup):
        ul = soup.find('ul', class_='txt_list')
        results = ul.find_all('a')
        for result in results:
            news_url = result.get('href')
            news_title = result.text.replace('\r', '').replace('\n', '').strip()
            dic = {
                'firm_news_title': news_title,
                'firm_news_url': news_url
            }
            print(dic)
            time.sleep(1)
            FirmNews.save_with_item(dic)


# 获取当前页面各类游戏视频信息
def get_game_video(soup):
    # 置顶的视频相关信息
    div1 = soup.find('div', class_='video_focus fl')
    first_video_url = div1.find('a').get('href')
    first_video_title = div1.find('img').get('alt').split('<br>')[1]
    first_video_author = div1.find('img').get('alt').split('<br>')[0]
    first_video_photo = div1.find('img').get('src')
    dict = {
        'video_title': first_video_title,
        'video_photo': first_video_photo,
        'video_url': first_video_url,
        'video_author': first_video_author
    }
    print(dict)
    time.sleep(1)
    FirstVideo.save_with_item(dict)
    # 第一类视频相关信息
    div2 = soup.find('div', class_='fr mod_list_pic video_list')
    save_video(div2)
    # 第二类视频相关信息
    div3 = soup.find('div', class_='mod_list_pic video_list video_sdlist')
    save_video(div3)
    # 第三类视频相关信息
    div4 = soup.find('div', class_='mod_list_pic video_list video_sdlistmore')
    save_video(div4)


# 所有视频:
def save_video(div):
    results = div.find_all('li')
    for result in results:
        if result.find('a', class_='mod_poster'):
            video_url = result.find('a').get('href')
            video_photo = result.find('a').find('img').get('_src')
            video_title1 = result.find('span', class_='mod_version').text
        if result.find('h3'):
            video_title2 = result.find('h3').text
        if result.find('p', class_='video_other'):
            video_author = result.find('p', class_='video_other').find('a').text
            author_index = result.find('a', class_='fl video_user').get('href')
            video_number = result.find('span', class_='fr video_num').text
        dic = {
            'video_title': video_title1+video_title2,
            'video_photo': video_photo,
            'video_url': video_url,
            'video_author': video_author,
            'author_index': author_index,
            'author_number': video_number
        }
        print(dic)
        time.sleep(1)
        GameVideo.save_with_item(dic)


# 当前最火的腾讯个人主页
def get_mod_person(soup):
    div = soup.find('div', class_='mod_zhubo mod_list_pic')
    results = div.find_all('li')
    for result in results:
        person_url = result.find('a').get('href')
        person_name = result.find('img').get('alt')
        person_photo = result.find('img').get('_src')
        dict = {
            'photo': person_photo,
            'name': person_name,
            'url': person_url
        }
        print(dict)
        time.sleep(1)
        ModPerson.save_with_item(dict)


# 获取手机游戏 客户端游戏等等游戏新闻
def get_data(div):
    lis = div.find_all('li')
    for li in lis:
        title1 = li.find('a').text.replace('\n', '').replace('\r', '').strip()
        create_time = li.find('span', class_='time_inner').text.replace('\n', '').replace('\r', '').strip()
        dict = {
            'title': title1,
            'create_time': create_time
        }
        url = li.find('a').get('href')
        if get_phone_detail_news(url):
            dict['content'] = ''.join(get_phone_detail_news(url))
        else:
            dict['content'] = url
        print(dict)
        time.sleep(1)
        ModALLGame.save_with_item(dict)


# 在爬取过程中，发现详情界面采取了ajax请求，此时request的url变化
# 该函数只爬取request请求的内容
def get_phone_detail_news(url):
    list = []
    soup = get_soup(url)
    div = soup.find('div', attrs={'bosszone': 'content'})
    if div:
        ps = div.find_all('p', attrs={'style': 'TEXT-INDENT: 2em'})
        for p in ps:
           list.append(p.text)
    return list


# 获取手游信息
# 手机游戏为数据库表mode_phone的[:8]
# 客户端游戏
# 在分析结构中发现与手机游戏前端界面结构一模一样
# 所以将其统一起来 存入同一个数据库
# 客户端游戏为数据库表mode_phone的[8:16]
# 网页游戏数据为数据库表mode_phone的[16:24]
# 游戏产业新闻 数据库[24:32]
# 单机/主机游戏  数据库 [32:40]
# 专区资讯 数据库 [40:48]
def get_all_game_value(soup):
    divs = soup.find_all('div', class_='game_txtnews fr')
    for div in divs:
        get_data(div)


# 获取近期测试游戏相关新闻：
def get_recent_test_game_news(soup):
    div = soup.find('div', class_='mod_bd new_gamesrank')
    trs = div.find_all('tr')
    for tr in trs[1:]:
        tds = tr.find_all('td')
        test_time = tds[0].text
        game_name = tds[1].text
        test_style = tds[2].text
        download_url = tds[3].find('a').get('href')
        dict = {
            'test_time': test_time,
            'game_name': game_name,
            'test_style': test_style,
            'download_url': download_url
        }
        print(dict)
        time.sleep(1)
        RecentGame.save_with_item(dict)


# 热门游戏排行
# 数据分析 number 用于画柱状图
# json 画图
def hot_games_rank(soup):
    div = soup.find('div', class_='mod_bd hot_gamesrank')
    trs = div.find_all('tr')
    for tr in trs[1:]:
        tds = tr.find_all('td')
        rank = tds[0].text
        game_name = tds[1].find('a').text.replace('\n', '').strip()
        game_url = tds[1].find('a').get('href')
        number = tds[2].text
        dict = {
            'rank': rank,
            'game_name': game_name,
            'number': number,
            'url':game_url
        }
        print(dict)
        time.sleep(1)
        HotGameRank.save_with_item(dict)


# 主函数
def main():
    url = 'http://games.qq.com/'
    soup = get_soup(url)
    # print('*' * 20 + '111' + '*' * 20)
    # # 热门游戏
    # get_mod_games_name(soup)
    # print('*' * 20+'222'+'*' * 20)
    # # 轮播图片
    # get_images(soup)
    # print('*' * 20 + '333' + '*' * 20)
    # 火热新闻
    get_hot_news(soup)
    print('*' * 20 + '444' + '*' * 20)
    # # 今日新闻
    # get_today_news(soup)
    # print('*' * 20 + '555' + '*' * 20)
    # # 企鹅电竞
    # get_qie_video(soup)
    # print('*' * 20+'666'+'*' * 20)
    # # 厂商新闻
    # get_firm_news(soup)
    # print('*' * 20+'777'+'*' * 20)
    # # 游戏视频
    # get_game_video(soup)
    # print('*' * 20+'888'+'*' * 20)
    # # 所有游戏新闻 手游信息,客户端，网游，单机/主机游戏，专区资讯，
    # get_all_game_value(soup)
    # print('*' * 20+'999'+'*' * 20)
    # # 最火个人主播界面
    # get_mod_person(soup)
    # print('*' * 20+'101010'+'*' * 20)
    # # 近期测试游戏新闻
    # get_recent_test_game_news(soup)
    # print('*' * 20+'111111'+'*' * 20)
    # # 游戏排名
    # hot_games_rank(soup)
    # get_images2(soup)


if __name__ == '__main__':
    main()




