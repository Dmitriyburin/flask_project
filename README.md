# Олимпиадник - сайт

## Тема и описание проекта
"Олимпиадник" позволит удобно и быстро находить нужные олимпиады. Будет возможность администрирования олимпиад (добавление, изменение, удаление). Также будет реализовано автоматическое добавление олимпиад с интеренет-ресурсов.
## Цели проекта:
- Расширить знания Flask, верстки
- Научиться писать парсеры и применить их в своем сайте
- Реализовать удобную панель администратора 
- Написать полноценный рабочий сайт и задеплоить его

## Запуск сайта ##
1. На мой сайт можно попасть по ссылке - 

## Реализация ##

Код состоит из классов и функций, выполняющих всю работу

_**Классы**_:
- Модели таблиц:
> Olympiads(SqlAlchemyBase, SerializerMixin)<br>
> SchoolClasses(SqlAlchemyBase)<br>
> Stages(SqlAlchemyBase)<br>
> Subjects(SqlAlchemyBase)<br>
- REST-API:
> OlympiadsResource(Resource)<br>
> OlympiadsListResource(Resource)<br>
> UsersResource(Resource)<br>
> UsersListResource(Resource)<br>


_**Основные Функции**_:
- Будут добавляться в процессе разработки

_**Библиотеки/Технологии**_:
- Flask
- MySQL
- SCSS/SASS

