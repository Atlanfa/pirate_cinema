import requests
from utils import get_film_id
from bs4 import BeautifulSoup


def get_link_from_response(response):
    dictionary = response.json()
    if 'url' in dictionary:
        urls = dictionary['url']
        urls_divided = urls.split(',')
        full_hd = urls_divided[3].split('or')[-1].strip()
    else:
        full_hd = "no link"
    return full_hd


def get_translator_id(film_link):
    main = requests.get(film_link)
    soup = BeautifulSoup(main.text, 'html.parser')
    script = soup.findAll('script')[-3]
    script_str = str(script.string)
    script_split = script_str.split(',')
    translator_id = script_split[1]
    return translator_id


def get_trailer(film_link):
    cookies = {
        'dle_user_taken': '1',
        'dle_user_token': '69a78bc31834ab709cb9122cd898fbc6',
        'PHPSESSID': 'dl6q6r8956nvcnc5baqf7i6hr5',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'rezka.ag',
        'Origin': 'https://rezka.ag',
        'Referer': f'{film_link}',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    }

    data = {
        'id': f'{get_film_id(film_link)}'
    }

    response = requests.post('https://rezka.ag/engine/ajax/gettrailervideo.php', headers=headers, cookies=cookies,
                             data=data)
    dictionary = response.json()
    if 'code' in dictionary:
        link_start = dictionary['code'].find('https')
        link_end = dictionary['code'].find('"', link_start)
        link = dictionary['code'][link_start:link_end]
        if "hdrezka" in link:
            main = requests.get(link)
            soup = BeautifulSoup(main.text, 'html.parser')
            script = soup.findAll('script')[-1]
            links_str = str(script.string).strip()
            links = links_str.split(',')
            link = links[2].strip().strip("'")
    else:
        link = "no link"
    return link


def get_film(film_link):
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Opera/9.80 (Windows NT 6.0; MRA 6.0 (build 5831)) Presto/2.12.388 Version/12.17',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'rezka.ag',
        'Connection': 'close',
        'Content-Length': '41',
    }

    data = {
        'id': f'{get_film_id(film_link)}',
        'translator_id': f'{get_translator_id(film_link)}',
        'action': 'get_movie'
    }

    response = requests.post('https://rezka.ag/ajax/get_cdn_series/', headers=headers, data=data, verify=False)

    full_hd = get_link_from_response(response)
    return full_hd


def get_series(film_link, episode, season):
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Opera/9.80 (Windows NT 6.0; MRA 6.0 (build 5831)) Presto/2.12.388 Version/12.17',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'rezka.ag',
        'Connection': 'close',
        'Content-Length': '63',
    }

    data = {
        'id': f'{get_film_id(film_link)}',
        'translator_id': f'{get_translator_id(film_link)}',
        'episode': f'{episode}',
        'season': f'{season}',
        'action': 'get_stream'
    }

    response = requests.post('https://rezka.ag/ajax/get_cdn_series/', headers=headers, data=data, verify=False)

    full_hd = get_link_from_response(response)

    return full_hd


def get_episode_list(film_link):
    import requests

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Opera/9.80 (Windows NT 6.0; MRA 6.0 (build 5831)) Presto/2.12.388 Version/12.17',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'rezka.ag',
        'Connection': 'close',
        'Content-Length': '46',
    }

    data = {
        'id': f'{get_film_id(film_link)}',
        'translator_id': f'{get_translator_id(film_link)}',
        'action': 'get_episodes'
    }

    response = requests.post('https://rezka.ag/ajax/get_cdn_series/', headers=headers, data=data, verify=False)
    dictionary = response.json()
    if 'seasons' in dictionary:
        seasons_count = dictionary['seasons'].count("Сезон")
        episodes_divided = dictionary['episodes'].split('simple-episodes-list')
        episodes_divided.pop(0)
        episodes_count = []
        for index in range(seasons_count):
            episodes_count.append(episodes_divided[index].count('Серия'))
    else:
        seasons_count = "no link"
        episodes_count = seasons_count
    return seasons_count, episodes_count

# print(get_film('https://rezka.ag/films/drama/36744-schastlivo-ostavatsya-2020.html'))
# print(get_series('https://rezka.ag/animation/adventures/37169-ataka-titanov-vybor-bez-sozhaleniy-ova-2-2014.html',
# 2, 1))
# print(get_episode_list('https://rezka.ag/series/drama/37730-starec-2019.html'))
# print(get_episode_list('https://rezka.ag/films/drama/36744-schastlivo-ostavatsya-2020.html'))
# print(get_trailer('https://rezka.ag/films/drama/806-pobeg-iz-shoushenka-1994.html'))
# print(get_trailer('https://rezka.ag/films/documentary/22652-cvet-nacii-2013.html'))
# print(get_trailer('https://rezka.ag/cartoons/comedy/14100-zhil-byl-pes.html'))
# print(get_episode_list('https://rezka.ag/series/action/37957-kung-fu-2021.html'))
# print(get_film('https://rezka.ag/films/drama/37977-kislorod-2021.html'))
