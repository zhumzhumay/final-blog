# final-blog
PYTHON. DJANGO. Проект Блог по типу социальных сетей.\
Сайт реализован в качестве дипломного проекта с выполнением следующих требований (наличием элементов):\
    1.Личный кабинет (CRUD без create, уже есть регистрация и аутент.) - 25\
    2.Функционал CRUD (В зависимости от проекта) - 25\
    3.Регистрация и аутентификация - 10\
    4.Создание БД (Не менее 5 таблиц, с foreign key не менее 2х) - 10\
    5.Функционал поиска - 10\
    6.Функционал сортировки - 10\
    7.Использование сторонних API - 5\
    8.Работа с местоположением клиентов - 5
    
В итоге в нем реализованы следующие возможности: просмотр постов на главной странице и  личной странице любого пользователя, а также комментариев к ним; публикация постов, \
проставление лайков, комментирование; сортирова постов и поиск по ним; создание, редактирование и удаление профиля; регистрация и аутентификация; поиск информации через апи википедии;\
получение геолокации пользователя.\
Выполнен на основе раннее созданного новостного блога https://github.com/zhumzhumay/newspaper \
p.s. Для работы с геолокацией нужно загрузить бд geoip в соответствующую папку в корне проекта и подставить переменную ip в соответствующую строку кода (вью профиля)
