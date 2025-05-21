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

    result['title'] = f"{medicamento}_events"

    meta = data.get('meta', {})
    results = data.get('results', [])
    event = results[0] if results else {}
    drugs = event.get('patient', {}).get('drug', []) 

    result['disclaimer'] = meta.get('disclaimer')
    result['terms'] = meta.get('terms')
    result['license'] = meta.get('license')
    result['last_updated'] = meta.get('last_updated')
    result['number_of_events'] = meta.get('results', {}).get('total', 0)    
    result['sender_organization'] = event.get('sender', {}).get('senderorganization')
    result['drug_authorization_number'] = str(drugs[0].get('drugauthorizationnumb')) if drugs and drugs[0].get('drugauthorizationnumb') is not None else "Unknown"
    
    result['overview_url'] = "https://open.fda.gov/apis/drug/event/"
    result['usage_url'] = "https://open.fda.gov/apis/drug/event/how-to-use-the-endpoint/"
    result['searchable_fields_url'] = "https://open.fda.gov/apis/drug/event/searchable-fields/"
    result['link'] = f"https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:{medicamento}"
    result['policy'] = {"@context": "http://www.w3.org/ns/odrl.jsonld", "type": "Set", "permission": [{"target": f"{medicamento}_events", "action": "use"}]}

    # Guardar resultado a archivo local (puedes cambiar esto)
    filename = f"{medicamento.lower().replace(' ', '_')}_events.json"
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

    task_zanitac = PythonOperator(
        task_id='fetch_zanitac',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'ZANTAC'},
    )

    task_revlimid = PythonOperator(
    task_id='fetch_revlimid',
    python_callable=fetch_drug_data,
    op_kwargs={'medicamento': 'REVLIMID'},
    )

    task_dupixent = PythonOperator(
        task_id='fetch_dupixent',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'DUPIXENT'},
    )

    task_aspirin = PythonOperator(
        task_id='fetch_aspirin',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'ASPIRIN'},
    )

    task_metformin = PythonOperator(
        task_id='fetch_metformin',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'METFORMIN'},
    )

    task_amlodipine = PythonOperator(
        task_id='fetch_amlodipine',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'AMLODIPINE'},
    )

    task_prednisone = PythonOperator(
        task_id='fetch_prednisone',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'PREDNISONE'},
    )

    task_atorvastatin = PythonOperator(
        task_id='fetch_atorvastatin',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'ATORVASTATIN'},
    )

    task_lyrica = PythonOperator(
        task_id='fetch_lyrica',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'LYRICA'},
    )

    task_eliquis = PythonOperator(
        task_id='fetch_eliquis',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'ELIQUIS'},
    )

    task_pantoprazole = PythonOperator(
        task_id='fetch_pantoprazole',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'PANTOPRAZOLE'},
    )

    task_proactiv_md_adapalene_acne_treatment = PythonOperator(
        task_id='fetch_proactiv_md_adapalene_acne_treatment',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'PROACTIV MD ADAPALENE ACNE TREATMENT'},
    )

    task_tysabri = PythonOperator(
        task_id='fetch_tysabri',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'TYSABRI'},
    )

    task_xarelto = PythonOperator(
        task_id='fetch_xarelto',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'XARELTO'},
    )

    task_ibuprofen = PythonOperator(
        task_id='fetch_ibuprofen',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'IBUPROFEN'},
    )

    task_lipitor = PythonOperator(
        task_id='fetch_lipitor',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'LIPITOR'},
    )

    task_synthroid = PythonOperator(
        task_id='fetch_synthroid',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'SYNTHROID'},
    )

    task_omeprazole = PythonOperator(
        task_id='fetch_omeprazole',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'OMEPRAZOLE'},
    )

    task_oxycontin = PythonOperator(
    task_id='fetch_oxycontin',
    python_callable=fetch_drug_data,
    op_kwargs={'medicamento': 'OXYCONTIN'},
    )

    task_nexium = PythonOperator(
        task_id='fetch_nexium',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'NEXIUM'},
    )

    task_remicade = PythonOperator(
        task_id='fetch_remicade',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'REMICADE'},
    )

    task_vitamin_d = PythonOperator(
        task_id='fetch_vitamin_d',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'VITAMIN D'},
    )

    task_gabapentin = PythonOperator(
        task_id='fetch_gabapentin',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'GABAPENTIN'},
    )

    task_acetaminophen = PythonOperator(
        task_id='fetch_acetaminophen',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'ACETAMINOPHEN'},
    )

    task_vitamin_d3 = PythonOperator(
        task_id='fetch_vitamin_d3',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'VITAMIN D3'},
    )

    task_methotrexate = PythonOperator(
        task_id='fetch_methotrexate',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'METHOTREXATE'},
    )

    task_repatha = PythonOperator(
        task_id='fetch_repatha',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'REPATHA'},
    )

    task_lisinopril = PythonOperator(
        task_id='fetch_lisinopril',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'LISINOPRIL'},
    )

    task_prolia = PythonOperator(
        task_id='fetch_prolia',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'PROLIA'},
    )

    task_dexamethasone = PythonOperator(
        task_id='fetch_dexamethasone',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'DEXAMETHASONE'},
    )

    task_proactiv_md_deep_cleansing_face_wash = PythonOperator(
    task_id='fetch_proactiv_md_deep_cleansing_face_wash',
    python_callable=fetch_drug_data,
    op_kwargs={'medicamento': 'PROACTIV MD DEEP CLEANSING FACE WASH'},
    )

    task_avonex = PythonOperator(
        task_id='fetch_avonex',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'AVONEX'},
    )

    task_tylenol_1 = PythonOperator(
        task_id='fetch_tylenol_1',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'TYLENOL'},
    )

    task_calcium = PythonOperator(
        task_id='fetch_calcium',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'CALCIUM'},
    )

    task_lasix = PythonOperator(
        task_id='fetch_lasix',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'LASIX'},
    )

    task_otezla = PythonOperator(
        task_id='fetch_otezla',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'OTEZLA'},
    )

    task_tylenol_2 = PythonOperator(
        task_id='fetch_tylenol_2',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'TYLENOL'},
    )

    task_proactiv_md_daily_oil_contr = PythonOperator(
        task_id='fetch_proactiv_md_daily_oil_contr',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'PROACTIV MD DAILY OIL CONTR'},
    )

    task_furosemide_1 = PythonOperator(
        task_id='fetch_furosemide_1',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'FUROSEMIDE'},
    )

    task_spiriva = PythonOperator(
        task_id='fetch_spiriva',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'SPIRIVA'},
    )

    task_ranitidine = PythonOperator(
        task_id='fetch_ranitidine',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'RANITIDINE'},
    )

    task_folic_acid = PythonOperator(
        task_id='fetch_folic_acid',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'FOLIC ACID'},
    )

    task_lantus = PythonOperator(
        task_id='fetch_lantus',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'LANTUS'},
    )

    task_tecfidera = PythonOperator(
        task_id='fetch_tecfidera',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'TECFIDERA'},
    )

    task_cymbalta = PythonOperator(
        task_id='fetch_cymbalta',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'CYMBALTA'},
    )

    task_crestor = PythonOperator(
        task_id='fetch_crestor',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'CRESTOR'},
    )

    task_furosemide_2 = PythonOperator(
        task_id='fetch_furosemide_2',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'FUROSEMIDE'},
    )

    task_entresto = PythonOperator(
        task_id='fetch_entresto',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'ENTRESTO'},
    )

    task_plavix = PythonOperator(
        task_id='fetch_plavix',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'PLAVIX'},
    )

    task_humalog = PythonOperator(
        task_id='fetch_humalog',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'HUMALOG'},
    )

    task_forteo = PythonOperator(
        task_id='fetch_forteo',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'FORTEO'},
    )

    task_orencia = PythonOperator(
        task_id='fetch_orencia',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'ORENCIA'},
    )

    task_prilosec = PythonOperator(
        task_id='fetch_prilosec',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'PRILOSEC'},
    )

    task_vitamin_b12 = PythonOperator(
        task_id='fetch_vitamin_b12',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'VITAMIN B12'},
    )

    task_simvastatin = PythonOperator(
        task_id='fetch_simvastatin',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'SIMVASTATIN'},
    )

    task_rituximab = PythonOperator(
        task_id='fetch_rituximab',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'RITUXIMAB'},
    )

    task_xeljanz = PythonOperator(
        task_id='fetch_xeljanz',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'XELJANZ'},
    )

    task_oxycodone = PythonOperator(
        task_id='fetch_oxycodone',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'OXYCODONE'},
    )

    task_avandia = PythonOperator(
        task_id='fetch_avandia',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'AVANDIA'},
    )

    task_ondansetron = PythonOperator(
    task_id='fetch_ondansetron',
    python_callable=fetch_drug_data,
    op_kwargs={'medicamento': 'ONDANSETRON'},
    )

    task_celebrex = PythonOperator(
        task_id='fetch_celebrex',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'CELEBREX'},
    )

    task_cyclophosphamide = PythonOperator(
        task_id='fetch_cyclophosphamide',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'CYCLOPHOSPHAMIDE'},
    )

    task_sertraline = PythonOperator(
        task_id='fetch_sertraline',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'SERTRALINE'},
    )

    task_bisoprolol = PythonOperator(
        task_id='fetch_bisoprolol',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'BISOPROLOL'},
    )

    task_xanax = PythonOperator(
        task_id='fetch_xanax',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'XANAX'},
    )

    task_singulair = PythonOperator(
        task_id='fetch_singulair',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'SINGULAIR'},
    )

    task_symbicort = PythonOperator(
        task_id='fetch_symbicort',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'SYMBICORT'},
    )

    task_paracetamol = PythonOperator(
        task_id='fetch_paracetamol',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'PARACETAMOL'},
    )

    task_prednisolone = PythonOperator(
        task_id='fetch_prednisolone',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'PREDNISOLONE'},
    )

    task_stelara = PythonOperator(
        task_id='fetch_stelara',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'STELARA'},
    )

    task_metoprolol = PythonOperator(
        task_id='fetch_metoprolol',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'METOPROLOL'},
    )

    task_percocet = PythonOperator(
        task_id='fetch_percocet',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'PERCOCET'},
    )

    task_levothyroxine = PythonOperator(
        task_id='fetch_levothyroxine',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'LEVOTHYROXINE'},
    )

    task_neulasta = PythonOperator(
        task_id='fetch_neulasta',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'NEULASTA'},
    )

    task_fish_oil = PythonOperator(
        task_id='fetch_fish_oil',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'FISH OIL'},
    )

    task_zyrtec = PythonOperator(
    task_id='fetch_zyrtec',
    python_callable=fetch_drug_data,
    op_kwargs={'medicamento': 'ZYRTEC'},
    )

    task_protonix = PythonOperator(
        task_id='fetch_protonix',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'PROTONIX'},
    )

    task_cimzia = PythonOperator(
        task_id='fetch_cimzia',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'CIMZIA'},
    )

    task_coumadin = PythonOperator(
        task_id='fetch_coumadin',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'COUMADIN'},
    )

    task_gilenya = PythonOperator(
        task_id='fetch_gilenya',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'GILENYA'},
    )

    task_vitamin_c = PythonOperator(
        task_id='fetch_vitamin_c',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'VITAMIN C'},
    )

    task_dilaudid = PythonOperator(
        task_id='fetch_dilaudid',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'DILAUDID'},
    )

    task_pomalyst = PythonOperator(
        task_id='fetch_pomalyst',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'POMALYST'},
    )

    task_ibrance = PythonOperator(
        task_id='fetch_ibrance',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'IBRANCE'},
    )

    task_actemra = PythonOperator(
        task_id='fetch_actemra',
        python_callable=fetch_drug_data,
        op_kwargs={'medicamento': 'ACTEMRA'},
    )
