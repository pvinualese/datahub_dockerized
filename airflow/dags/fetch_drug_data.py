from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_drug_data(medicamento: str):
    api_key = "hvowKCAWViRvZqWuepoLTkPYS2AdiIV2HiJ1wSkB"
    url = f"https://api.fda.gov/drug/event.json?api_key={api_key}&search=patient.drug.medicinalproduct:{medicamento}&limit=1"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    result = {}
    meta = data.get('meta', {})
    result['disclaimer'] = meta.get('disclaimer')
    result['terms'] = meta.get('terms')
    result['license'] = meta.get('license')
    result['last_updated'] = meta.get('last_updated')
    result['total_results'] = meta.get('results', {}).get('total', 0)
    
    # Extraer datos del primer evento
    results = data.get('results', [])
    if results:
        event = results[0]
        result['sender_organization'] = event.get('sender', {}).get('senderorganization')
        drugs = event.get('patient', {}).get('drug', [])
        if drugs:
            result['drug_authorization_number'] = drugs[0].get('drugauthorizationnumb')
        else:
            result['drug_authorization_number'] = None
    else:
        result['sender_organization'] = None
        result['drug_authorization_number'] = None

    # Guardar resultado a archivo local (puedes cambiar esto)
    filename = f"{medicamento.lower()}_events.json"
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Datos guardados para {medicamento} en {filename}")

with DAG(
    dag_id='fetch_drug_events',
    start_date=datetime(2025, 5, 20),
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
    tags=['openfda', 'drug'],
) as dag:

    task_ibuprofen = PythonOperator(
        task_id='fetch_ibuprofen',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'IBUPROFEN'},
    )

    task_aspirin = PythonOperator(
        task_id='fetch_aspirin',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'ASPIRIN'},
    )

    task_ibuprofen >> task_aspirin
