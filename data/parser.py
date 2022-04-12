import requests
import re
from bs4 import BeautifulSoup
import asyncio
import httpx
import datetime

full_olympiads_list = []


async def pars_olymps(page_link, olympiads_list):
    global full_olympiads_list
    async with httpx.AsyncClient() as client:
        page = await client.get(page_link)
        soup = BeautifulSoup(page.text, 'html.parser')
        table_olympiads = soup.find('table', class_='activities_table').tbody
        olympiads = table_olympiads.find_all('a', class_='black_hover_blue')
        subjects = table_olympiads.find_all('span', class_='light_grey')
        for i, olymp in enumerate(olympiads):

            separate_number_page = olymp['href'].split('/')[2]
            separate_page_dict = await parse_separate_page(separate_number_page, client)
            olymp_info = subjects[i].text.split(' |')
            school_classes = olymp_info[0].split('-')
            if school_classes[0].count(','):
                school_classes = school_classes[0].split(',')
            subjects_for_olymp = [olymp_info[1].strip()]
            if subjects_for_olymp[0].count('предметов'):
                subjects_for_olymp = re.sub(r'([А-Я][a-я][a-я])', r' \1',
                                            subjects_for_olymp[0]).replace('язык', '').split()[2:]
            if len(olymp.text) > 140:
                olymp.text = olymp.text[:140]
            olympiads_list.append(
                {'title': olymp.text, 'school_class': list(map(int, school_classes)), 'subject': subjects_for_olymp,
                 **separate_page_dict}
            )
            print(len(olympiads_list),
                  {'title': olymp.text, 'school_class': list(map(int, school_classes)), 'subject': subjects_for_olymp,
                   **separate_page_dict})
        full_olympiads_list.extend(olympiads)
        return olympiads_list


async def parse_separate_page(number_olymp, client):
    async with httpx.AsyncClient() as client:
        page = await client.get(f'https://info.olimpiada.ru/activity/{number_olymp}')
        if page.status_code == 200:
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

            stages = await parse_stages(f'https://info.olimpiada.ru/activity/{number_olymp}/events', client)
            history = await parse_history(f'https://info.olimpiada.ru/activity/{number_olymp}/history', client)
            return {'links': links, 'stages': stages, 'history': history}
        return {}
    # official_site_link = links[0]
    # email_link = links[1]
    # founders_links = links[2:]
    # return {'links': [{'official_site_link': official_site_link,
    #                    'email_link': email_link, 'founders_links': founders_links}]}


async def parse_stages(link, client):
    async with httpx.AsyncClient() as client:
        page = await client.get(link)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')
            stages_a = soup.find('div', id='archive_events')
            stages = []
            try:
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
            except (TypeError, ValueError):
                return stages
            return stages


async def parse_history(link, client):
    try:
        page = await client.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')
        text = '\n'.join(map(lambda x: x.text, soup.find('div', class_='main').find_all('p')))
    except (TypeError, ValueError, AttributeError):
        return ''
    return text


async def main():
    global full_olympiads_list
    queue = asyncio.Queue()
    task_list = []
    for i in range(1, 5):
        task = asyncio.create_task(
            pars_olymps(f'https://info.olimpiada.ru/activities/single/random/page/{i}', full_olympiads_list))
        task_list.append(task)

    await queue.join()
    await asyncio.gather(*task_list, return_exceptions=True)
    return full_olympiads_list


def lol_parse():
    response = requests.get(f'https://www.ucheba.ru/for-abiturients/olympiads/spb')
    soup = BeautifulSoup(response.text, 'html.parser')
    olymps = soup.find_all('div', class_='olympiads__content')
    for olymp in olymps:
        title = olymp.find('h2', class_='olympiads__title').text.strip()
        school_class = olymp.find('div', class_='class__value').text.strip()
        print(title, school_class)


if __name__ == '__main__':
    asyncio.run(main())
