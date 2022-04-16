import requests
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import asyncio
import httpx
import datetime
from seleniumwire import webdriver

full_olympiads_list = []
RU_MONTH_VALUES = {
    'янв': 1,
    'фев': 2,
    'мар': 3,
    'апр': 4,
    'мая': 5,
    'июн': 6,
    'июл': 7,
    'авг': 8,
    'сен': 9,
    'окт': 10,
    'ноя': 11,
    'дек': 12,
}


def interceptor(request):
    ua = UserAgent()
    del request.headers['user-agent']
    # request.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,'\
    #                             'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    request.headers['user-agent'] = ua.random


def main_olimpiada_ru(region_number=78):
    ua = UserAgent()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua.random
    }

    cookies = {
        'region': f'{region_number}'
    }

    EXE_PATH = r'C:\Program Files\Google\Chrome\Application\chromedriver\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=EXE_PATH)

    driver.get('https://olimpiada.ru/activities')
    # Добавление куки для определения региона: 78 - Санкт-Петербург
    for key, value in cookies.items():
        driver.add_cookie({'name': key, 'value': value})

    # Добавление headers
    driver.request_interceptor = interceptor

    driver.get('https://olimpiada.ru/activities')
    for request in driver.requests:
        print(request.headers)
    total_height = 100000
    for i in range(1, total_height, 15):
        driver.execute_script("window.scrollTo(0, {});".format(i))

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    olympiads = soup.find('div', id='megalist').find_all('div', class_='olimpiada')
    olympiads_list = []
    for i, olympiad in enumerate(olympiads):
        try:

            title = olympiad.find('span', class_='headline').text
            last_s = olympiad.find('span', class_='headline red').text
            school_classes = olympiad.find('span', class_='classes_dop').text.split()[0].split('–')
            separate_page = olympiad.find('a', class_='none_a black')['href']
            separate_page_dict, subjects = parse_separate_page(separate_page)
            # description = olympiad.find('a', class_='olimp_desc').text
            # print(i, {'title': title, 'last': last_s, 'subjects': subjects, 'school_class': school_class,
            #           'separate_page': separate_page,
            #           'description': None})

            olympiads_list.append(
                {'title': title, 'school_class': list(map(int, school_classes)), 'subject': subjects,
                 **separate_page_dict}
            )
        except Exception as E:
            print("ОШИБКА ", E)
    return olympiads_list


def parse_stage(stages):
    stages_lst = []
    for stage in stages:
        td_stages = stage.find_all('td')
        date = ' '.join(td_stages[1].text.split()).split('...')
        if len(date) == 2:
            date = date[1].split()
        else:
            date = date[0].split()
        date = datetime.datetime.strptime(f'{date[0]}.{RU_MONTH_VALUES[date[1]]}.2022', "%d.%m.%Y")

        stages_lst.append({
            'name': td_stages[0].text,
            'date': [date]
        })
    return stages_lst


def parse_separate_page(link, region_number=78):
    ua = UserAgent()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': ua.random
    }

    cookies = {
        'region': f'{region_number}'
    }
    response = requests.get(f'https://olimpiada.ru{link}', headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    stages = soup.find('table', class_='events_for_activity')
    stages_active_lst = []
    stages_past_lst = []

    if stages:
        stages_active = soup.find('table', class_='events_for_activity').find_all('tr', class_='notgreyclass')
        stages_past = soup.find('table', class_='events_for_activity').find_all('tr', class_='gray')

        if stages_active:
            stages_active_lst.extend(parse_stage(stages_active))
        else:
            stages_active_lst.append({
                'name': 'Точные даты неизвестны',
                'date': [datetime.datetime.now()]
            })
        if stages_past:
            stages_past_lst.extend(parse_stage(stages_active))
    else:
        stages_active_lst.append({
            'name': 'Точные даты неизвестны',
            'date': [datetime.datetime.now()]
        })

    contact_link = soup.find_all('div', class_='contacts')[-1]
    link = contact_link.find('a', {'target': '_blank'})['href']
    history = soup.find('div', id='history')
    subjects_tags = soup.find('div', class_='subject_tags_full')
    subjects = [' '.join(subject.text.split()) for subject in subjects_tags][1:]

    if history:
        history = '\n'.join(list(map(lambda x: x.text, soup.find('div', id='history').find_all('p'))))

    stages_active_lst.sort(key=lambda x: x['date'][0])
    return {'links': {'Сайт': link}, 'stages': list(reversed(stages_active_lst)), 'history': history}, subjects


if __name__ == '__main__':
    main_olimpiada_ru(78)
