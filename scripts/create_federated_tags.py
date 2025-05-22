import logging

from datahub.emitter.mce_builder import make_tag_urn
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import TagPropertiesClass

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def create_tag(gms_server, tag_name, display_name, description):
    rest_emitter = DatahubRestEmitter(gms_server=gms_server)
    tag_urn = make_tag_urn(tag_name)
    tag_properties_aspect = TagPropertiesClass(
        name=display_name,
        description=description,
    )
    event = MetadataChangeProposalWrapper(
        entityUrn=tag_urn,
        aspect=tag_properties_aspect,
    )
    rest_emitter.emit(event)
    log.info(f"Created tag {tag_urn} on {gms_server}")

if __name__ == "__main__":
    create_tag(
        gms_server="http://datahub-gms-federado:8080",
        tag_name="fármacos",
        display_name="Fármacos",
        description="Datasets relacionados con fármacos.",
    )

    create_tag(
        gms_server="http://datahub-gms-federado:8080",
        tag_name="clima",
        display_name="Clima",
        description="Datasets relacionados con la climatología.",
    )

    create_tag(
        gms_server="http://datahub-gms-federado:8080",
        tag_name="precipitations",
        display_name="Precipitations",
        description="Datasets relacionados con precipitaciones meteorológicas.",
    )
