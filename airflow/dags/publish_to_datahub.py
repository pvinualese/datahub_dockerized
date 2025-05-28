import time
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def build_aspect_from_json(input_json):
    title = input_json.get('title', 'Unknown Title')
    drug_name = title.replace('_events', '')
    urn = f"urn:li:dataset:(urn:li:dataPlatform:airflow,{title},PROD)"
    current_time_ms = int(time.time() * 1000)

    aspects = [
        {
            "entityType": "dataset",
            "changeType": "UPSERT",
            "entityUrn": urn,
            "aspectName": "datasetProperties",
            "aspect": {
                "__type": "DatasetProperties",
                "name": title,
                "description": f"Información de los eventos producidos por el medicamento {drug_name}",
                "customProperties": {
                    "disclaimer": input_json.get("disclaimer", ""),
                    "terms": input_json.get("terms", ""),
                    "license": input_json.get("license", ""),
                    "last_updated": input_json.get("last_updated", ""),
                    "number_of_events": input_json.get("number_of_events", ""),
                    "sender_organization": input_json.get("sender_organization", ""),
                    "drug_authorization_number": input_json.get("drug_authorization_number", ""),
                    "overview_url": input_json.get("overview_url", ""),
                    "usage_url": input_json.get("usage_url", ""),
                    "searchable_fields_url": input_json.get("searchable_fields_url", ""),
                    "link": input_json.get("link", ""),
                    "policy": str(input_json.get("policy", ""))
                }
            }
        },
        {
            "entityType": "dataset",
            "changeType": "UPSERT",
            "entityUrn": urn,
            "aspectName": "ownership",
            "aspect": {
                "__type": "Ownership",
                "owners": [
                    {
                        "owner": "urn:li:corpGroup:US-FDA",
                        "type": "DATAOWNER",
                        "source": {
                            "type": "MANUAL",
                            "url": "https://www.fda.gov/"
                        }
                    }
                ],
                "lastModified": {
                    "actor": "urn:li:corpGroup:US-FDA",
                    "time": current_time_ms
                }
            }
        },
        {
            "entityType": "dataset",
            "changeType": "UPSERT",
            "entityUrn": urn,
            "aspectName": "domains",
            "aspect": {
                "__type": "Domains",
                "domains": ["urn:li:domain:medicamentos"]
            }
        },
        {
            "entityType": "dataset",
            "changeType": "UPSERT",
            "entityUrn": urn,
            "aspectName": "glossaryTerms",
            "aspect": {
                "__type": "GlossaryTerms",
                "terms": [
                    {"urn": "urn:li:glossaryTerm:fármacos"}
                ],
                "auditStamp": {
                    "time": current_time_ms,
                    "actor": "urn:li:corpGroup:US-FDA"
                }
            }
        },
        {
            "entityType": "dataset",
            "changeType": "UPSERT",
            "entityUrn": urn,
            "aspectName": "globalTags",
            "aspect": {
                "__type": "GlobalTags",
                "tags": [
                    {
                        "tag": "urn:li:tag:fármacos",
                        "context": "Datasets con información sobre eventos producidos por diferentes fármacos."
                    }
                ]
            }
        }
    ]

    return aspects

def send_aspect_to_datahub(aspect_list: list):
    url = "http://datahub-gms-drugs:8080/openapi/entities/v1/"  
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImRydWdzQGRydWdzLmNvbSIsInR5cGUiOiJQRVJTT05BTCIsInZlcnNpb24iOiIyIiwianRpIjoiNGEzOTExYTgtNWYxYS00OWE4LWI4MTEtMDU4ZDMyOTgwYjZiIiwic3ViIjoiZHJ1Z3NAZHJ1Z3MuY29tIiwiZXhwIjoxNzUxMDE0NDI1LCJpc3MiOiJkYXRhaHViLW1ldGFkYXRhLXNlcnZpY2UifQ.-S7uV_rCesUQ92bse8TzaaeZX_WFsAKc3kh3YsWcvxo'
    }

    response = requests.post(url, headers=headers, json=aspect_list)
    response.raise_for_status()
    print("Enviado a DataHub:", aspect_list[0]['entityUrn'])

