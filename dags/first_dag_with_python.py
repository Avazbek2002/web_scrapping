import requests
from bs4 import BeautifulSoup
from airflow.decorators import task
import re
from datetime import datetime, timedelta
from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from utils.scrap_qalampir import scrap_qalampir
from utils.scrap_kunuz import scrap_kunuz
from utils.scrap_xabar import scrap_xabar
from utils.scrap_daryo import scrap_daryo
import certifi
import os
os.system("pip install pymongo")
from pymongo import MongoClient


with DAG(dag_id="web_scrapping_dag", 
         start_date=datetime(2022,1,23), schedule="@daily",
         catchup=False) as dag:
        
    @task(task_id="scrapping_kunuz")
    def scrap_kunuz_operator():
        return scrap_kunuz()

    @task(task_id="scrapping_qalampir")
    def scrap_qalampir_operator():
        return scrap_qalampir()

    @task(task_id="scrapping_xabar")
    def scrap_xabar_operator():
        return scrap_xabar()
    
    @task(task_id="scrapping_daryo")
    def scrap_daryo_operator():
        return scrap_daryo()
    
    @task(task_id="upload_to_the_database")
    def upload_to_database(kunuz, qalampir, xabar, daryo):
        client = MongoClient(
            "mongodb+srv://isroilovavazbek2002:Avazbek2002@cluster0.twxv5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
            tlsCAFile=certifi.where()
        )
        db = client["uzinfocom"]
        collection = db["web_scrapping"]
        collection.insert_many(kunuz)
        print("Inserted kunuz")
        collection.insert_many(qalampir)
        print("Inserted qalampir")
        collection.insert_many(xabar)
        print("Inserted xabar")
        collection.insert_many(daryo)


    kunuz_scrapped = scrap_kunuz_operator()
    qalampir_scrapped = scrap_qalampir_operator()
    xabar_scrapped = scrap_xabar_operator()
    daryo_scrapped = scrap_daryo_operator()
    upload_to_database(kunuz_scrapped, qalampir_scrapped, xabar_scrapped, daryo_scrapped)
    