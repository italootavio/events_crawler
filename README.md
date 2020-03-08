# events_crawler


O programa é um Crawler que utiliza a Biblioteca Scrapy para obter dados de evento do site https://www.sympla.com.br.

Para executar o código é necessário que possuir os pacotes do scrapy, sqlite3, protego e beautifulsoup4 instalados no python virtual environment.

A execução do cógido deve ser feita chamando o aquivo sympla.py utilizando o comando abaixo:

scrapy runspider sympla.py

Sendo que, a sua localização é events_sympla/symplaCrawler/spiders/sympla.py

Também é possível informar o número de páginas a serem percorridas pelo crawler utilizando o comando abaixo:

scrapy runspider sympla.py -a num_max_pages=2

Ao executar o programa, a Classe SymplaSpider é instanciada e assim o algoritmo começa a rastrear o conteúdo da página.

Para fins de tratamento de dados foram criados 3 pipelines presentes na pasta Pipelines. Sua ordem de execução é: TreatDataPipeline, DataBasePipeline e QueryDBPipeline respectivamente.

O primeiro é responsável por tratar os dados obtidos pelo crawler. O segundo por criar as tabelas no Banco SQLite e inserir os seus dados. O terceiro por efetuar as consultas de informações retiradas do site em questão.
