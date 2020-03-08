# -*- coding: utf-8 -*-

import sqlite3
from _sqlite3 import Error

#Ultima Pipeline, consulta as questoes estabelecidas nas seçoes "Analise" e "Extras" no Banco de dados
class QueryDBPipeline(object):

    def questions(self,spider):

        #Questoes de Analise
        query1 = 'SELECT CITY_LOCATION, COUNT(ID) AS NUMERO_EVENTOS ' \
                'FROM EVENT GROUP BY CITY_LOCATION ORDER BY NUMERO_EVENTOS DESC LIMIT 1'
        spider.logger.info("Qual e a localidade com maior numero de eventos?")
        spider.logger.info((self.conn.execute(query1).fetchall()))

        query2 = 'SELECT AVG (QUANTIDADE) AS MEDIA_LOTE FROM (SELECT E.ID, COUNT(T.TICKET_TYPE) AS QUANTIDADE FROM EVENT E INNER JOIN TICKET T ON E.ID = T.EVENT_ID GROUP BY E.ID);'
        spider.logger.info("Qual e a quantidade media de lotes(tipos de tickets) por eventos?")
        spider.logger.info((self.conn.execute(query2).fetchall()))

        query3 ='SELECT E.LINK, E.NAME, MAX(T.TICKET_VALUE) AS VALOR ' \
               'FROM EVENT E INNER JOIN TICKET T ON E.ID = T.EVENT_ID;'
        spider.logger.info("Dos eventos coletados, qual possui o maior valor de ingresso?")
        spider.logger.info((self.conn.execute(query3).fetchall()))

        #Questao Extra
        query4 ="SELECT COUNT(*) FROM EVENT WHERE DESCRIPTION LIKE UPPER('%http://facebook.com/events%')"
        spider.logger.info("Quantos dos eventos coletados possuem algum link para alguma página do Facebook?")
        spider.logger.info((self.conn.execute(query4).fetchall()))

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

    def close_spider(self, spider):
        # response as questoes e posteriormente fecha a conexao apos finalizar a execuçao do pipeline
        self.questions(spider)
        self.conn.close()