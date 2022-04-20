from collections import OrderedDict
from PyQt5.QtWidgets import QFileDialog
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtWidgets
from pathlib import Path
import threading
import requests
import time
import json
import datetime
import sys
import shutil
import dialog
import dialog2
import startwindow

MAX_USERS = 100000
MAX_POST = 100000
access_token = 'TOKEN'
version = 5.92
users_time = {}
users = []
table = {}
mass = []
cities = {}
sexs = {'male': 0, 'female': 0}
countries = {}
ages = {}
PATH = Path('data.json')
PATH.touch()
hour = datetime.datetime.now().hour


class DialogWindow2(QtWidgets.QMainWindow, dialog2.Ui_Dialog):
    table = {}
    selectedUser = ''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Online')
        self.showOnlineButton.clicked.connect(self.showOnline)
        self.listWidget.itemClicked.connect(self.selectionChanged)
        self.listWidget_2.itemClicked.connect(self.selectionChanged2)

    def selectionChanged(self, item):
        self.selectedUser = item.text()
        userDates = self.table[item.text()]
        self.listWidget_2.clear()
        for date in userDates:
            self.listWidget_2.addItem(date)

    def selectionChanged2(self, item):
        hours = []
        minutes = []
        for online in self.table[self.selectedUser][item.text()]:
            hours.append(online)
            minutes.append(self.table[self.selectedUser][item.text()][online])
        fig, ax = plt.subplots()
        ax.bar(hours, minutes)
        fig.set_figwidth(12)  # ширина Figure
        fig.set_figheight(6)
        plt.title('Статистика по онлайну')
        plt.ylabel('Кол-во минут')
        plt.xlabel('Часы')
        plt.rcParams['font.size'] = '12'
        plt.show()

    def showOnline(self):
        global table
        self.table = table
        if self.table.__len__() == 0:
            try:
                self.table = json.loads(PATH.read_text(encoding='utf-8'))
            except:
                print("error json.loads")
        self.listWidget.addItems(list(self.table.keys()))


