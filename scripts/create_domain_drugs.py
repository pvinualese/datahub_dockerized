import logging

from datahub.emitter.mce_builder import make_domain_urn
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import ChangeTypeClass, DomainPropertiesClass

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARN)

domain_urn = make_domain_urn("medicamentos")
domain_properties_aspect = DomainPropertiesClass(
    name="Medicamentos", description="Dominio para datos de medicamentos"
)

event: MetadataChangeProposalWrapper = MetadataChangeProposalWrapper(
    entityType="domain",
    changeType=ChangeTypeClass.UPSERT,
    entityUrn=domain_urn,
    aspect=domain_properties_aspect,
)

rest_emitter = DatahubRestEmitter(gms_server="http://datahub-gms-drugs:8080")  # Cambia la URL si tu DataHub está en otro host/puerto
rest_emitter.emit(event)
log.info(f"Created domain {domain_urn}")