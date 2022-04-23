import asyncio
from pprint import pprint
from .parser_olimpiada_ru import main_olimpiada_ru
from .parser_info_olimpiada import main_info_olimpiada_ru


def main():
    full_olympiads_list = []
    full_olympiads_list.extend(main_olimpiada_ru())
    return full_olympiads_list

if __name__ == '__main__':
    pprint(main())
