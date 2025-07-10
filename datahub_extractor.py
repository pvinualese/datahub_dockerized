import requests
import json
import time

# Configuración drugs
# GRAPHQL_URL = "http://localhost:8086/api/graphql"
# AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImRhdGFodWIiLCJ0eXBlIjoiUEVSU09OQUwiLCJ2ZXJzaW9uIjoiMiIsImp0aSI6ImRlOTA4NDVmLThmNjktNGNjYi1iOTg3LTM5ODZiMjZlYTdlZSIsInN1YiI6ImRhdGFodWIiLCJleHAiOjE3NTMwMDg4NTQsImlzcyI6ImRhdGFodWItbWV0YWRhdGEtc2VydmljZSJ9.gXnbW6Uv6gI13pNrA55SlBAZS4hWk6-QO4zPyuEwmAU"

# Configuración federado
GRAPHQL_URL = "http://localhost:8084/api/graphql"
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhY3RvclR5cGUiOiJVU0VSIiwiYWN0b3JJZCI6ImRhdGFodWIiLCJ0eXBlIjoiUEVSU09OQUwiLCJ2ZXJzaW9uIjoiMiIsImp0aSI6ImQ3M2E0NTFkLWFhOTktNDU5ZC1hZGJmLTg2M2Q5ZDU0Y2RhZiIsInN1YiI6ImRhdGFodWIiLCJleHAiOjE3NTQ3MzUxMDEsImlzcyI6ImRhdGFodWItbWV0YWRhdGEtc2VydmljZSJ9.iSRR3v5cxyuAYvFDCeMKtV4rmVCz03ctyhvm45Lb9MY"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": AUTH_TOKEN
}

# Utilidad para hacer peticiones GraphQL
def run_query(query, variables=None):
    response = requests.post(
        GRAPHQL_URL,
        headers=HEADERS,
        json={"query": query, "variables": variables or {}}
    )
    response.raise_for_status()
    return response.json()["data"]

def get_domains():
    query = """
    {
      search(input: { type: DOMAIN, query: "*", start: 0, count: 50 }) {
        searchResults {
          entity {
            ... on Domain {
              urn
              properties {
                name
                description
              }
            }
          }
        }
      }
    }
    """
    data = run_query(query)
    return [d["entity"] for d in data["search"]["searchResults"]]

def get_datasets_by_domain(domain_urn):
    query = """
    query($urn: String!) {
      searchAcrossEntities(
        input: {
          query: "*"
          filters: [{ field: "domains", values: [$urn] }]
          types: [DATASET]
          start: 0
          count: 100
        }
      ) {
        searchResults {
          entity {
            ... on Dataset {
              urn
              name
              platform { name }
            }
          }
        }
      }
    }
    """
    data = run_query(query, {"urn": domain_urn})
    return [d["entity"] for d in data["searchAcrossEntities"]["searchResults"]]

def get_dataset_details(urn):
    query = """
    query($urn: String!) {
      dataset(urn: $urn) {
        urn
        name
        description
        platform { name }
        properties {
          name
          description
          customProperties { key value }
        }
        ownership {
          owners {
            owner {
              ... on CorpGroup {
                name
              }
            }
          }
        }
        tags { tags { tag { name } } }
        schemaMetadata {
          fields { fieldPath type }
        }
        domain {
          domain { properties { name } }
        }
        glossaryTerms {
          terms {
            term {
              glossaryTermInfo {
                name
                description
              }
            }
          }
        }
      }
    }
    """
    try:
        return run_query(query, {"urn": urn})["dataset"]
    except Exception as e:
        print(f"❌ Error al obtener detalles del dataset {urn}: {e}")
        return None

def main():
    result = []

    print("🔍 Obteniendo dominios...")
    domains = get_domains()
    print(f"✅ {len(domains)} dominios encontrados.")

    for domain in domains:
        domain_urn = domain["urn"]
        domain_props = domain.get("properties", {})
        domain_obj = {
            "urn": domain_urn,
            "name": domain_props.get("name", ""),
            "description": domain_props.get("description", ""),
            "datasets": []
        }

        print(f"\n📁 Procesando dominio: {domain_obj['name']}")

        datasets = get_datasets_by_domain(domain_urn)
        print(f"   → {len(datasets)} datasets encontrados.")

        for ds in datasets:
            print(f"      ↳ Detalles: {ds['name']}")
            details = get_dataset_details(ds["urn"])
            if details:
                domain_obj["datasets"].append(details)
            time.sleep(0.15)  # evitar saturar

        result.append(domain_obj)

    # Guardar archivo estructurado por dominio
    with open("datahub_full_export.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("\n💾 Archivo guardado como datahub_full_export.json")

if __name__ == "__main__":
    main()