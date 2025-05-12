import json
import requests
from datahub.metadata.schema_classes import (
    DatasetSnapshotClass,
    MetadataChangeEventClass,
    DatasetPropertiesClass,
    GlobalTagsClass,
    TagAssociationClass,
    OwnershipClass,
    OwnerClass,
    OwnershipTypeClass,
)
from datahub.emitter.mce_builder import make_dataset_urn


# Función para extraer valores del campo 'extras'
def get_extra_value(extras, key):
    for item in extras:
        if item["key"] == key:
            return item["value"]
    return None


# Obtener todos los paquetes de la organización 'meteorologia'
ckan_url = "http://localhost:8181/api/3/action/package_search"
# ckan_url = "http://host.docker.internal:8181/api/3/action/package_search"

params = {"q": "organization:meteorologia", "rows": 1000}
response = requests.get(ckan_url, params=params, verify=False)

if response.status_code != 200:
    raise Exception(f"Error en package_search: {response.status_code} - {response.text}")

datasets = response.json()["result"]["results"]

mces = []

for ckan_data in datasets:
    dataset_urn = make_dataset_urn(platform="ckan", name=ckan_data["name"], env="PROD")
    description = ckan_data.get("notes", "")
    resources = ckan_data.get("resources", [])

    resource = resources[0] if resources else {}

    custom_properties = {
        "organization": ckan_data.get("organization", {}).get("title", ""),
        "version": ckan_data.get("version", ""),
        "created": ckan_data.get("metadata_created", ""),
        "modified": ckan_data.get("metadata_modified", ""),
        "url": ckan_data.get("url", ""),
        "access_rights": get_extra_value(ckan_data.get("extras", []), "access_rights"),
        "contact_name": get_extra_value(ckan_data.get("extras", []), "contact_name"),
        "contact_uri": get_extra_value(ckan_data.get("extras", []), "contact_uri"),
        "publisher_type": get_extra_value(ckan_data.get("extras", []), "publisher_type"),
        "spatial_uri": get_extra_value(ckan_data.get("extras", []), "spatial_uri"),
        "temporal_start": get_extra_value(ckan_data.get("extras", []), "temporal_start"),
        "temporal_end": get_extra_value(ckan_data.get("extras", []), "temporal_end"),
        "theme": get_extra_value(ckan_data.get("extras", []), "theme"),
        "access_url": resource.get("url"),
        "format": resource.get("format"),
        "availability": resource.get("availability"),
        "created": resource.get("created"),
        "description": resource.get("description"),
        "download_url": resource.get("download_url"),
        "license": resource.get("license"),
        "metadata_modified": resource.get("metadata_modified"),
        "mimetype": resource.get("mimetype"),
        "name": resource.get("name"),
        "rights": resource.get("rights"),
        "url": resource.get("url"),
    }

    dataset_properties = DatasetPropertiesClass(
        name=ckan_data.get("title", ""),
        description=description,
        customProperties=custom_properties
    )

    tags = [
        TagAssociationClass(tag=f"urn:li:tag:{tag['name']}") for tag in ckan_data.get("tags", [])
    ]
    global_tags = GlobalTagsClass(tags=tags) if tags else None

    owner = OwnerClass(
        owner=f"urn:li:corpuser:{ckan_data['organization']['name']}",
        type=OwnershipTypeClass.DATAOWNER,
    ) if ckan_data.get("organization") else None
    ownership = OwnershipClass(owners=[owner]) if owner else None

    snapshot = DatasetSnapshotClass(
        urn=dataset_urn,
        aspects=[dataset_properties] +
                ([global_tags] if global_tags else []) +
                ([ownership] if ownership else [])
    )

    mce = MetadataChangeEventClass(proposedSnapshot=snapshot)
    mces.append(mce.to_obj())

# Guardar todos los MCEs en un JSON
with open("all_ckan_mces.json", "w", encoding="utf-8") as f:
    json.dump(mces, f, indent=2, ensure_ascii=False)

print(f"✅ Se transformaron {len(mces)} datasets CKAN a DataHub y se guardaron en ckan_mces_all.json.")
