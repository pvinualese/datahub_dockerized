import logging
from datahub.emitter.mce_builder import make_domain_urn
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import ChangeTypeClass, DomainPropertiesClass

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def create_domain(emitter, domain_name, display_name, description):
    domain_urn = make_domain_urn(domain_name)
    domain_properties_aspect = DomainPropertiesClass(
        name=display_name,
        description=description
    )
    event = MetadataChangeProposalWrapper(
        entityType="domain",
        changeType=ChangeTypeClass.UPSERT,
        entityUrn=domain_urn,
        aspect=domain_properties_aspect,
    )
    emitter.emit(event)
    log.info(f"Created/Updated domain {domain_urn}")

if __name__ == "__main__":
    # Puedes cambiar estas URLs si tienes diferentes servidores GMS para cada dominio
    emitter_drugs = DatahubRestEmitter(gms_server="http://datahub-gms-federado:8080")
    emitter_prec = DatahubRestEmitter(gms_server="http://datahub-gms-federado:8080")

    create_domain(emitter_drugs, "medicamentos", "Medicamentos", "Dominio para datos de medicamentos")
    create_domain(emitter_prec, "meteorologia", "Meteorología", "Dominio para datos meteorológicos")
