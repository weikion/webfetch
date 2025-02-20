###########################################################################
## 指定网址内容转稿
## https://www.sindow.net/
## author：weiziqian
## contact：43188540
###########################################################################

# http://www.news.cn/politics/leaders/20231225/06ba7f4a60ab41d58e8abc3052aded04/c.html
# https://www.southcn.com/node_07e973c1a3/9da95bb922.shtml
# http://www.chinanews.com.cn/gn/shipin/cns/2023/12-26/news978636.shtml
# https://h.xinhuaxmt.com/vh512/share/11827152?d=134b437&channel=weixin
# http://www.news.cn/fortune/2023-12/22/c_1130042613.htm
# http://www.chinanews.com.cn/gn/2023/12-22/10133192.shtml
# https://wap.peopleapp.com/article/7294049/7132130
# https://content-static.cctvnews.cctv.com/snow-book/index.html?item_id=8378179903021996147&t=1702701159787&toc_style_id=feeds_default&track_id=8F3845CA-D75E-4142-A828-D3C968273E29_724396775854&share_to=copy_url
# https://news.cctv.com/2023/12/16/ARTIv6yR0nipCGuyOjiSoT7k231216.shtml
# http://wap.cztv.com/articles/index.html?pubId=2229472
# http://www.qstheory.cn/dukan/qs/2024-04/15/c_1130109121.htm
# https://app.xdplus.cn/xdkb/template/displayTemplate/news/newsDetail/24/32809.html?isShare=true

import sys
import os
import wx
import json
import requests
import asyncio
from bs4 import BeautifulSoup
from pyppeteer import launch
from urllib.parse import urlparse
from libs.login import LoginFrame
from libs.frame import MainFrame
from libs.helper import keep_html_tags, read_json
import multiprocessing as mp
from multiprocessing import Value, Manager, Process

# 初始化session对象
session = requests.session()
# webdriver 用户目录
current_dir = os.getcwd()
user_data_dir = os.path.join(current_dir, "temp")
chromium_dir = os.path.join(current_dir, "chrome-win32/chrome.exe")

# 版本信息
about = {
    'name': 'webfetch',
    'version': 'beta1.2.1'
}

ua_pc = '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
ua_h5 = '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'

# 浏览器参数
launch_args = {
    "headless": True,
    "userDataDir": user_data_dir,
    "executablePath": chromium_dir,
    "args": [
        "--start-maximized",
        "--no-sandbox",
        "--disable-infobars",
        "--ignore-certificate-errors",
        "--log-level=3",
        "--enable-extensions",
        "--window-size=1920,1080",
        "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
        # "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) "Chrome/78.0.3904.97 Safari/537.36",
        # "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "like Gecko) Mobile/15E148",
    ],
}

# 域名对应的解析器
domain_to_parser = dict()
# domain_to_parser = {
#     'news.cn': {'def': 'xinhua_parser', 'name': '新华网'},
#     'h.xinhuaxmt.com': {'def': 'xinhua_h5_parser', 'name': '新华网H5'},
#     'www.southcn.com': {'def': 'southcn_parser', 'name': '南方网'},
#     'content-static.cctvnews.cctv.com': {'def': 'cctv_app_parser', 'name': '央视新闻客户端'},
#     'news.cctv.com': {'def': 'cctv_parser', 'name': '央视网'},
#     'www.chinanews.com.cn': {'def': 'chinanews_parser', 'name': '中新网'},
#     'wap.peopleapp.com': {'def': 'peopleapp_h5_parser', 'name': '人民日报H5'},
# }


domain_to_parser['www.news.cn'] = {'def': 'xinhua_parser', 'name': '新华网', 'ua': 'ua_pc'}


