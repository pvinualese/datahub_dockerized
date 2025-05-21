import logging

from datahub.emitter.mce_builder import make_tag_urn
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter

# Imports for metadata model classes
from datahub.metadata.schema_classes import TagPropertiesClass

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

tag_urn = make_tag_urn("fármacos")
tag_properties_aspect = TagPropertiesClass(
    name="Fármacos",
    description="Datasets relacionados con fármacos.",
)

event: MetadataChangeProposalWrapper = MetadataChangeProposalWrapper(
    entityUrn=tag_urn,
    aspect=tag_properties_aspect,
)

# Create rest emitter
rest_emitter = DatahubRestEmitter(gms_server="http://datahub-gms-drugs:8080")
rest_emitter.emit(event)
log.info(f"Created tag {tag_urn}")