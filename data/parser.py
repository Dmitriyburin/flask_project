import requests
import re
from bs4 import BeautifulSoup
from pprint import pprint
import datetime


def pars_olymps(page):
    soup = BeautifulSoup(page.text, 'html.parser')
    table_olympiads = soup.find('table', class_='activities_table').tbody
    olympiads_list = []
    olympiads = table_olympiads.find_all('a', class_='black_hover_blue')
    subjects = table_olympiads.find_all('span', class_='light_grey')
    for i, olymp in enumerate(olympiads):
        if i == 2:
            break
        separate_number_page = olymp['href'].split('/')[2]
        separate_page_dict = parse_separate_page(separate_number_page)
        olymp_info = subjects[i].text.split(' |')
        school_classes = olymp_info[0].split('-')
        if school_classes[0].count(','):
            school_classes = school_classes[0].split(',')
        subjects_for_olymp = [olymp_info[1].strip()]
        if subjects_for_olymp[0].count('предметов'):
            subjects_for_olymp = re.sub(r'([А-Я][a-я][a-я])', r' \1',
                                        subjects_for_olymp[0]).replace('язык', '').split()[2:]

        olympiads_list.append(
            {'title': olymp.text, 'school_class': list(map(int, school_classes)), 'subject': subjects_for_olymp,
             **separate_page_dict}
        )
        print(olympiads_list)
    return olympiads_list


def parse_separate_page(number_olymp):
    page = requests.get(f'https://info.olimpiada.ru/activity/{number_olymp}')
    soup = BeautifulSoup(page.text, 'html.parser')
    table_olympiad = soup.find('table', class_='act_info_table')
    links_with_title = table_olympiad.find_all('tr')[1:]
    links = {}
    for tr in links_with_title:
        try:
            title = tr.find('td', class_='first').text
            link = tr.find('td', class_='second').a['href']
            links[title] = link
        except TypeError:
            continue

    stages = parse_stages(f'https://info.olimpiada.ru/activity/{number_olymp}/events')

    return {'links': links, 'stages': stages}
    # official_site_link = links[0]
    # email_link = links[1]
    # founders_links = links[2:]
    # return {'links': [{'official_site_link': official_site_link,
    #                    'email_link': email_link, 'founders_links': founders_links}]}


def parse_stages(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    stages_a = soup.find('div', id='archive_events')
    stages = []
    for i, a in enumerate(stages_a):
        description = a.find_all('td')[1].contents[1].text.strip()
        dates = a.find('font').text.split(' - ')
        if description.startswith('-'):
            description = description[2:]
        dates = [datetime.datetime.strptime(date, "%d.%m.%Y") for date in dates]
        stages.append({
            'date': dates,
            'name': description
        })
    return stages


def full_pars_olymp():
    full_olympiads_list = []
    for i in range(1, 2):
        page = requests.get(f'https://info.olimpiada.ru/activities/single/page/{i}')
        full_olympiads_list.extend(pars_olymps(page))
    return full_olympiads_list


if __name__ == '__main__':
    pprint(full_pars_olymp())