async def xinhua_parser(soup, url):
    platform = ''
    news_title = ''
    # news_body = ''

    if soup.find('div', {"class": "header domPC"}):
        platform = soup.find('div', {"class": "header domPC"}).find('div', {"class": "source"}).get_text()
        platform = platform.replace('来源：', '')
        platform = platform.strip("\n")  # 去掉尾部的换行和空格
    elif soup.find('div', {"class": "xl-cont-head"}):
        platform = soup.find('div', {"class": "xl-cont-head"}).find('div', {"class": "source"}).get_text()
        platform = platform.replace('来源：', '')
        platform = platform.strip("\n")  # 去掉尾部的换行和空格
    # print(platform)

    if soup.find('div', {"class": "header domPC"}):
        news_title = soup.find('div', {"class": "header domPC"}).find('h1').get_text()
    elif soup.find('div', {"class": "xl-cont-head"}):
        news_title = soup.find('div', {"class": "xl-cont-head"}).find('h1').get_text()
    # print(news_title)

    # 替换图片路径
    news_body_node = soup.find('div', {"id": "detail"})
    img_tags = news_body_node.find_all('img')
    url_path = os.path.dirname(url)

    for img in img_tags:
        # 获取原始的src属性值
        old_src = img['src']
        # 修改src属性值为新的值
        if old_src.find('http', 0, 5) == -1:
            img['src'] = f"{url_path}/{old_src}"
    news_body = news_body_node.prettify()

    # print(news_body)
    return [platform, news_title, news_body]


domain_to_parser['h.xinhuaxmt.com'] = {'def': 'xinhua_h5_parser', 'name': '新华网移动版', 'ua': 'ua_h5'}


async def xinhua_h5_parser(soup, url):
    platform = soup.find('header').find('p', {"class": "hender-info-source-v7"}).get_text()
    platform = platform.replace('来源：', '')
    platform = platform.strip("\n")  # 去掉尾部的换行和空格
    # print(platform)
    news_title = soup.find('header').find('h1').get_text()
    # print(news_title)
    news_body_node = soup.find('section', {"class": "main-text-container"})
    img_tags = news_body_node.find_all('img')

    # 懒加载机制，如果有data-src值，则赋值到src
    for img in img_tags:
        try:
            img['src'] = img['data-src']
        except KeyError:
            pass

    news_body = news_body_node.prettify()
    # print(news_body)
    return [platform, news_title, news_body]


domain_to_parser['www.southcn.com'] = {'def': 'southcn_parser', 'name': '南方网', 'ua': 'ua_pc'}


async def southcn_parser(soup, url):
    platform = soup.find('span', {"id": "source_baidu"}).get_text()
    platform = platform.replace('来源：', '')
    # print(platform)
    news_title = soup.find('h2', {"id": "article_title"}).get_text()
    # print(news_title)
    news_body = soup.find('div', {"id": "content"}).prettify()
    # print(news_body)
    return [platform, news_title, news_body]


domain_to_parser['content-static.cctvnews.cctv.com'] = {'def': 'cctv_app_parser', 'name': '央视新闻移动版', 'ua': 'ua_h5'}


async def cctv_app_parser(soup, url):
    platform = soup.find('div', {"class": "index-header"}).find('div', {"class": "media-name"}).get_text()
    # print(platform)
    news_title = soup.find('div', {"class": "index-header"}).find('h1').get_text()
    # print(news_title)
    news_body_node = soup.find('article', {"class": "article-content"})

    # 替换视频标签
    if news_body_node.find('video'):
        news_body_node.find('div', {"class": "container-video"}).string = news_body_node.find('video').prettify()

    news_body = news_body_node.prettify()
    # print(news_body)
    return [platform, news_title, news_body]


domain_to_parser['news.cctv.com'] = {'def': 'cctv_parser', 'name': '央视网', 'ua': 'ua_pc'}


async def cctv_parser(soup, url):
    platform = '央视网'
    # print(platform)
    news_title = soup.find('div', {"id": "title_area"}).find('h1').get_text()
    # print(news_title)
    if soup.find('div', {"id": "content_area"}):
        news_body = soup.find('div', {"id": "content_area"}).prettify()
    elif soup.find('div', {"id": "text_area"}):
        news_body = soup.find('div', {"id": "text_area"}).prettify()

    # print(news_body)
    return [platform, news_title, news_body]


domain_to_parser['www.chinanews.com.cn'] = {'def': 'chinanews_parser', 'name': '中国新闻网', 'ua': 'ua_pc'}


