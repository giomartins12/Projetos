'''
- Previsão do tempo capitais brasileiras com Webscraping e
banco de dados MySQL e AWS RDS e S3.
'''

import datetime as datetime
import requests
from bs4 import BeautifulSoup as BS
import mysql.connector
import pandas as pd
import boto3


usuario = "user"
senha = "senha"

db_connection = mysql.connector.connect(host='<bd_name>.us-east-1.rds.amazonaws.com',
                                            user=f'{usuario}', password=f'{senha}', database='<bd_name>')
cursor = db_connection.cursor()

page = requests.get("https://www.climatempo.com.br/brasil")
soup = BS(page.text, 'html.parser')
tempo = soup.find_all(class_="card-capitals")
tempos = []

for temp in tempo:
    temperatura = {}
    temperatura['data'] = datetime.date.today().strftime('%y-%m-%d')
    temperatura['hora'] = datetime.datetime.today().time().strftime('%H:%M:%S')
    temperatura['cidade'] = temp.find_all('a', {'class': 'city'})[0].get_text()
    temperatura['temp_max'] = temp.find_all('p', {'class': 'max _margin-r-20'})[0].get_text().strip('\n')
    temperatura['temp_min'] = temp.find_all('p', {'class': 'min'})[0].get_text().strip('\n')
    temperatura['quant_poss'] = temp.find_all('p', {'class': '-gray _flex _align-center'})[0].get_text().strip('\n')

    tempos.append(temperatura)

for busca in tempos:
    inf_data = busca['data']
    inf_hora = busca['hora']
    inf_cidade = busca['cidade']
    inf_temp_max = busca['temp_max']
    inf_temp_min = busca['temp_min']
    inf_quant_poss = busca['quant_poss']

    menu = (f'{inf_data}', f'{inf_hora}', f'{inf_cidade}', f'{inf_temp_max}', f'{inf_temp_min}', f'{inf_quant_poss}')
    sql = "INSERT INTO nome_da_tabela (data, hora, cidade, temp_max, temp_min, quant_poss) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, menu)
    db_connection.commit()

s3_client = boto3.client(
    's3',
    aws_access_key_id='key_id',
    aws_secret_access_key='secret_key'
)

connect = db_connection
listar = 'SELECT * FROM nome_da_tabela'
tempo = pd.read_sql(listar, connect)
tempo.to_csv("nome_da_planilha.csv", index=False)
s3_client.upload_file("nome_da_planilha.csv", "nome_do_bucket", "nome_da_planilha.csv")

cursor.close()
db_connection.close()







