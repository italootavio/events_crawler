# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

# Pipeline criada para tratar os dados retirados das paginas de cada evento
class TreatDataPipeline(object):
    def process_item(self, item, spider):
        self.event = item
        self.process_event_id() # extrai o ID do Evento da URL
        self.process_info_city() # processa a Cidade do Evento
        self.process_event_name() # processa o nome do Evento
        self.process_event_description() # processa a Descriçao
        self.process_info_calendar() # processa as Datas e Horarios do Evento
        self.process_ticket_types() # processa os tipos de Tickets
        self.process_ticket_values() # processa os valores dos Tickets

        return self.event

    def process_event_id(self):
        if self.event['url'] is None:
            self.event['id'] = ''
        else:
            self.event['id'] = self.event['url'].split('__')[-1]

    def process_info_city(self):
        if self.event['info_city'] is not None:
            info_city = self.event['info_city']
            self.event['info_city'] = []
            info_city = " ".join(info_city.upper().split())  # remove os espacos em branco e coloca em caixa alta
            for a_division in info_city.split('-'): #divide a string que contem o endereco e adiciona na lista
                self.event['info_city'].append(a_division)

    def process_event_name(self):
        if self.event['name'] is not None:
            self.event['name'] = self.event['name'].upper() # coloca em caixa alta

    def process_event_description(self):
        if self.event['description'] is not None or self.event['description'] is not [] or self.event['description'] !="":
            # utiliza o BeautifulSoup para remover as tags HTML da descriçao do evento
            cleantext = BeautifulSoup(self.event['description'], "lxml").text
            cleantext = " ".join(str(cleantext).upper().split())
            self.event['description'] = cleantext
            ##self.event['description'].append(cleantext)

    def process_info_calendar(self):
        # este metodo coloca o Formato de Saida conforme o formato DATETIME do SQLITE
        # Data formats:
        # Format 1: 05 de fevereiro de 2020, 18h - 29 de abril de 2020, 16h
        # or
        # Format 2: 05 de fevereiro de 2020, 18h-22h30
        # Format output:  [YYYY-MM-DD HH:MM, YYYY-MM-DD HH:MM]

        if self.event['info_calendar'] is not None:
            months = {'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
                      'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
                      'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'}
            convert_date = {'day': '', 'month': '', 'year': '', 'hour': '', 'minute': '00'}
            dateTime_formated = []  # list return
            info_calendar = self.event['info_calendar'].replace(' de ', ' ').replace(',', '')

            if ' - ' in info_calendar:
                # Process format 1
                sliced = info_calendar.split('-')
                for part in sliced:
                    processing_part = " ".join(part.split())
                    separe_date = processing_part.split(' ')
                    convert_date['day'] = separe_date[0]
                    convert_date['month'] = months[separe_date[1]]
                    convert_date['year'] = separe_date[2]
                    time = separe_date[3].split('h')
                    if time[1] == '':
                        convert_date['hour'] = time[0]
                        dateTime_formated.append("{it[year]}-{it[month]}-{it[day]} {it[hour]}:{it[minute]}".format(it=convert_date))
                    else:
                        convert_date['hour'] = time[0]
                        convert_date['minute'] = time[1]
                        dateTime_formated.append("{it[year]}-{it[month]}-{it[day]} {it[hour]}:{it[minute]}".format(it=convert_date))
            else:
                # Process format 2
                processing_part = " ".join(info_calendar.split())
                processing_part = processing_part.replace('-', ' ')
                separe_date = processing_part.split(' ')
                convert_date['day'] = separe_date[0]
                convert_date['month'] = months[separe_date[1]]
                convert_date['year'] = separe_date[2]
                for i in range(3,5):
                    time = separe_date[i].split('h')
                    if time[1] == '':
                        convert_date['hour'] = time[0]
                    else:
                        convert_date['hour'] = time[0]
                        convert_date['minute'] = time[1]

                    dateTime_formated.append("{it[year]}-{it[month]}-{it[day]} {it[hour]}:{it[minute]}".format(it=convert_date))

            self.event['info_calendar'] = dateTime_formated

    def process_ticket_types(self):
        processed_type = []
        for type_t in self.event['ticket_types']:
            processed_type.append(" ".join(type_t.split()).upper())
        self.event['ticket_types'] = processed_type

    def process_ticket_values(self):
        if self.event['ticket_values'] is None:
            self.event['ticket_values'] = []

        # Caso o numero de tipos de tickets seja menor do que o numero de valores de tickes
        # sao adicionados zeros ao final da lista
        # demonstrando assim que os ingressos sao gratis
        while len(self.event['ticket_values']) < len(self.event['ticket_types']):
            self.event['ticket_values'].insert(0,'0')
        processed_value = []
        for value in self.event['ticket_values']:
            value = value.replace(' ', '').replace('R$', '').replace(',', '.')
            processed_value.append(value)
        self.event['ticket_values'] = processed_value