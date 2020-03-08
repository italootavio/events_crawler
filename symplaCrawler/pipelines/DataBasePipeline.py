# -*- coding: utf-8 -*-
import sqlite3
from _sqlite3 import Error

# Pipeline responsavel por criar as tableas Event e Ticket no Banco de dados e Inserir os dados tratados pelo Pipeline Anterior

class DataBasePipeline(object):
    def process_item(self, item, spider):
        # insere os dados tratados em suas respectivas tabelas
        insert_item = {}

        # se existir algum dado vazio sai do metodo
        for key,value in item.items():
            if value is None:
                return
            else:
                insert_item[key] = value

        # cria um dicionario com os dados organizados para insercao na base de dados
        row = {'id':insert_item['id'],
               'link':insert_item['url'],
               'name':insert_item['name'],
               'description':insert_item['description'],
               'init_date':insert_item['info_calendar'][0],
               'final_date':insert_item['info_calendar'][-1],
               'city_location':insert_item['info_city'][-1],
               'address':insert_item['info_city'][0]}

        # executa a insercao do Evento na tabela Event
        self.conn.execute(
           'INSERT INTO EVENT(ID, DESCRIPTION, LINK, NAME, INIT_DATE, FINAL_DATE, CITY_LOCATION,ADDRESS) '
           'VALUES(:id, :description, :link, :name, :init_date, :final_date, :city_location,:address)',
            row
        )

        # percorre os tickets e insere um a um na tabela Ticket
        for i in range(len(item['ticket_types'])):
            row = {'id':insert_item['id'],'ticket_type':item['ticket_types'][i],'ticket_value':item['ticket_values'][i]}
            self.conn.execute(
                'INSERT INTO TICKET(EVENT_ID, TICKET_TYPE, TICKET_VALUE) '
                'VALUES(:id, :ticket_type, :ticket_value)',
                row
            )
        self.conn.commit()
        return item

    def create_tables(self):
        # metodo responsavel por criar as tabelas Event e Ticket
        try:
            self.conn.execute(
                         "CREATE TABLE IF NOT EXISTS EVENT("
                         "ID INTEGER NOT NULL PRIMARY KEY, "
                         "DESCRIPTION VARCHAR(300),"
                         "LINK VARCHAR(50) NOT NULL,"
                         "NAME VARCHAR(50) NOT NULL, "
                         "INIT_DATE DATETIME NOT NULL, "
                         "FINAL_DATE DATETIME NOT NULL, "
                         "CITY_LOCATION VARCHAR(15) NOT NULL,	"
                         "ADDRESS VARCHAR(20)"
                         ");"
                     )
            self.conn.execute(
                         "CREATE TABLE IF NOT EXISTS TICKET("
                         "EVENT_ID INTEGER NOT NULL, "
                         "TICKET_TYPE VARCHAR(20) NOT NULL, "
                         "TICKET_VALUE REAL NOT NULL, "
                         "FOREIGN KEY (EVENT_ID) REFERENCES EVENT(ID));"
                     )
        except Error as e:
            print(e)

    def create_connection(self,db_file):
        # metodo responsavel por criar a conexao com o SQLite
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

    def open_spider(self, spider):
        # executa a chamada inicial do Pipeline criando a conexao do banco e as tabelas
        locationDB = '../../SGBD/test_Sympla_DB.db'
        self.create_connection(locationDB)
        self.create_tables()

    def close_spide(self, spider):
        # fecha a conexao apos finalizar a execuçao do pipeline
        self.conn.close()
