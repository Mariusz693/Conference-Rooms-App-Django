# Conference-Rooms-App-Django

Web application for booking conference rooms with user authorization and an administration panel.


### Main functionalities for Users:
- View all rooms, search by capacity or projector
- Create a profile and confirm by e-mail, update, change password, delete account
- Book a room and confirm by e-mail or cancel, check current and previous reservations
- Send a contact form

|![Conference-Rooms-App](../main/screenshots/user_01.png) |![Conference-Rooms-App](../main/screenshots/user_02.png) |
|---------------------------------------------------------|---------------------------------------------------------|
|![Conference-Rooms-App](../main/screenshots/user_03.png) |![Conference-Rooms-App](../main/screenshots/user_04.png) |
|![Conference-Rooms-App](../main/screenshots/user_05.png) |![Conference-Rooms-App](../main/screenshots/user_06.png) |
|![Conference-Rooms-App](../main/screenshots/user_07.png) |![Conference-Rooms-App](../main/screenshots/user_08.png) |
|![Conference-Rooms-App](../main/screenshots/user_09.png) |![Conference-Rooms-App](../main/screenshots/user_10.png) |


### Main functionalities for Admins:
- Update admin profile, change password
- Create a room profile, update or delete
- View all rooms and check reservations
- Send a link to the user to confirm the reservation

|![Conference-Rooms-App](../main/screenshots/admin_01.png)|![Conference-Rooms-App](../main/screenshots/admin_02.png)|
|---------------------------------------------------------|---------------------------------------------------------|
|![Conference-Rooms-App](../main/screenshots/admin_03.png)|![Conference-Rooms-App](../main/screenshots/admin_04.png)|
|![Conference-Rooms-App](../main/screenshots/admin_05.png)|![Conference-Rooms-App](../main/screenshots/admin_06.png)|
|![Conference-Rooms-App](../main/screenshots/admin_07.png)|![Conference-Rooms-App](../main/screenshots/admin_08.png)|


### Technologies:
* Django
* Bootstrap
* Crispy-bootstrap

### Installation:
* Creating a virtual environment `virtualenv -p python3 env`
* Activation of the virtual environment `source env/bin/activate`
* Installation of necessary libraries `pip3 install -r requirements.txt`
* Creating a project `django-admin startproject conference_rooms_project`
* Creating applications `python3 manage.py startapp conference_rooms_app`
* Creating migration `python3 manage.py makemigrations`
* Migration upgrade `python3 manage.py migrate`
* Launching the application `python3 manage.py runserver`
* Open the application `http://localhost:8000/conference_rooms/home_page/`

### Contact
* [LinkedIn](https://www.linkedin.com/in/mariusz-kuleta/)