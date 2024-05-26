# Решение по кейсу "Клиентский портал по исследованию защищенности внешнего периметра заказчика" от [Летс Хак](https://летсхак.хакатоны.рус/)

# Юридическая часть

### Проблемы с не электронными документами

1. Возможно подделать
   - Нет способов достоверной проверки
2. Сложно автоматически проверить документы

Для процесса автоматизации процесса (с соблюдением всех необходимых законов) данный вариант не подходит

### Электронные документы

УКЭП - Укрепленная Электронная Подпись
МЧД - Машинно Читаемая Доверенность

У нас может произойти 2 варианта

1. Регистрируется руководитель (учредитель) фирмы
   - Для действий от ЮР лица необходима только УКПЭ
2. Регистрируется доверенное лицо
   - Необходима МЧД (от компании, которую представляет физ лицо)
   - УКЭП физ лица

В электронном варианте у нас есть способ удостоверения личности через Госуслуги. Пользователь авторизируется с
использованием УКЭП. Других способов подтвердить лигитимность личность человека в интернете нет.

![sad](/resources/user_types.png)

# Техническая часть

### Сервисы

##### API Госуслуг (портал ЕСИА)

- Ауентефикация человека
- Возможность запросить необходимые данные о человеке

Необходимо от пользователя:

- УКЭП для авторизации на портале Госуслуг

##### API ФНС

- Получить данные о компании

Необходимо от пользователя:

- ИНН

##### Обработка УКЭП

Два варианта

- Создать собственный вариант, выполняющий требования ГОСТ 34.10/11 2012
  - Возможно создать уязвимость в передаче данных
- Использовать готовое решение (библиотеку / сервис) - PyCades как пример
  - Поддержка от компании с гарантиями
  - Платное решение для серверных платформ

### Проблемы

- Не протестированы запросы к API Госуслуг (т.к нет доступа)
- Не протестирована работы с реальными ЭЦП
- Не доработанный фронтенд (отвественный за фронтенд не успел выложить рабочую версию)

# Как использовать наш проект

Запустить через докер

```commandline
docker-compose up --build
```

```commandline
docker-compose build --platform=linux/amd64 -t .
```

### Endpoints
