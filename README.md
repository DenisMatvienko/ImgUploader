<h2 align="center">ImgUploader</h2>

Сервис для загрузки изображений. 
Загрузка изображения происходит по ссылке или выбрав файл с компьютера. Выбранное изображение можно редактировать
изеняя ширину и высоту, можно задать только ширину или только высоту, пропорции сохраняются. Использование для одного из 
значений = 0, не сохраняет пропорции изображения и автоматически задаст свой параметр. Поля ШхВ - обязательные 
для ввода. При создании сервиса не было условия, для размеров изображения и при задании даже самых маленьких размеров:
"1х1", а так же больших размеров - будем считать сохранением условий необходимого размера изображений.

#### Install/Установка

##### Работа с репозитоием:
Инициализироать репозиторий:

```
 git init
```

##### Virtual env. activate/Активация виртуального окружения #####
Windows:
```
 path\to\env\Scripts\activate
```

Linux:
```
source env/bin/activate
```

Клонируем репозиторий:
```
 git clone https://github.com/DenisMatvienko/ImgUploader
```

##### Requirements install/Установка библиотек #####
Windows:
```
pip3 install -r requirements.txt
```

Linux:
```
cd 'Project_name'
pip install virtualenvwrapper
mkvirtualenv "name_your_project"
cat requirements.txt
pip3 install -r requirements.txt
```
##### Data base/База данных #####

Для работы с новой базой данных необходимо произвести миграции в терминале.

```
 py manage.py makemigrations
```

```
 py manage.py migrate
```

##### Data base/Application use #####

В терминале необходимо запустить локальный сервер.

```
 py manage.py runserver
```

#

### Consultancy/Консультирование ###
По вопрсам и рекомендациям, относительно сервиса обращаться на почту *grabsomebuds27@gmail.com*.
