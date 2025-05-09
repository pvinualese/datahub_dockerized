import logging

from datahub.emitter.mce_builder import make_term_urn
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import GlossaryTermInfoClass, ChangeTypeClass

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# El identificador debe ser sin espacios ni acentos
term_urn = make_term_urn("clima")
term_properties_aspect = GlossaryTermInfoClass(
    definition="Datasets de climatología.",
    name="Clima",
    termSource="",
)

event: MetadataChangeProposalWrapper = MetadataChangeProposalWrapper(
    entityUrn=term_urn,
    aspect=term_properties_aspect    
)

rest_emitter = DatahubRestEmitter(gms_server="http://datahub-gms-clima:8080")  # Cambia la URL si tu DataHub está en otro host/puerto
rest_emitter.emit(event)
log.info(f"Created term {term_urn}")