async def chinanews_parser(soup, url):
    platform = '中国新闻网'
    news_title = ''
    news_body = ''

    if soup.find('div', {"class": "content_title"}):
        news_title = soup.find('div', {"class": "content_title"}).find('div', {"class": "title"}).get_text()  # 视频新闻
    elif soup.find('h1', {"class": "content_left_title"}):
        news_title = soup.find('h1', {"class": "content_left_title"}).get_text()  # 图片新闻
    elif soup.find('div', {"class": "newscontent"}):
        news_title = soup.find('div', {"class": "newscontent"}).find('div', {"class": "title"}).get_text()  # H5版标题，图文类
    elif soup.find('div', {"class": "van-action-sheet__content"}):
        news_title = soup.find('div', {"class": "van-action-sheet__content"}).find('div', {"class": "sheet-title"}).get_text()  # H5版标题，视频类
    # print(news_title)

    if soup.find('div', {"class": "video-pic"}):
        news_body = soup.find('div', {"class": "video-pic"}).prettify()  # 视频新闻
        if soup.find('div', {"class": "content_desc"}):
            news_body += soup.find('div', {"class": "content_desc"}).prettify()  # 视频新闻
    elif soup.find('div', {"class": "content_maincontent_content"}):  # 图片新闻
        news_body = soup.find('div', {"class": "content_maincontent_content"}).prettify()
    elif soup.find('div', {"class": "newscontent"}):
        news_body_node = soup.find('div', {"class": "newscontent"})  # H5版内容，图文类
        news_body_node.find('div', {"class": "title"}).extract()
        news_body_node.find('div', {"class": "pubtime"}).extract()
        news_body_node.find('div', {"class": "related-topic"}).extract()
        news_body = news_body_node.prettify()
    elif soup.find('div', {"class": "van-action-sheet__content"}):  # H5版内容，视频类
        video_content = soup.find('div', {"class": "videoimgbox"}).find('video').prettify()
        news_body_node = soup.find('div', {"class": "van-action-sheet__content"}).find('div', {"class": "content"})
        news_body_node.find('div', {"class": "sheet-title"}).extract()
        news_body_node.find('div', {"class": "pubtime"}).extract()
        news_body = video_content + news_body_node.prettify()
    # print(news_body)

    return [platform, news_title, news_body]


domain_to_parser['m.chinanews.com'] = {'def': 'chinanews_h5_parser', 'name': '中国新闻网移动版', 'ua': 'ua_h5'}


async def chinanews_h5_parser(soup, url):
    platform = "中国新闻网"
    # print(platform)

    if soup.find('div', {"class": "newscontent"}):
        news_title = soup.find('div', {"class": "newscontent"}).find('div', {"class": "title"}).get_text()  # H5版标题，图文类
    elif soup.find('div', {"class": "van-action-sheet__content"}):
        news_title = soup.find('div', {"class": "van-action-sheet__content"}).find('div', {"class": "sheet-title"}).get_text()  # H5版标题，视频类
    # print(news_title)

    if soup.find('div', {"class": "newscontent"}):
        news_body_node = soup.find('div', {"class": "newscontent"})  # H5版内容，图文类
        news_body_node.find('div', {"class": "title"}).extract()
        news_body_node.find('div', {"class": "pubtime"}).extract()
        news_body_node.find('div', {"class": "related-topic"}).extract()
        news_body = news_body_node.prettify()
    elif soup.find('div', {"class": "van-action-sheet__content"}):  # H5版内容，视频类
        video_content = soup.find('div', {"class": "videoimgbox"}).find('video').prettify()
        news_body_node = soup.find('div', {"class": "van-action-sheet__content"}).find('div', {"class": "content"})
        news_body_node.find('div', {"class": "sheet-title"}).extract()
        news_body_node.find('div', {"class": "pubtime"}).extract()
        news_body = video_content + news_body_node.prettify()
    # print(news_body)

    return [platform, news_title, news_body]


domain_to_parser['wap.peopleapp.com'] = {'def': 'peopleapp_h5_parser', 'name': '人民日报移动版', 'ua': 'ua_h5'}


