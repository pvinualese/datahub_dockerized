import json
from datetime import datetime
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

# Cargar JSON de CKAN (simula respuesta de API)
with open("ckan_sample.json", encoding="utf-8") as f:
    ckan_data = json.load(f)

# Buscar los valores en "extras"
def get_extra_value(extras, key):
    for item in extras:
        if item["key"] == key:
            return item["value"]
    return None

# Crear URN del dataset
dataset_urn = make_dataset_urn(platform="ckan", name=ckan_data["name"], env="PROD")

# Extraer propiedades
description = ckan_data.get("notes", "")
resources = ckan_data.get("resources", [])


# Construir campos personalizados
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
    "access_url": resources[0].get("url"),
    "format": resources[0].get("format"),
    "availability": resources[0].get("availability"),
    "created": resources[0].get("created"),
    "description": resources[0].get("description"),
    "download_url": resources[0].get("download_url"),
    "license": resources[0].get("license"),
    "metadata_modified": resources[0].get("metadata_modified"),
    "mimetype": resources[0].get("mimetype"),
    "name": resources[0].get("name"),
    "rigths": resources[0].get("rights"),
    # "size": resources[0].get("size"),
    "url": resources[0].get("url")
}

# Crear aspecto DatasetProperties
dataset_properties = DatasetPropertiesClass(
    name=ckan_data.get("title", ""),
    description=description,
    customProperties=custom_properties
)

# Asociar tags de CKAN (si hay)
tags = [
    TagAssociationClass(tag=f"urn:li:tag:{tag['name']}") for tag in ckan_data.get("tags", [])
]
global_tags = GlobalTagsClass(tags=tags) if tags else None

# Asociar owner (si quieres que sea la organización como owner)
owner = OwnerClass(
    owner=f"urn:li:corpuser:{ckan_data['organization']['name']}",
    type=OwnershipTypeClass.DATAOWNER,
)
ownership = OwnershipClass(owners=[owner]) if ckan_data.get("organization") else None

# Crear snapshot
snapshot = DatasetSnapshotClass(
    urn=dataset_urn,
    aspects=[dataset_properties] +
            ([global_tags] if global_tags else []) +
            ([ownership] if ownership else [])
)

# Crear el MCE
mce = MetadataChangeEventClass(proposedSnapshot=snapshot)

# Guardar como JSON para DataHub
with open("ckan_mce_transformed.json", "w") as f:
    json.dump([mce.to_obj()], f, indent=2)

print("✅ Datos CKAN convertidos a ckan_mce_transformed.json para DataHub.")
