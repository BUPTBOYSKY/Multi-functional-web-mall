# Multi-functional-web-mall

In order to show the personal information and and product, we design a web mall, the  website can be concluded to three part: Front end website, Backend database and the connection between them.

## Overview

1. In the front website, we use html, css and javascrip to design a user friendly website, which can display personalized information. 
2. And for the Data Management & connection, Under the Django structure, we can use Django admin to manage front-end web pages, and with the help of URL configuration, the website can synchronize updates.Therefore, when I change the items stored in the cloud database, the webpage will also change accordingly.
2. And in the backend, we use Django's ORM for database design and operations, the back-end structure show here. More over, we use SQLite to simplify the development and testing process. The below picture shows our cloud database.

## Requirements

+ Python 3.0+
+ Html5
+ JavaScript
+ Django 5.0+

## Usage

Download all file, and then open Integrated Terminal，load it into the folder of 'Multi functional web all main' that you downloaded, and then enter the command:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
After running the server, you can open the webpage with a browser http://127.0.0.1:8000/mixiaozi/ To view the website, or use http://127.0.0.1:8000/admin/ To manage the database.
The account that sign in the admin: 
```bash
Username: testuser
Password: 123456
```

## Conclusion

The Mi Xiaozi Mall project is a user-friendly e-commerce platform built with Django, featuring categories like electronics, clothing, and supermarket items. It offers secure cart management, real-time updates, face recognition login, and a responsive design. Key features include dynamic navigation, a background toggle, and AJAX for seamless user interactions, creating an efficient and engaging online shopping experience.
