from datetime import date
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
from datetime import datetime


result = []
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/109.0.0.0 Safari/537.36'
}


async def make_queue_mgsu(un_id, url, filter_date):
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            try:
                async with session.get(url=url, headers=headers, timeout=20) as response:
                    if response.status == 404:
                        print(f'{response.status} - Нет такой страницы {url}')
                        return
                    response_text = await response.text()
                    soup = BeautifulSoup(response_text, 'lxml')
                    main_container = soup.find('div', id='inner-content', class_='container').find('div', id='news-container')

                    pages = int(main_container.find('ul', class_='pagination').find_all('li')[-2].text) \
                        if main_container.find('ul', class_='pagination') else 1

                    # pages = 1
                    for page in range(1, pages+1):
                        url_ = f'{url}?PAGEN_1={page}' if page > 1 else url
                        try:
                            async with session.get(url=url_, headers=headers, timeout=20) as response:
                                if response.status == 404:
                                    print(f'{response.status} - Нет такой страницы {url}')
                                    continue
                                response_text = await response.text()
                                print(f'{response.status} Обрабатываем страницу {page} из {pages}, {url_}')
                                soup = BeautifulSoup(response_text, 'lxml')
                                conf_block = soup.find('div', id='inner-content', class_='container').\
                                    find('div', id='news-container').find_all('section', class_='news-list-item')

                                for n, conf in enumerate(conf_block):
                                    title = conf.find('div', class_='news-title').find('a').text.strip()
                                    if 'конфер' in title:
                                        conf_url = f"https://mgsu.ru{conf.find('div', class_='news-title').find('a').get('href').strip()}"
                                        task = asyncio.create_task(parser_mgsu_pages(session, un_id, conf_url, filter_date, n, page))
                                        tasks.append(task)
                                    # break
                        except Exception as e:
                            raise Exception(f'Не удалось обработать ссылку {n} на странице {page} в {__name__} для {url_}\n{e}')

                    await asyncio.gather(*tasks)
            except Exception as e:
                raise Exception(f'Не удалось получить данные в {__name__} для {url}\n{e}')
    except Exception as e:
        raise Exception(f'Не удалось обработать очередь для {__name__}\n{e}')



async def parser_mgsu_pages(session, un_id, url, filter_date, n, page):
    try:
        async with session.get(url=url, headers=headers, timeout=20) as response:
            if response.status == 404:
                print(f'{response.status} - Нет такой страницы {url}')
                return
            print(f'{response.status} Выполняется ссылка {n + 1} на странице {page}, {url}')
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'lxml')
            conf_block = soup.find('div', id='inner-content')
            un_name = soup.find('div', id='inner-header').find('img').get('alt').strip()

            conf_name = normalise_str(conf_block.find('div', class_='news-title').text)
            local = False if 'международн' in conf_name.lower() else True

            conf_id = f"{un_id}_{url.split('/')[-2]}"
            hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
            conf_card_href = url

            lines = conf_block.find('div', class_='news-text').find_all(['div', 'p', 'li'])

            conf_s_desc = ''
            reg_date_begin = ''
            reg_date_end = ''
            conf_date_begin = ''
            conf_date_end = ''
            reg_href = ''
            conf_desc = ''
            org_name = ''
            themes = ''
            online = False
            conf_href = ''
            offline = False
            conf_address = ''
            contacts = ''
            rinc = False

            for line in list(lines):
                # print(line.text)
                if conf_s_desc == '':
                    conf_s_desc = normalise_str(line.text)

                if ('заявк' in line.text.lower() or 'принимаютс' in line.text.lower() or 'участи' in line.text.lower()
                            or 'регистрац' in line.text.lower() or 'регистрир' in line.text.lower()) and reg_date_begin == '':
                    reg_date_begin = str(list(find_date_in_string(line.text.lower()))[0].date()) if \
                        list(find_date_in_string(line.text.lower())) else ''
                    reg_date_end = str(list(find_date_in_string(line.text.lower()))[1].date()) if \
                        len(list(find_date_in_string(line.text.lower()))) > 1 else ''

                if ('состоится' in line.text.lower() or 'открытие' in line.text.lower()
                    or 'проведен' in line.text.lower()) and conf_date_begin == '':
                    conf_date_begin = str(list(find_date_in_string(line.text.lower()))[0].date()) if \
                        list(find_date_in_string(line.text.lower())) else ''
                    conf_date_end = str(list(find_date_in_string(line.text.lower()))[1].date()) if \
                        len(list(find_date_in_string(line.text.lower()))) > 1 else ''

                if not online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower()):
                    online = True
                    conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'
                if not offline and ('место' in line.text.lower() or 'адрес' in line.text.lower()):
                    offline = True
                    conf_address = normalise_str(line.get_text(separator=" "))

                conf_desc = conf_desc + ' ' + normalise_str(line.get_text(separator=" "))

                if reg_href == '' and ('регистрац' in line.text.lower() or 'зарегистр' in line.text.lower()
                                       or 'участия' in line.text.lower() or 'заявк' in line.text.lower()):
                    reg_href = line.find('a').get('href') if line.find('a') \
                                                             and ('http:' in line.find('a').get('href') or
                                                                  'https:' in line.find('a').get('href')) and\
                                                             ('.pdf' not in line.find('a').get('href') or
                                                              '.doc' not in line.find('a').get('href') or
                                                              '.xls' not in line.find('a').get('href')) else 'отсутствует'

                if org_name == '' and 'организатор' in line.text.lower():
                    org_name = normalise_str(line.get_text(separator=" "))

                if not online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower() or
                                   'ссылка' in line.text.lower()):
                    conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'
                    online = True

                if not offline and ('место' in line.text.lower() or 'адрес' in line.text.lower() or
                                    'очно' in line.text.lower()):
                    conf_address = normalise_str(line.text)
                    offline = True

                if ('тел.' in line.text.lower() or 'контакт' in line.text.lower() or 'mail' in line.text.lower()
                        or 'почта' in line.text.lower() or 'почты' in line.text.lower()):
                    contacts = contacts + ' ' + normalise_str(line.text)

                if line.find('a') and 'mailto' in line.find('a').get('href'):
                    contacts = contacts + ' ' + normalise_str(line.find('a').text)

                if not rinc:
                    rinc = True if 'ринц' in line.text.lower() else False

            if (conf_date_begin != '' and datetime.strptime(conf_date_begin,
                                                            '%Y-%m-%d') >= filter_date) or conf_date_begin == '':
                result.append(
                        {'conf_id': conf_id,
                         'hash': hash_,
                         'un_name': un_name,
                         'local': local,
                         'reg_date_begin': reg_date_begin,
                         'reg_date_end': reg_date_end,
                         'conf_date_begin': conf_date_begin,
                         'conf_date_end': conf_date_end,
                         'conf_card_href': conf_card_href,
                         'reg_href': reg_href,
                         'conf_name': conf_name,
                         'conf_s_desc': conf_s_desc,
                         'conf_desc': conf_desc,
                         'org_name': org_name,
                         'themes': themes,
                         'online': online,
                         'conf_href': conf_href,
                         'offline': offline,
                         'conf_address': conf_address,
                         'contacts': contacts.strip(),
                         'rinc': rinc,
                         }
                    )
    except asyncio.TimeoutError as e:
        print(f'Отказ по таймауту, ссылка {n + 1} на странице {page}, {url}', e)


def parser_mgsu(un_id, url, date_):
    try:
        asyncio.run(make_queue_mgsu(un_id, url, date_))
        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_mgsu('mgsu', 'https://mgsu.ru/news/announce/', datetime.strptime('2023.01.01', '%Y.%m.%d')))
