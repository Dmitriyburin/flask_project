import requests
import re
from bs4 import BeautifulSoup
from pprint import pprint


def pars_olymps(page):
    soup = BeautifulSoup(page.text, 'html.parser')
    table_olympiads = soup.find('table', class_='activities_table').tbody
    olympiads_list = []
    olympiads = table_olympiads.find_all('a', class_='black_hover_blue')
    subjects = table_olympiads.find_all('span', class_='light_grey')
    for i, olymp in enumerate(olympiads):
        olymp_info = subjects[i].text.split(' |')
        school_classes = olymp_info[0].split('-')
        if school_classes[0].count(','):
            school_classes = school_classes[0].split(',')
        subjects_for_olymp = [olymp_info[1].strip()]
        if subjects_for_olymp[0].count('предметов'):
            subjects_for_olymp = re.sub(r'([А-Я][a-я][a-я])', r' \1',
                                        subjects_for_olymp[0]).replace('язык', '').split()[2:]

        olympiads_list.append(
            {'title': olymp.text, 'school_class': list(map(int, school_classes)), 'subject': subjects_for_olymp}
        )
    return olympiads_list


def full_pars_olymp():
    full_olympiads_list = []
    for i in range(1, 5):
        page = requests.get(f'https://info.olimpiada.ru/activities/single/page/{i}')
        full_olympiads_list.extend(pars_olymps(page))
    return full_olympiads_list


if __name__ == '__main__':
    pprint(full_pars_olymp())