async def peopleapp_h5_parser(soup, url):
    platform = soup.find('div', {"class": "head-info normal-info"}).find('span', {
        "class": "pr10 head-info-copyfrom"}).get_text()
    # print(platform)
    news_title = soup.find('h1', {"class": "title"}).get_text()
    # print(news_title)
    news_body = soup.find('div', {"class": "article article-detail"}).prettify()
    # print(news_body)
    return [platform, news_title, news_body]


domain_to_parser['wap.cztv.com'] = {'def': 'cztv_h5_parser', 'name': '中国蓝新闻', 'ua': 'ua_h5'}


async def cztv_h5_parser(soup, url):
    platform = '中国蓝新闻'
    # print(platform)
    news_title = soup.find('p', {"class": "header"}).get_text()
    # print(news_title)
    news_body = soup.find('div', {"class": "viewdt"}).prettify()
    # print(news_body)
    return [platform, news_title, news_body]


domain_to_parser['www.qstheory.cn'] = {'def': 'qstheory_parser', 'name': '求是网', 'ua': 'ua_pc'}


async def qstheory_parser(soup, url):
    platform = '求是网'
    # print(platform)
    news_title = soup.find('div', {"class": "inner"}).find('h1').get_text()
    news_title = news_title.strip("\n")  # 去掉尾部的换行和空格
    # print(news_title)

    # 替换图片路径
    news_body_node = soup.find('div', {"class": "inner"}).find('div', {"class": "text"})
    img_tags = news_body_node.find_all('img')
    url_path = os.path.dirname(url)

    for img in img_tags:
        # 获取原始的src属性值
        old_src = img['src']
        # 修改src属性值为新的值
        if old_src.find('http', 0, 5) == -1:
            img['src'] = f"{url_path}/{old_src}"

    news_body = news_body_node.prettify()
    # print(news_body)
    return [platform, news_title, news_body]


domain_to_parser['app.xdplus.cn'] = {'def': 'xdplus_parser', 'name': '现代快报', 'ua': 'ua_h5'}


async def xdplus_parser(soup, url):
    platform = '现代快报'
    # print(platform)
    news_title = soup.find('h2', {"id": "title"}).get_text()
    news_title = news_title.strip("\n")  # 去掉尾部的换行和空格
    # print(news_title)
    news_body_node = soup.find('div', {"class": "main-content-box"})
    img_tags = news_body_node.find_all('img')

    # 懒加载机制，如果有data-src值，则赋值到src
    for img in img_tags:
        try:
            img['src'] = img['data-src']
        except KeyError:
            pass

    news_body = news_body_node.prettify()
    # print(news_body)
    return [platform, news_title, news_body]

async def open_page(browser, url, data, i):
    temp_data = data['data']
    temp_data[i][4] = '正在采集...'
    temp_data[i][5] = wx.Colour(255, 255, 0, 255)
    data['data'] = temp_data
    page = await browser.newPage()
    await page.goto(url)
    await asyncio.sleep(3)  # 等网页加载完

    # 获取当前页面高度，滚动页面到底部，触发页面的懒加载
    # currentHeight = await page.evaluate("document.body.scrollHeight")
    # while True:
    #     # 向下滚动1像素
    #     await page.evaluate(f"window.scrollTo({{top: {currentHeight}, behavior: 'smooth'}})")
    #     # 等待页面加载新内容
    #     await page.waitForFunction(f"document.body.scrollTop + window.innerHeight >= document.body.offsetHeight",
    #                                timeout=1000)
    #     newHeight = await page.evaluate("document.body.scrollHeight")
    #     if newHeight == currentHeight:
    #         break
    #     currentHeight = newHeight

    # 央视移动的懒加载，要触发滚动到底部
    if await page.querySelector(".editor"):
        await page.hover(".editor")

    # 中国新闻网的视频新闻加载详情
    if await page.querySelector(".vertical-title"):
        await page.click(".vertical-title span")

    await asyncio.sleep(1)  # 等网页加载完

    task = await page.content()
    # print(task)
    soup = BeautifulSoup(task, 'html.parser')
    # print(soup.prettify())
    res = urlparse(url)
    domain = res.netloc

    try:
        page_data = await eval("{0}".format(domain_to_parser[domain]['def']))(soup, url)
        msg = '采集成功'
        color = wx.Colour(0, 255, 0, 255)
        data['complete_count'] += 1
    except (ValueError, AttributeError):
        page_data = ['', data['data'][i][2], '']
        msg = '采集失败'
        color = wx.Colour(255, 0, 0, 255)

    # print(page_data)
    temp_data = data['data']
    temp_data[i][3] = page_data[0]
    temp_data[i][2] = page_data[1]
    temp_data[i][4] = msg
    temp_data[i][5] = color
    temp_data[i][6] = await keep_html_tags(page_data[2])
    data['data'] = temp_data

    # await page.close()


