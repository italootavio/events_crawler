# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from symplaCrawler.items import Event

import sys
class SymplaSpider(scrapy.Spider):
    name = 'sympla' # nome do spider
    __num_page = 1 # variavel utilizada para percorrer a pagina de eventos
    __num_max_pages = None # variavel utilizada numero maximo de paginas
    __relative_url = 'https://www.sympla.com.br/eventos?ordem=data&pagina=' # url relativa da pagina de eventos

    def __init__(self,num_max_pages=None,*args,**kwargs):
        # sobrecarga do construtor para aceitar o parametro num_max_pages(passagem de paginas por parametro)
        super(SymplaSpider,self).__init__(*args,**kwargs)
        if num_max_pages is None:
            self.__num_max_pages = sys.maxsize
        else:
            self.__num_max_pages = int(num_max_pages)

    def start_requests(self):
        # metodo que iniciar a chamada das Requests utilizando a URL abaixo
        # e chamando metodo __parse_events_page para o tratamento da pagina
        yield Request(
            url="https://www.sympla.com.br/eventos",
            callback=self.__parse_events_page
        )

    def __parse_events_page(self, response):
        # pesquisa o botao "CARREGAT MAIS"
        next_page = response.xpath('//button[@id=\'more-events\']/@data-url').get()
        # caso o botao exista e o numero de paginas for menor do que o maximo estabelecido no construtor da classe
        # inicia outra request recursivamente passando como url a proxima pagina e chamando o metodo __parse_events_page
        if next_page is not [] and self.__num_page < self.__num_max_pages:
            self.__num_page += 1
            yield Request(url=self.__relative_url+str(self.__num_page),callback=self.__parse_events_page)

        # chama o metodo __processes_event_page para tratar a pagina de eventos
        for requisition in self.__processes_event_page(response):
            yield requisition

    def __processes_event_page(self,response):
        # seleciona todos os eventos da pagina e cria uma requisicao para cada um destes, chamando o metodo __parse_event
        events_links = response.xpath('//ul[@class = \'search-result-list w-clearfix\']/li/a/@href').getall()
        if events_links:
            for event in events_links:
                yield Request(url=event,callback=self.__parse_event)

    def __parse_event(self,response):
        # neste metodo e selecionado sao coletados os dados via xpath, sendo estes:
        # URL da pagina, Nome do Evento, Cidade, Data/Horario, Descricao, Tipos e Valores dos Ingressos

        page_type = response.xpath("//meta[@name='description']/@content").get()
        if "SYMPLA BILETO" in page_type.upper():
            return

        event_name = response.xpath('//h1[@class = \'event-name\']/text()').get() # seleciona o Nome do Evento
        event_info_city = response.xpath('//div[@class = \'event-info-city\']/text()').get() # seleciona a Cidade
        event_info_calendar = response.xpath('//div[@class = \'event-info-calendar\']/text()').get() #seleciona a Data e Hora
        event_description = response.xpath("//div[@id='event-txt']").get() # seleciona a Descriçao
        event_ticket_types = response.xpath('//span[@style=\'font-weight: bold; word-break: break-all;\']/text()').getall()
        event_ticket_values = response.xpath("//form/table/tr[not(@class='title') and not(@id='show-discount') and not(@id='discount-form')]/td[not(@class='opt-panel')]/span[not(@style='font-weight: bold; word-break: break-all;') and not(@style='font-size: 11px;font-weight: bold;color: #58C22E;') and not(@class='note')]/text()").getall()

        yield Event(
            url=response.url,
            name=event_name,
            info_city=event_info_city,
            info_calendar=event_info_calendar,
            description=event_description,
            ticket_types=event_ticket_types,
            ticket_values=event_ticket_values
        )