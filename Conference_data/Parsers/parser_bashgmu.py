import time
from datetime import date
from bs4 import BeautifulSoup
import json
import hashlib
from .find_dates_in_string import find_date_in_string, normalise_str
from datetime import datetime
import requests
from urllib3 import exceptions


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/109.0.0.0 Safari/537.36'
}

result = []
confer = []

def parser_bashgmu_pages(un_id, url, date_):
    try:
        session = requests.session()
        try:
            resp = session.get(url=url, headers=headers, timeout=20)
            if resp.status_code == 404:
                print(f'{resp.status_code} - Нет такой страницы {url}')
                return

            soup = BeautifulSoup(resp.text, 'lxml')
            if soup.find('div', class_='grants-list'):
                main_containers = soup.find('div', class_='grants-list')
                # print(main_containers)
                confs = main_containers.find_all('p', class_='grants-item')
                # print(confs)
                for conf in confs:
                    conf_name = normalise_str(conf.find('a').get_text(separator=' '))
                    if 'конфер' in conf_name.lower():
                        confer.append(
                            [
                                {
                                    'title': conf_name,
                                    'url': f"https://bashgmu.ru{conf.find('a').get('href')}"
                                }
                            ]
                        )
                # print(confer)

            for conf in confer:
                # print(conf[0])
                get_bashgmu_page_data(session, un_id, conf[0], date_)

        except Exception as e:
            print(f'Ошибка загрузки данных для {url}')

    except Exception as e:
        raise Exception(f'Не удалось открыть сессию для {__name__}\n{e}')

def get_bashgmu_page_data(session, un_id, conf, filter_date):
    try:
        resp = session.get(url=conf["url"], headers=headers, timeout=20)
        if resp.status_code == 404:
            print(f'{resp.status_code} - Нет такой страницы {conf["url"]}')
            return
        print(f'{resp.status_code} - Обработка конференции {conf["url"]}')

        soup = BeautifulSoup(resp.text, 'lxml')

        main_containers = soup.find('div', class_='grants-detail')
        # print(main_containers)

        un_name = 'Башкирский государственный медицинский университет'
        conf_name = conf['title']
        conf_s_desc = conf_name
        local = False if 'международн' in conf_name.lower() else True

        conf_id = f"{un_id}_{conf['url'].split('/')[-2]}"
        hash_ = str(hashlib.md5(bytes(conf_id, 'utf-8')).hexdigest())
        conf_card_href = conf['url']

        conf_date_begin = ''
        conf_date_end = ''

        conf_address = ''

        reg_date_begin = ''
        reg_date_end = ''
        reg_href = ''
        conf_desc = ''
        org_name = ''
        themes = ''

        online = True if 'онлайн' in conf_name.lower() or 'он-лайн' in conf_name.lower() else False
        offline = True

        conf_href = ''
        contacts = ''
        rinc = False

        lines = main_containers.find_all(['h3', 'p'])

        for line in lines:

            conf_desc = conf_desc + ' ' + normalise_str(line.get_text(separator=" "))

            if ('состоится' in line.text.lower() or 'открытие' in line.text.lower()
                or 'проведен' in line.text.lower()) and conf_date_begin == '':
                conf_date_begin = str(list(find_date_in_string(line.text.lower()))[0].date()) if \
                    list(find_date_in_string(line.text.lower())) else ''
                conf_date_end = str(list(find_date_in_string(line.text.lower()))[1].date()) if \
                    len(list(find_date_in_string(line.text.lower()))) > 1 else ''

            if ('заявк' in line.text.lower() or 'принимаютс' in line.text.lower() or 'регистрац' in line.text.lower() or
                'регистрир' in line.text.lower()) and reg_date_begin == '':
                reg_date_begin = str(list(find_date_in_string(line.text.lower()))[0].date()) if \
                    list(find_date_in_string(line.text.lower())) else ''
                reg_date_end = str(list(find_date_in_string(line.text.lower()))[1].date()) if \
                    len(list(find_date_in_string(line.text.lower()))) > 1 else ''

            if reg_href == '' and ('регистрац' in line.text.lower() or 'зарегистр' in line.text.lower()
                                   or 'участия' in line.text.lower() or 'заявк' in line.text.lower()):
                reg_href = line.find('a').get('href') if line.find('a') \
                                                         and ('http:' in line.find('a').get('href') or
                                                              'https:' in line.find('a').get('href')) and \
                                                         ('.pdf' not in line.find('a').get('href') or
                                                          '.doc' not in line.find('a').get('href') or
                                                          '.xls' not in line.find('a').get('href')) else 'отсутствует'

            if org_name == '' and 'организатор' in line.text.lower():
                org_name = normalise_str(line.get_text(separator=" "))

            if online and ('онлайн' in line.text.lower() or 'трансляц' in line.text.lower()):
                conf_href = line.find('a').get('href') if line.find('a') else 'отсутствует'

            if offline and ('место' in line.text.lower() or 'адрес' in line.text.lower()):
                offline = True
                conf_address = normalise_str(line.get_text(separator=" "))

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
                 'conf_s_desc': conf_s_desc.strip(),
                 'conf_desc': conf_desc.strip(),
                 'org_name': org_name,
                 'themes': themes.strip(),
                 'online': online,
                 'conf_href': conf_href,
                 'offline': offline,
                 'conf_address': conf_address.strip(),
                 'contacts': contacts.strip(),
                 'rinc': rinc,
                 }
            )
    except Exception as e:
        print(f'Ошибка загрузки данных для {conf["url"]}.\n{e}')


def parser_bashgmu(un_id, url, date_):
    try:
        parser_bashgmu_pages(un_id, url, date_)
        with open(f'Conference_data/Parsers/JSON_log/{un_id}_{date.today()}.json', 'w', encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
        return result
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(parser_bashgmu('bashgmu', 'https://bashgmu.ru/science_and_innovation/konferentsii/',
                       datetime.strptime('2023.01.01', '%Y.%m.%d')))