async def open_browser(data):
    tasks = []

    # 根据域名使用不同的ua，注：实现不了，因为是用多个标签打开网页
    # res = urlparse(data['data'][0][1])
    # domain = res.netloc
    # if domain in domain_to_parser:
    #     launch_args['args'][7] = domain_to_parser[domain]['ua']

    browser = await launch(**launch_args)
    for i in range(len(data['data'])):
        url = data['data'][i][1]

        if data['data'][i][4] == '不能采集':  # 不能采集的跳过
            continue

        # await asyncio.gather(open_page(browser, url, urls_grid, i))
        tasks.append(open_page(browser, url, data, i))
    await asyncio.gather(*tasks)
    await browser.close()
    data['complete'] = 1


def fetch_task(data):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(open_browser(data))
    # loop.close()


class Main(MainFrame):
    def __init__(self, parent, username, expires):
        MainFrame.__init__(self, parent, username, expires)

        # 线程列表
        self.processes = []

    # 提交
    def submit(self, event):
        self.submit_btn.Disable()
        del res_data['data'][:]
        urls = self.urls.GetValue()
        if len(urls) > 0:  # 有内容才能继续
            urls = urls.split('\n')
            # print(urls)
            # 渲染grid
            index = 0
            temp_data = []
            for url in urls:
                # 超过10行跳出
                if index > 9:
                    break
                url = url.strip()
                # print(url)
                if len(url) > 0:  # 跳过空行
                    node_list = [str(index + 1), url, " "]
                    # self.res_info.SetCellValue(index, 0, str(index + 1))
                    # self.res_info.SetCellValue(index, 1, url)  # url[:46]

                    res = urlparse(url)
                    domain = res.netloc
                    if domain in domain_to_parser:
                        platform = domain_to_parser[domain]['name']
                        status = '可以采集'
                        bg_color = wx.GREEN
                    else:
                        platform = '未知来源'
                        status = '不能采集'
                        bg_color = wx.RED
                    # self.res_info.SetCellValue(index, 3, platform)
                    node_list.append(platform)
                    # self.res_info.SetCellValue(index, 4, status)
                    node_list.append(status)
                    # self.res_info.SetCellBackgroundColour(index, 4, bg_color)
                    node_list.append(bg_color)

                    node_list.append("")

                    temp_data.append(node_list)

                    index = index + 1
            res_data['data'] = temp_data
            # self.submit_btn.Disable()
            self.urls.Clear()
            self.start_btn.Enable()
            self.submit_btn.Enable()

            self.m_timer1.Start(1000)
        else:
            box = wx.MessageDialog(None, '请输入转稿的网址', u'提示', wx.OK)
            box.ShowModal()
            box.Destroy()

    # 开始采集
    def start(self, event):
        # print(res_data)
        if len(res_data['data']) > 0:
            browser_mp = Process(target=fetch_task, args=(res_data,))
            browser_mp.daemon = True
            browser_mp.start()
            self.processes.append(browser_mp)

            # main(self.res_info, self.push_db_btn)
            self.start_btn.Disable()
            self.set_panel.Disable()

    # 关闭程序
    def quit(self, event):
        box = wx.MessageDialog(None, '确定要关闭程序吗？', u'提示', wx.YES_NO | wx.ICON_QUESTION)
        if box.ShowModal() == wx.ID_YES:
            # self.Close(True)
            for p in self.processes:
                print('process %d-%d terminate' % (os.getpid(), p.pid))
                p.terminate()
            self.Destroy()
            sys.exit()
            # print(fetch_exit.value)

        box.Destroy()

    # 加入稿库
    def push_db(self, event):
        config = read_json('config')
        gaoku_url = config['gaoku_url']
        if gaoku_url.strip() == "":
            msg = '未配置稿库接口地址'
        else:
            try:
                self.push_db_btn.Disable()
                for i in range(len(res_data['data'])):
                    data = {
                        'src_url': res_data['data'][i][1],  # 来源网址
                        'title': res_data['data'][i][2],
                        'content': res_data['data'][i][6],
                        'media_name': res_data['data'][i][3],
                    }
                    # print(data)
                    res_byte = session.post(gaoku_url, data=data)
                    json_data = res_byte.json()
                    # print(json_data)

                self.set_panel.Enable()
                self.start_btn.Disable()
                self.m_timer1.Stop()

                # 重置底色
                for i in range(len(res_data['data'])):
                    self.res_info.SetCellBackgroundColour(i, 4, wx.WHITE)

                del res_data['data'][:]  # 清空列表
                res_data['complete'] = 0  # 重置状态
                res_data['complete_count'] = 0  # 重置状态
                self.res_info.ClearGrid()

                msg = '加入稿库成功！'
            except Exception:
                msg = '网络出错，请重试'

        box = wx.MessageDialog(None, msg, u'提示', wx.OK)
        box.ShowModal()
        box.Destroy()


    # 重置
    def reset(self, event):
        box = wx.MessageDialog(None, '确定要清除采集结果吗？', u'提示', wx.YES_NO | wx.ICON_QUESTION)
        if box.ShowModal() == wx.ID_YES:
            self.push_db_btn.Disable()
            self.set_panel.Enable()
            self.start_btn.Disable()
            self.m_timer1.Stop()

            # 重置底色
            for i in range(len(res_data['data'])):
                self.res_info.SetCellBackgroundColour(i, 4, wx.WHITE)

            del res_data['data'][:]  # 清空列表
            res_data['complete'] = 0  # 重置状态
            res_data['complete_count'] = 0  # 重置状态
            self.res_info.ClearGrid()

        box.Destroy()

    # 计时器触发事件
    def timer_func(self, event):
        # print(res_data)
        if len(res_data['data']) > 0:
            for i in range(len(res_data['data'])):
                self.res_info.SetCellValue(i, 0, res_data['data'][i][0])
                self.res_info.SetCellValue(i, 1, res_data['data'][i][1])
                self.res_info.SetCellValue(i, 2, res_data['data'][i][2])
                self.res_info.SetCellValue(i, 3, res_data['data'][i][3])
                self.res_info.SetCellValue(i, 4, res_data['data'][i][4])
                self.res_info.SetCellBackgroundColour(i, 4, res_data['data'][i][5])

            if res_data['complete'] == 1:
                self.reset_btn.Enable()
                # 如果有成功的采集，加入稿库按钮才可用
                if res_data['complete_count'] > 0:
                    self.push_db_btn.Enable()


if __name__ == "__main__":
    mp.freeze_support()  # 解决window下无限的开进程的问题
    res_data = Manager().dict()  # 采集的数据
    res_data['data'] = []
    res_data['complete'] = 0  # 采集过程完成
    res_data['complete_count'] = 0  # 成功的采集数量
    login_status = Value('I', 0)  # 登录成功
    login_username = Manager().dict()  # 登录的账号信息

    # 先创建临时目录
    if not os.path.exists(user_data_dir):
        os.mkdir(user_data_dir)

    # 开始进程
    app = wx.App()
    config = read_json('config')
    login_url = config['login_url']

    if login_url.strip() == "":
        main_win = Main(None, '', '')
        main_win.SetTitle(main_win.GetTitle() + '-' + about['version'])
        main_win.Show()  # 显示主窗口
    else:
        login_win = LoginFrame(None, Main, about, session, login_status, login_username)
        login_win.Show()

    app.MainLoop()
