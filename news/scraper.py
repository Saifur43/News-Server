import requests
from urllib import request as req
from bs4 import BeautifulSoup

from .models import News

requests.packages.urllib3.disable_warnings()


# samakal news data collection
def samakal(url):
    url = url
    html_doc = req.urlopen(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    news = soup.find('div', class_='col-md-8 col-sm-12 col-xs-12')

    for title, link, img in zip(news.find_all('h4', class_='heading'), news.find_all('a', class_="link-overlay"),
                                news.find_all('img', class_='media-object img-btm-r img-60')):

        if News.objects.filter(title=title.string).exists():
            continue
        else:
            category_slug = str(link['href'].split('/')[3])
            new_news = News()
            new_news.source_name = 'সমকাল'
            new_news.source_slug = 'samakal'
            new_news.title = title.string
            new_news.link = link['href']
            new_news.img_link = img['src']
            new_news.category_slug = category_slug

            if category_slug == 'politics':
                new_news.category_name = 'রাজনীতি'
            elif category_slug == 'international':
                new_news.category_name = 'আন্তর্জাতিক'
            elif category_slug == 'bangladesh':
                new_news.category_name = 'বাংলাদেশ'
            elif category_slug == 'economics':
                new_news.category_name = 'অর্থনীতি'
            elif category_slug == 'entertainment':
                new_news.category_name = 'বিনোদন'
            elif category_slug == 'sports':
                new_news.category_name = 'খেলা'
            elif category_slug == 'probas':
                new_news.category_name = 'প্রবাস'
            else:
                new_news.category_name = 'বিবিধ'

            new_news.save()


# priyo news data collection
def priyo(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    news_list = soup.find_all('div', class_='pr-4 mc-10')

    for x in news_list:
        titles = x.find_all('h4')
        links = x.find_all('div', class_='article-image')
        tags = x.find_all('div', class_='article-description')

    for title, link, tag in zip(titles, links, tags):

        if News.objects.filter(title=title.text).exists():
            continue
        else:
            category_slug = tag.find('a').text
            new_news = News()
            new_news.source_name = 'প্রিয় সংবাদ'
            new_news.source_slug = 'Priyo'
            new_news.title = title.text
            new_news.link = "https://www.priyo.com" + str(link.find('a').get('href'))
            new_news.img_link = link.find('img')['src']
            new_news.category_slug = category_slug

            new_news.save()


# prothon alo news data collection
def palo(url):
    page = requests.get(url)
    news = BeautifulSoup(page.text, 'html.parser')

    for title, link, img, category in zip(news.find_all('h2', class_='title_holder'),
                                          news.find_all('a', attrs={'class': 'link_overlay'}),
                                          news.find_all('div', class_='image'),
                                          news.find_all('a', class_='category aitm')):

        if News.objects.filter(title=title.text).exists():
            continue
        else:
            category_slug = category.text
            new_news = News()
            new_news.source_name = 'প্রথম আলো'
            new_news.source_slug = 'ProthomAlo'
            new_news.title = title.text
            link2 = link.get('href')
            new_news.link = "https://www.prothomalo.com/" + str(link2)
            lnk = img.find('img')
            new_news.img_link = "http:" + str(lnk['src'])
            new_news.category_slug = category_slug

            new_news.save()


def kalerkonto(url):
    page = req.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    news_list = soup.find_all('div', class_='col-xs-12 home-top-news')

    for x in news_list:
        info = x.find_all('div', class_='col-xs-6')

    i = 0

    for title in info:
        if News.objects.filter(title=title.find('h2').text).exists():
            continue
        else:
            new_news = News()
            new_news.source_name = 'কালের কণ্ঠ'
            new_news.source_slug = 'KalerKonto'
            new_news.title = title.find('h2').text
            links = (title.find_all('a'))
            lnk = links[-1].get('href')
            if i == 0:
                new_news.link = "http://www.kalerkantho.com/" + str(lnk[1:])
            else:
                new_news.link = "http://www.kalerkantho.com/" + str(lnk)
            img_link = title.find('img')
            new_news.img_link = img_link['src']
            category = lnk.split('/')
            if i == 0:
                category_slug = category[2]
            else:
                category_slug = category[1]
            new_news.category_slug = category_slug

            if category_slug == 'Politics':
                new_news.category_name = 'রাজনীতি'
            elif category_slug == 'international':
                new_news.category_name = 'আন্তর্জাতিক'
            elif category_slug == 'national':
                new_news.category_name = 'বাংলাদেশ'
            elif category_slug == 'economics':
                new_news.category_name = 'অর্থনীতি'
            elif category_slug == 'entertainment':
                new_news.category_name = 'বিনোদন'
            elif category_slug == 'sport':
                new_news.category_name = 'খেলা'
            elif category_slug == 'probas':
                new_news.category_name = 'প্রবাস'
            else:
                new_news.category_name = 'বিবিধ'

            new_news.save()
            i = i + 1


def chanel_i(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    newslist = soup.find('div', class_='col-sm-12')

    for news in newslist.find_all('div', class_='item-content'):

        if News.objects.filter(title=news.find('h2').text).exists():
            continue
        else:
            new_news = News()
            new_news.source_name = 'চ্যানেল আই অনলাইন'
            new_news.source_slug = 'Chaneli'
            new_news.title = news.find('h2').text
            new_news.link = news.find('a').get('href')
            new_news.img_link = news.find('a')['data-src']
            tags = news.find_all('a')
            new_news.category_slug = tags[1].text
            new_news.save()

    newslist2 = soup.find('div', class_='col-sm-8 content-column')
    for news in newslist2.find_all('div', class_='item-inner clearfix'):

        if News.objects.filter(title=news.find('h2').text).exists():
            continue
        else:
            new_news = News()
            new_news.source_name = 'চ্যানেল আই অনলাইন'
            new_news.source_slug = 'Chaneli'
            new_news.title = news.find('h2').text
            new_news.link = news.find('a').get('href')
            style = news.find_all('a')[3]
            new_news.img_link = style['data-src']
            tags = news.find_all('a')
            new_news.category_slug = tags[2].text
            new_news.save()


def bdnews24(url):

    url1 = "https://bangla.bdnews24.com/world/"
    url2 = "https://bangla.bdnews24.com/bangladesh/"
    url3 = "https://bangla.bdnews24.com/politics/"
    url4 = "https://bangla.bdnews24.com/sport/"

    # Intenational news
    page = requests.get(url1)
    soup = BeautifulSoup(page.text, 'html.parser')

    info = soup.find_all('div', class_='column-1')
    news_list = info[1]
    for title, img in zip(news_list.find_all('a'), news_list.find_all('img')):
        if News.objects.filter(title=title.text).exists():
            continue
        else:
            new_news = News()
            new_news.source_name = 'বিডিনিউজ২৪'
            new_news.source_slug = 'bdnews24'
            new_news.title = title.text
            new_news.link = title.get('href')
            new_news.img_link = img['src']
            new_news.category_name = "আন্তর্জাতিক"
            new_news.category_slug = "international"
            new_news.save()

    # Bangaldesh News
    page = requests.get(url2)
    soup = BeautifulSoup(page.text, 'html.parser')

    info = soup.find_all('div', class_='column-1')
    news_list = info[1]
    for title, img in zip(news_list.find_all('a'), news_list.find_all('img')):
        if News.objects.filter(title=title.text).exists():
            continue
        else:
            new_news = News()
            new_news.source_name = 'বিডিনিউজ২৪'
            new_news.source_slug = 'bdnews24'
            new_news.title = title.text
            new_news.link = title.get('href')
            new_news.img_link = img['src']
            new_news.category_name = "বাংলাদেশ"
            new_news.category_slug = "national"
            new_news.save()

    # Poliics News
    page = requests.get(url3)
    soup = BeautifulSoup(page.text, 'html.parser')

    info = soup.find_all('div', class_='column-1')
    news_list = info[1]
    for title, img in zip(news_list.find_all('a'), news_list.find_all('img')):
        if News.objects.filter(title=title.text).exists():
            continue
        else:
            new_news = News()
            new_news.source_name = 'বিডিনিউজ২৪'
            new_news.source_slug = 'bdnews24'
            new_news.title = title.text
            new_news.link = title.get('href')
            new_news.img_link = img['src']
            new_news.category_name = "রাজনীতি"
            new_news.category_slug = "politics"
            new_news.save()

    # Sports News
    page = requests.get(url4)
    soup = BeautifulSoup(page.text, 'html.parser')

    news_list = soup.find('div', attrs={'id': 'main'})
    i = 1
    for title, img in zip(news_list.find_all('a'), news_list.find_all('img')):
        if i == 13:
            break

        elif News.objects.filter(title=title.text).exists():
            continue
        else:
            new_news = News()
            new_news.source_name = 'বিডিনিউজ২৪'
            new_news.source_slug = 'bdnews24'
            new_news.title = title.text
            new_news.link = title.get('href')
            new_news.img_link = img['src']
            new_news.category_name = "খেলা"
            new_news.category_slug = "sport"
            new_news.save()

        i = i + 1
