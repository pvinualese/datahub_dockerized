from datahub.metadata.schema_classes import (
    DatasetSnapshotClass,
    MetadataChangeEventClass,
    DatasetPropertiesClass,
)
from datahub.emitter.mce_builder import make_dataset_urn
import json
from datetime import datetime

# Crear URN del dataset
dataset_urn = make_dataset_urn(platform="demo", name="example_table", env="PROD")

# Crear aspecto de propiedades con un nuevo campo 'owner'
properties = DatasetPropertiesClass(
    description="Tabla de ejemplo para pruebas",
    tags=[],  # Lista vacía de etiquetas
    owner="John Doe"  # Nuevo campo 'owner' agregado
)

# Crear snapshot con el aspecto
snapshot = DatasetSnapshotClass(
    urn=dataset_urn,
    aspects=[properties],
)

# Crear evento de cambio de metadatos (MCE) con un campo adicional 'changeTimestamp'
mce = MetadataChangeEventClass(
    proposedSnapshot=snapshot,
    changeType="UPSERT",  # Especificamos que es una inserción o actualización
    changeTimestamp=datetime.utcnow().isoformat()  # Nueva fecha de cambio
)

# Guardar como JSON en el formato adecuado
with open("sample_data.json", "w") as f:
    json.dump([mce.to_obj()], f, indent=2)


