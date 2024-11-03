import os
import sqlite3
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import datetime as dt


class DataBase():
    def __init__(self):
        self.connection = sqlite3.connect('db.db')
        self.cursor = self.connection.cursor()

    def get_curs(self):
        return self.cursor.execute(f"SELECT curs FROM info").fetchone()[0]

    def set_curs(self, curs):
        self.cursor.execute(f"UPDATE info SET curs='{curs}'")
        self.connection.commit()

    def get_service_sacc(self):
        creds_json = os.path.dirname(__file__) + "/credentials.json"
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(
            httplib2.Http())
        return build('sheets', 'v4', http=creds_service)

    def get_status(self, trek):
        service = self.get_service_sacc()

        range_name = f'Треки!A1:Z'
        result = service.spreadsheets().values().get(spreadsheetId='1j3FaWtKbNzuPM8ZdPUkluRgL2n-TWgyETntP79Ly5ho',
                                                     range=range_name).execute()

        values = result.get('values', [])
        for i in values:
            if len(i) > 1 and i[0] == trek:
                return i[1]
        return -1


    def add_link(self, chat_id, link):
        self.cursor.execute(f"UPDATE data set link='{link}' WHERE chat_id={chat_id}")
        self.connection.commit()

    def add_size(self, chat_id, size):
        self.cursor.execute(f"UPDATE data set size='{size}' WHERE chat_id={chat_id}")
        self.connection.commit()

    def add_cost(self, chat_id, cost):
        self.cursor.execute(f"UPDATE data set cost='{cost}' WHERE chat_id={chat_id}")
        self.connection.commit()

    def get_cost(self, chat_id):
        return self.cursor.execute(f"SELECT cost FROM data WHERE chat_id={chat_id}").fetchone()[0]

    def get_link(self, chat_id):
        return self.cursor.execute(f"SELECT link FROM data WHERE chat_id={chat_id}").fetchone()[0]

    def get_size(self, chat_id):
        return self.cursor.execute(f"SELECT size FROM data WHERE chat_id={chat_id}").fetchone()[0]

    def add_user(self, chat_id):
        self.cursor.execute(f"DELETE FROM data WHERE chat_id={chat_id}")
        self.connection.commit()
        self.cursor.execute(f"INSERT INTO data (chat_id) VALUES ({chat_id})")
        self.connection.commit()

    def get_user_data(self, chat_id):
        return self.cursor.execute(f"SELECT * FROM data WHERE chat_id={chat_id}").fetchone()

    def add_dost(self, chat_id, type):
        self.cursor.execute(f"UPDATE data SET dost={type} WHERE chat_id={chat_id}")
        self.connection.commit()

    def is_open(self, chat_id):
        return self.cursor.execute(f"SELECT * FROM users WHERE talk=1 and chat_id={chat_id}").fetchone()

    def add_talk(self, chat_id, txt):
        if self.cursor.execute(f"SELECT * FROM users WHERE chat_id={chat_id}").fetchone():
            return
        if self.open_connect():
            self.cursor.execute(f"INSERT INTO users (chat_id,talk,text) VALUES ({chat_id},0,'{txt}')")
            self.connection.commit()
        else:
            self.cursor.execute(f"INSERT INTO users (chat_id,talk,text) VALUES ({chat_id},1,'{txt}')")
            self.connection.commit()

    def get_open_chat_id(self):
        ask = self.cursor.execute(f"SELECT chat_id FROM users WHERE talk=1").fetchone()
        if ask:
            return ask[0]
        return '-1'
    def open_connect(self):
        return bool(self.cursor.execute(f"SELECT * FROM users WHERE talk=1").fetchone())

    def open_new_connect(self, chat_id):
        self.cursor.execute(f"UPDATE users SET talk=1 WHERE chat_id={chat_id}")
        self.connection.commit()

    def get_connect_text(self, chat_id):
        return self.cursor.execute(f"SELECT text FROM users WHERE chat_id={chat_id}").fetchone()[0]

    def wait_connect(self):
        return self.cursor.execute(f"SELECT chat_id FROM users WHERE talk=0").fetchone()

    def close_talk(self, chat_id):
        self.cursor.execute(f"DELETE FROM users WHERE chat_id={chat_id}")
        self.connection.commit()

    def get_text(self, chat_id):
        data = self.get_user_data(chat_id)
        txt = f"""<b>Размер:</b> {data[3]}
<b>Ссылка:</b> {data[4]}
<b>Стоимость:</b> {data[1]}
<b>Доставка: </b> {'Экспресс' if data[5] == 2 else 'Обычная'}"""
        return txt


db = DataBase()