class startwindow(QtWidgets.QMainWindow, startwindow.Ui_MainWindow):
    cities = {}
    sexs = {'male': 0, 'female': 0}
    countries = {}
    ages = {}
    size = 10

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.startButton.clicked.connect(self.start)
        self.printOnlineButton.clicked.connect(self.printOnline)
        self.printAverageOnlineButton.clicked.connect(self.printAverageOnline)
        self.checkOnlineButton.clicked.connect(self.checkOnline)
        self.saveButton.clicked.connect(self.saveFile)
        self.openButton.clicked.connect(self.getFileNames)
        self.citiesButton.clicked.connect(self.cities)
        self.agesButton.clicked.connect(self.ages)
        self.countriesButton.clicked.connect(self.countries)
        self.sexsButton.clicked.connect(self.sexs)
        self.userCheckBox.stateChanged.connect(
            lambda state=self.userCheckBox.isChecked(), checkBox=1: self.selectCheckBox(state, checkBox))
        self.groupCheckBox.stateChanged.connect(
            lambda state=self.groupCheckBox.isChecked(), checkBox=2: self.selectCheckBox(state, checkBox))

    def selectCheckBox(self, toggle, checkBox):
        if toggle == QtCore.Qt.Checked:
            if checkBox == 1:
                self.groupCheckBox.setChecked(0)
            if checkBox == 2:
                self.userCheckBox.setChecked(0)

    def start(self):
        self.loadLabel.setText('Подождите...')
        global mass
        lineEdit = self.lineEdit.text()
        if lineEdit == '':
            self.loadLabel.setText('Введите ID!')
            return
        self.status.setText("id:" + str(lineEdit))
        try:
            if self.userCheckBox.isChecked() == 1:
                userName = getUserName(lineEdit)
                self.label_2.setText("Пользователь: " + userName)
                mass = getFriends(lineEdit)
            else:
                groupName = getGroupName(lineEdit)
                self.label_2.setText("Сообщество: " + groupName)
                mass = getMembers(lineEdit)
        except:
            self.loadLabel.setText('Неверный ID!')

        users_details = get_details(mass, 'sex,bdate,city,country')
        cities, sexs, countries, ages = calculatingStats(users_details)
        self.cities = cities
        self.sexs = sexs
        self.countries = countries
        self.ages = ages
        self.loadLabel.setText('Готово!')

    def checkOnline(self):
        if mass.__len__() != 0:
            collecting_online(mass)
        else:
            self.label.setText("Не верный id")

    def printOnline(self):
        self.DialogWindow2 = DialogWindow2()
        self.DialogWindow2.show()

    def printAverageOnline(self):
        try:
            table = json.loads(PATH.read_text(encoding='utf-8'))
            sum = {}
            average = {}
            for user in table:
                for date in table[user]:
                    for hour in table[user][date]:
                        try:
                            sum[hour] += table[user][date][hour]
                        except:
                            sum[hour] = table[user][date][hour]
        except:
            print("error json.loads")
        len = table.__len__()
        for hour in sum:
            average[int(hour)] = int(sum[hour]) / len
        average = OrderedDict(sorted(average.items(), key=lambda item: item[0]))
        averageHour = []
        averageCount = []
        for x in average:
            averageHour.append(str(x))
            averageCount.append(average[x])

        fig, ax = plt.subplots()
        ax.bar(averageHour, averageCount)
        fig.set_figwidth(5)  # ширина Figure
        fig.set_figheight(6)
        plt.title('Статистика по онлайну')
        plt.ylabel('Минуты')
        plt.xlabel('Часы')
        plt.rcParams['font.size'] = '12'
        plt.show()

    def cities(self):
        size = self.size
        citiesTitle = []
        citiesCount = []
        cities = OrderedDict(sorted(self.cities.items(), key=lambda item: item[1]))
        for city in cities:
            citiesTitle.append(city)
            citiesCount.append(cities[city])
        citiesTitle.reverse()
        citiesCount.reverse()

        fig, ax = plt.subplots()
        ax.bar(citiesTitle[:size], citiesCount[:size])
        fig.set_figwidth(15)  # ширина Figure
        fig.set_figheight(6)
        plt.title('Статистика по городам')
        plt.ylabel('Кол-во человек')
        plt.xlabel('Город')
        plt.rcParams['font.size'] = '10'
        plt.show()

    def countries(self):
        size = self.size
        countriesTitle = []
        countriesCount = []
        countries = OrderedDict(sorted(self.countries.items(), key=lambda item: item[1]))
        for country in countries:
            countriesTitle.append(country)
            countriesCount.append(countries[country])
        countriesTitle.reverse()
        countriesCount.reverse()

        fig, ax = plt.subplots()
        ax.bar(countriesTitle[:size], countriesCount[:size])
        fig.set_figwidth(15)  # ширина Figure
        fig.set_figheight(6)
        plt.title('Статистика по странам')
        plt.ylabel('Кол-во человек')
        plt.xlabel('Страна')
        plt.rcParams['font.size'] = '12'
        plt.show()

    def ages(self):
        self.size = 10
        agesTitle = []
        agesCount = []
        ages = OrderedDict(sorted(self.ages.items(), key=lambda item: item[1]))
        for age in ages:
            agesTitle.append(age)
            agesCount.append(ages[age])

        fig, ax = plt.subplots()
        ax.bar(agesTitle, agesCount)
        fig.set_figwidth(10)  # ширина Figure
        fig.set_figheight(6)
        plt.title('Статистика по возрасту')
        plt.ylabel('Кол-во человек')
        plt.xlabel('Возраст')
        plt.rcParams['font.size'] = '12'
        plt.show()

    def sexs(self):
        sexs = self.sexs
        sexsTitle = []
        sexsCount = []
        for sex in sexs:
            sexsTitle.append(sex)
            sexsCount.append(sexs[sex])

        fig, ax = plt.subplots()
        ax.bar(sexsTitle, sexsCount)
        fig.set_figwidth(5)  # ширина Figure
        fig.set_figheight(6)
        plt.title('Статистика по полу')
        plt.ylabel('Кол-во человек')
        plt.xlabel('Пол')
        plt.rcParams['font.size'] = '12'
        plt.show()

    def getFileNames(self):
        filename = QFileDialog.getOpenFileNames(self, "*")
        shutil.copy2(filename, PATH)

    def saveFile(self):
        filename, ok = QFileDialog.getSaveFileName(None, 'Save JSON File', "JSON files (*.json)")
        shutil.copy2(PATH, filename)


def getFriends(user_id):
    count = 5000
    offset = 0
    friends = []
    while offset < MAX_USERS:
        response = requests.get('https://api.vk.com/method/friends.get',
                                params={
                                    'access_token': access_token,
                                    'v': version,
                                    'user_id': user_id,
                                    'count': count,
                                    'offset': offset,
                                }
                                )
        todos = json.loads(response.text)
        if 'error' in todos:
            print(f"error_code {todos['error']['error_code']} : {todos['error']['error_msg']}")
            return friends
        else:
            data = response.json()['response']['items']
            if data.__len__() == 0:
                break
        offset += count
        friends.extend(data)
    return friends


def getMembers(group_id):
    count = 1000
    offset = 0
    members = []
    while offset < MAX_USERS:
        response = get_repeat('https://api.vk.com/method/groups.getMembers',
                              params={
                                  'access_token': access_token,
                                  'v': version,
                                  'group_id': group_id,
                                  'count': count,
                                  'offset': offset,
                              }
                              )
        todos = json.loads(response.text)
        if 'error' in todos:
            print(f"error_code {todos['error']['error_code']} : {todos['error']['error_msg']}")
            return members
        else:
            data = response.json()['response']['items']
            if data.__len__() == 0:
                break
        offset += count
        members.extend(data)
    return members