def publish_with_aspect(file_path):
    with open(file_path, 'r') as f:
        input_json = json.load(f)
    
    aspect_list = build_aspect_from_json(input_json)
    send_aspect_to_datahub(aspect_list)

with DAG(
    dag_id='publish_to_datahub',
    start_date=datetime(2025, 5, 20),
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
    tags=['datahub', 'openfda'],
) as dag:

    task_publish_zantac = PythonOperator(
    task_id='publish_zantac',
    python_callable=publish_with_aspect,
    op_kwargs={'file_path': '/opt/airflow/zantac_events.json'},
    )

    task_publish_revlimid = PythonOperator(
        task_id='publish_revlimid',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/revlimid_events.json'},
    )

    task_publish_dupixent = PythonOperator(
        task_id='publish_dupixent',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/dupixent_events.json'},
    )

    task_publish_aspirin = PythonOperator(
        task_id='publish_aspirin',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/aspirin_events.json'},
    )

    task_publish_metformin = PythonOperator(
        task_id='publish_metformin',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/metformin_events.json'},
    )

    task_publish_amlodipine = PythonOperator(
        task_id='publish_amlodipine',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/amlodipine_events.json'},
    )

    task_publish_prednisone = PythonOperator(
        task_id='publish_prednisone',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/prednisone_events.json'},
    )

    task_publish_atorvastatin = PythonOperator(
        task_id='publish_atorvastatin',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/atorvastatin_events.json'},
    )

    task_publish_lyrica = PythonOperator(
    task_id='publish_lyrica',
    python_callable=publish_with_aspect,
    op_kwargs={'file_path': '/opt/airflow/lyrica_events.json'},
    )

    task_publish_eliquis = PythonOperator(
        task_id='publish_eliquis',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/eliquis_events.json'},
    )

    task_publish_pantoprazole = PythonOperator(
        task_id='publish_pantoprazole',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/pantoprazole_events.json'},
    )

    task_publish_proactiv_md_adapalene_acne_treatment = PythonOperator(
        task_id='publish_proactiv_md_adapalene_acne_treatment',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/proactiv_md_adapalene_acne_treatment_events.json'},
    )

    task_publish_tysabri = PythonOperator(
        task_id='publish_tysabri',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/tysabri_events.json'},
    )

    task_publish_xarelto = PythonOperator(
        task_id='publish_xarelto',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/xarelto_events.json'},
    )

    task_publish_ibuprofen = PythonOperator(
        task_id='publish_ibuprofen',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/ibuprofen_events.json'},
    )

    task_publish_lipitor = PythonOperator(
        task_id='publish_lipitor',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/lipitor_events.json'},
    )

    task_publish_synthroid = PythonOperator(
        task_id='publish_synthroid',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/synthroid_events.json'},
    )

    task_publish_omeprazole = PythonOperator(
        task_id='publish_omeprazole',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/omeprazole_events.json'},
    )

    task_publish_oxycontin = PythonOperator(
        task_id='publish_oxycontin',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/oxycontin_events.json'},
    )

    task_publish_nexium = PythonOperator(
        task_id='publish_nexium',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/nexium_events.json'},
    )

    task_publish_remicade = PythonOperator(
        task_id='publish_remicade',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/remicade_events.json'},
    )

    task_publish_vitamin_d = PythonOperator(
        task_id='publish_vitamin_d',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/vitamin_d_events.json'},
    )

    task_publish_gabapentin = PythonOperator(
    task_id='publish_gabapentin',
    python_callable=publish_with_aspect,
    op_kwargs={'file_path': '/opt/airflow/gabapentin_events.json'},
    )

    task_publish_acetaminophen = PythonOperator(
        task_id='publish_acetaminophen',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/acetaminophen_events.json'},
    )

    task_publish_vitamin_d3 = PythonOperator(
        task_id='publish_vitamin_d3',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/vitamin_d3_events.json'},
    )

    task_publish_methotrexate = PythonOperator(
        task_id='publish_methotrexate',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/methotrexate_events.json'},
    )

    task_publish_repatha = PythonOperator(
        task_id='publish_repatha',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/repatha_events.json'},
    )

    task_publish_lisinopril = PythonOperator(
        task_id='publish_lisinopril',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/lisinopril_events.json'},
    )

    task_publish_prolia = PythonOperator(
        task_id='publish_prolia',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/prolia_events.json'},
    )

    task_publish_dexamethasone = PythonOperator(
        task_id='publish_dexamethasone',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/dexamethasone_events.json'},
    )

    task_publish_proactiv_md_deep_cleansing_face_wash = PythonOperator(
        task_id='publish_proactiv_md_deep_cleansing_face_wash',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/proactiv_md_deep_cleansing_face_wash_events.json'},
    )

    task_publish_avonex = PythonOperator(
        task_id='publish_avonex',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/avonex_events.json'},
    )

    task_publish_tylenol_1 = PythonOperator(
        task_id='publish_tylenol_1',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/tylenol_events.json'},
    )

    task_publish_calcium = PythonOperator(
        task_id='publish_calcium',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/calcium_events.json'},
    )

    task_publish_lasix = PythonOperator(
    task_id='publish_lasix',
    python_callable=publish_with_aspect,
    op_kwargs={'file_path': '/opt/airflow/lasix_events.json'},
    )

    task_publish_otezla = PythonOperator(
        task_id='publish_otezla',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/otezla_events.json'},
    )

    task_publish_tylenol_2 = PythonOperator(
        task_id='publish_tylenol_2',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/tylenol_events.json'},
    )

    task_publish_proactiv_md_daily_oil_contr = PythonOperator(
        task_id='publish_proactiv_md_daily_oil_contr',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/proactiv_md_daily_oil_contr_events.json'},
    )

    task_publish_furosemide_1 = PythonOperator(
        task_id='publish_furosemide_1',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/furosemide_events.json'},
    )

    task_publish_spiriva = PythonOperator(
        task_id='publish_spiriva',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/spiriva_events.json'},
    )

    task_publish_ranitidine = PythonOperator(
        task_id='publish_ranitidine',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/ranitidine_events.json'},
    )

    task_publish_folic_acid = PythonOperator(
        task_id='publish_folic_acid',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/folic_acid_events.json'},
    )

    task_publish_lantus = PythonOperator(
        task_id='publish_lantus',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/lantus_events.json'},
    )

    task_publish_tecfidera = PythonOperator(
        task_id='publish_tecfidera',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/tecfidera_events.json'},
    )

    task_publish_cymbalta = PythonOperator(
        task_id='publish_cymbalta',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/cymbalta_events.json'},
    )

    task_publish_crestor = PythonOperator(
        task_id='publish_crestor',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/crestor_events.json'},
    )

    task_publish_furosemide_2 = PythonOperator(
    task_id='publish_furosemide_2',
    python_callable=publish_with_aspect,
    op_kwargs={'file_path': '/opt/airflow/furosemide_events.json'},
    )

    task_publish_entresto = PythonOperator(
        task_id='publish_entresto',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/entresto_events.json'},
    )

    task_publish_plavix = PythonOperator(
        task_id='publish_plavix',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/plavix_events.json'},
    )

    task_publish_humalog = PythonOperator(
        task_id='publish_humalog',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/humalog_events.json'},
    )

    task_publish_forteo = PythonOperator(
        task_id='publish_forteo',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/forteo_events.json'},
    )

    task_publish_orencia = PythonOperator(
        task_id='publish_orencia',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/orencia_events.json'},
    )

    task_publish_prilosec = PythonOperator(
        task_id='publish_prilosec',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/prilosec_events.json'},
    )

    task_publish_vitamin_b12 = PythonOperator(
        task_id='publish_vitamin_b12',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/vitamin_b12_events.json'},
    )

    task_publish_simvastatin = PythonOperator(
        task_id='publish_simvastatin',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/simvastatin_events.json'},
    )

    task_publish_rituximab = PythonOperator(
        task_id='publish_rituximab',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/rituximab_events.json'},
    )

    task_publish_xeljanz = PythonOperator(
    task_id='publish_xeljanz',
    python_callable=publish_with_aspect,
    op_kwargs={'file_path': '/opt/airflow/xeljanz_events.json'},
    )

    task_publish_oxycodone = PythonOperator(
        task_id='publish_oxycodone',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/oxycodone_events.json'},
    )

    task_publish_avandia = PythonOperator(
        task_id='publish_avandia',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/avandia_events.json'},
    )

    task_publish_ondansetron = PythonOperator(
        task_id='publish_ondansetron',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/ondansetron_events.json'},
    )

    task_publish_celebrex = PythonOperator(
        task_id='publish_celebrex',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/celebrex_events.json'},
    )

    task_publish_cyclophosphamide = PythonOperator(
        task_id='publish_cyclophosphamide',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/cyclophosphamide_events.json'},
    )

    task_publish_sertraline = PythonOperator(
        task_id='publish_sertraline',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/sertraline_events.json'},
    )

    task_publish_bisoprolol = PythonOperator(
        task_id='publish_bisoprolol',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/bisoprolol_events.json'},
    )

    task_publish_xanax = PythonOperator(
        task_id='publish_xanax',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/xanax_events.json'},
    )

    task_publish_singulair = PythonOperator(
        task_id='publish_singulair',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/singulair_events.json'},
    )

    task_publish_symbicort = PythonOperator(
        task_id='publish_symbicort',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/symbicort_events.json'},
    )

    task_publish_paracetamol = PythonOperator(
        task_id='publish_paracetamol',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/paracetamol_events.json'},
    )

    task_publish_prednisolone = PythonOperator(
        task_id='publish_prednisolone',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/prednisolone_events.json'},
    )

    task_publish_stelara = PythonOperator(
        task_id='publish_stelara',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/stelara_events.json'},
    )

    task_publish_metoprolol = PythonOperator(
        task_id='publish_metoprolol',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/metoprolol_events.json'},
    )

    task_publish_percocet = PythonOperator(
        task_id='publish_percocet',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/percocet_events.json'},
    )

    task_publish_levothyroxine = PythonOperator(
        task_id='publish_levothyroxine',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/levothyroxine_events.json'},
    )

    task_publish_neulasta = PythonOperator(
        task_id='publish_neulasta',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/neulasta_events.json'},
    )

    task_publish_fish_oil = PythonOperator(
        task_id='publish_fish_oil',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/fish_oil_events.json'},
    )

    task_publish_zyrtec = PythonOperator(
        task_id='publish_zyrtec',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/zyrtec_events.json'},
    )

    task_publish_protonix = PythonOperator(
        task_id='publish_protonix',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/protonix_events.json'},
    )

    task_publish_cimzia = PythonOperator(
        task_id='publish_cimzia',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/cimzia_events.json'},
    )

    task_publish_coumadin = PythonOperator(
    task_id='publish_coumadin',
    python_callable=publish_with_aspect,
    op_kwargs={'file_path': '/opt/airflow/coumadin_events.json'},
    )

    task_publish_gilenya = PythonOperator(
        task_id='publish_gilenya',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/gilenya_events.json'},
    )

    task_publish_vitamin_c = PythonOperator(
        task_id='publish_vitamin_c',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/vitamin_c_events.json'},
    )

    task_publish_dilaudid = PythonOperator(
        task_id='publish_dilaudid',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/dilaudid_events.json'},
    )

    task_publish_pomalyst = PythonOperator(
        task_id='publish_pomalyst',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/pomalyst_events.json'},
    )

    task_publish_ibrance = PythonOperator(
        task_id='publish_ibrance',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/ibrance_events.json'},
    )

    task_publish_actemra = PythonOperator(
        task_id='publish_actemra',
        python_callable=publish_with_aspect,
        op_kwargs={'file_path': '/opt/airflow/actemra_events.json'},
    )
