import requests
import json
import os



def get_herolist(url):
    url = url + 'js/herolist.json'
    json_response = requests.get(url)
    return json_response.json()


def get_html(url):
    url = url + 'herolist.shtml'
    response = requests.get(url)
    return response.text


def get_img(herolist):
    os.mkdir('images')
    for hero in herolist:
        ename = str(hero['ename'])
        url = 'https://game.gtimg.cn/images/yxzj/img201606/heroimg/' + ename + '/' + ename + '.jpg'
        img_response = requests.get(url)
        with open('images/' + ename + '.jpg', 'wb') as code:
            code.write(img_response.content)


def main():
    url = 'https://pvp.qq.com/web201605/'
    html = get_html(url)
    herolist = get_herolist(url)
    get_img(herolist)


main()
