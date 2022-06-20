'''
- Mostra a previsão do tempo de uma cidade via API de site
com armazenamento em banco de dados MySQL no AWS RDS e S3.
'''

import requests
import datetime
import mysql.connector
from mysql.connector import errorcode
import logging
import pandas as pd
import boto3


usuario = "user"
senha = "senha"

def cadastra_tempo():
    inf_cidade = cidade
    inf_data = data
    inf_hora = hora_format
    inf_descricao = descricao
    inf_temp = temp
    menu = (f'{inf_cidade}', f'{inf_data}', f'{inf_hora}', f'{inf_descricao}', inf_temp,)
    sql = "INSERT INTO nome_da_tabela (cidade, data, hora, Condição, temperatura) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, menu)
    db_connection.commit()


# Conexão banco de dados

try:
    db_connection = mysql.connector.connect(host='bd_name.us-east-1.rds.amazonaws.com',
                                            user=f'{usuario}', password=f'{senha}', database='bd_name')

except mysql.connector.Error as error:
    if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        logging.critical("\nErro na conexão com banco de dados...login ou senha!")
    elif error.errno == errorcode.ER_BAD_DB_ERROR:
        logging.critical("Erro de inicialização do banco de dados!")
    else:
        logging.WARNING(error)
else:
    logging.info("Banco de dados conectado!")
    logging.debug(db_connection)
    cursor = db_connection.cursor()

# Conexão com bucket S3

s3_client = boto3.client(
    's3',
    aws_access_key_id='key_id',
    aws_secret_access_key='Secret_key'
)


# Conectando com API de previsão do tempo

# link do open_weather: https://openweathermap.org/

API_KEY = "Codigo gerado pela Api do site"
cidade = "cidade a escolha"
link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&lang=pt_br"

requisicao = requests.get(link)
requisicao_dic = requisicao.json()
descricao = requisicao_dic['weather'][0]['description']
temperatura = requisicao_dic['main']['temp'] - 273.15
temp = round(temperatura)
data = datetime.date.today()
hora = datetime.datetime.today().time()
hora_format = str(hora)[:-7]
cadastra_tempo()
connect = db_connection
listar = 'SELECT * FROM nome_da_tabela'
tempo = pd.read_sql(listar, connect)
tempo.to_csv("nome_da_planilha.csv", index=False)
s3_client.upload_file("nome_da_planilha.csv", "nome_do_bucket", "nome_da_planilha.csv")

# Gerando arquivo de log

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    filename="tempo.log")
s3_client.upload_file("nome_do_log.log", "nome_do_bucket", "nome_do_log.log")


print(cidade, data, hora_format)
print(descricao, f"{temp}ºC")


cursor.close()
db_connection.close()