def get_repeat(url, params):
    repeat = True
    while repeat:
        resp = requests.get(url, params=params)
        data = resp.json()
        if 'error' in data and 'error_code' in data['error']:
            print(f"error_code {data['error']['error_code']} : {data['error']['error_msg']}")
            if data['error']['error_code'] == 6:
                time.sleep(1)
            else:
                repeat = False
        else:
            repeat = False
    return resp


def collecting_online(ids):
    time.sleep(1)
    global users
    users = ids
    count = 1000
    offset = 0
    while offset < ids.__len__():
        user_ids = ','.join([str(i) for i in ids[offset:count + offset]])
        data = requests.get('https://api.vk.com/method/users.get',
                            params={
                                'access_token': access_token,
                                'v': version,
                                'user_ids': user_ids,
                                'fields': 'online'
                            }
                            )
        try:
            users_online = json.loads(data.text)['response']
            for item in users_online:
                users_time[item['id']] = item['online']
        except:
            break;
        offset += count
    check_online()


def check_online():
    global users, hour
    now = datetime.datetime.now()
    if now.hour != hour:
        hour = now.hour
        for item in users_time:
            users_time[item] = 0
    count = 1000
    offset = 0
    while offset < users.__len__():
        user_ids = ','.join([str(i) for i in users[offset:count + offset]])
        while True:
            try:
                data = requests.get('https://api.vk.com/method/users.get',
                                    params={
                                        'access_token': access_token,
                                        'v': version,
                                        'user_ids': user_ids,
                                        'fields': 'online'
                                    }
                                    )
            except:
                print("ERROR CONNECT")
                time.slep(60)
                continue
            break
        try:
            users_online = json.loads(data.text)['response']
            for item in users_online:
                try:
                    users_time[item['id']] += item['online']
                except:
                    users_time[item['id']] = item['online']
            offset += count
        except:
            break;
    save_data()
    threading.Timer(60.0, check_online).start()


def save_data():
    global table
    now = datetime.datetime.now()
    date = str(datetime.date.today())

    if (len(table) == 0):
        try:
            table = json.loads(PATH.read_text(encoding='utf-8'))
        except:
            table = users_time.copy()
            for item in users_time:
                table[item] = None

    for user, time in users_time.items():
        try:
            table[user][date][now.hour] = time
        except:
            try:
                table[user][date] = {now.hour: time}
            except:
                try:
                    table[user] = {date: {now.hour: time}}
                except:
                    f = table

    try:
        PATH.write_text(json.dumps(table), encoding='utf-8')
        print(f"{now.hour}:{now.minute}:{now.second} ------- save data")
    except:
        print(f"{now.hour}:{now.minute}:{now.second} ------- error save data")


def get_details(ids, fields):
    count = 1000
    offset = 0
    users_details = []
    while offset < ids.__len__():
        user_ids = ','.join([str(i) for i in ids[offset:count + offset]])
        data = requests.get('https://api.vk.com/method/users.get',
                            params={
                                'access_token': access_token,
                                'v': version,
                                'user_ids': user_ids,
                                'fields': fields
                            }
                            )
        users_detail = json.loads(data.text)['response']
        users_details.extend(users_detail)
        offset += count
    return users_details


def calculatingStats(users_details):
    cities = {}
    sexs = {'male': 0, 'female': 0}
    countries = {}
    ages = {}
    today = datetime.date.today()
    for user in users_details:
        if 'city' in user:
            try:
                cities[user['city']['title']] += 1
            except KeyError:
                cities[user['city']['title']] = 1
        if 'sex' in user:
            if user['sex'] == 1:
                sexs['female'] += 1
            elif user['sex'] == 2:
                sexs['male'] += 1
        if 'country' in user:
            try:
                countries[user['country']['title']] += 1
            except KeyError:
                countries[user['country']['title']] = 1
        if 'bdate' in user:
            dt = user['bdate'].split('.')
            if dt.__len__() == 3:
                age = today.year - int(dt[2])
                if age in ages:
                    ages[age] += 1
                else:
                    ages[age] = 1
    return cities, sexs, countries, ages


def getUserName(user_ids):
    data = requests.get('https://api.vk.com/method/users.get',
                        params={
                            'access_token': access_token,
                            'v': version,
                            'user_ids': user_ids,
                        }
                        )
    try:
        todos = json.loads(data.text)
        name = todos['response'][0]['last_name'] + " " + todos['response'][0]['first_name']
    except KeyError:
        name = ''
    return name

    return users_details


def getGroupName(group_id):
    response = requests.get('https://api.vk.com/method/groups.getById',
                            params={
                                'access_token': access_token,
                                'v': version,
                                'group_id': group_id,
                                'fields': 'name'
                            }
                            )
    try:
        todos = json.loads(response.text)
        name = todos['response'][0]['name']
    except KeyError:
        name = ''
    return name


if __name__ == '__main__':
    # mass = getFriends(131753976)
    # collecting_online(mass)
    # while(True):
    #    time.sleep(5)

    app = QtWidgets.QApplication([])
    application = startwindow()
    application.show()
    sys.exit(app.exec_())
