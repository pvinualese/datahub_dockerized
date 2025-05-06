import json
from org.apache.nifi.processor.io import StreamCallback
from java.io import InputStream, OutputStream

def transform_json(input_json):
    keywords_str = input_json.get("keywords", "[]")
    try:
        tags_list = json.loads(keywords_str)
        if not isinstance(tags_list, list):
            tags_list = []
    except json.JSONDecodeError:
        tags_list = []

    entity_urn = "urn:li:dataset:(urn:li:dataPlatform:nifi," + input_json.get('packageName', 'Unknown Name') + ",PROD)"

    # Aspecto de DatasetProperties
    dataset_properties_aspect = {
        "entityType": "dataset",
        "entityUrn": entity_urn,
        "changeType": "UPSERT",
        "aspectName": "datasetProperties",
        "aspect": {
            "value": {
                "name": input_json.get("packageName", "Unknown Name"),
                "description": input_json.get("packageDescription", "No description available"),
                "customProperties": {
                    "resource_rights": input_json.get("resourceRights", "Unknown Resource Rights"),
                    "spatial_uri": input_json.get("spatialURI", "Unknown Spatial URI"),
                    "byte_size": input_json.get("byteSize", 0),
                    "contact_point": input_json.get("contactPoint", "Unknown URI"),
                    "access_url": input_json.get("accessURL", "Unknown Access URL"),
                    "download_url": input_json.get("downloadURL", "Unknown Download URL"),
                    "availability": input_json.get("availability", "Unknown Availability"),
                    "dataset_rights": input_json.get("datasetRights", "Unknown Dataset Rights"),
                    "themes": input_json.get("themes", ["Unknown Theme"]),
                    "license_type": input_json.get("licenseType", "Unknown License Type"),
                    "description": input_json.get("packageDescription", "No description available"),
                    "temporal_start": input_json.get("temporalStart", "Unknown Date"),
                    "station_name_address": input_json.get("station_name_address", "Unknown Address"),
                    "visibility": input_json.get("visibility", "Unknown Visibility"),
                    "contact_name": input_json.get("contactName", "Unknown Contact Name"),
                    "station_id": input_json.get("station_id", "Unknown Station ID"),
                    "landing_page": input_json.get("landingPage", "Unknown Landing Page"),
                    "format": input_json.get("format", "Unknown Format"),
                    "resource_description": input_json.get("resourceDescription", "No description available"),
                    "resource_name": input_json.get("resourceName", "Unknown Resource Name"),
                    "entity_id": input_json.get("entity_id", "Unknown Entity ID"),
                    "publisher_url": input_json.get("publisherURL", "Unknown Publisher URL"),
                    "version": input_json.get("version", "Unknown Date"),
                    "organization_type": input_json.get("organizationType", "Unknown Organization Type"),
                    "license": input_json.get("license", "Unknown License"),
                    "mimetype": input_json.get("mimetype", "Unknown MIME type"),
                    "link": input_json.get("Link", "Unknown link")
                }
            }
        }
    }

    # Aspecto de globalTags (si hay tags)
    global_tags_aspect = {
        "entityType": "dataset",
        "entityUrn": entity_urn,
        "changeType": "UPSERT",
        "aspectName": "globalTags",
        "aspect": {
            "value": {
                "tags": [{"tag": f"urn:li:tag:{tag.strip().lower().replace(' ', '_')}"} for tag in tags_list]
            }
        }
    }

    transformed = [dataset_properties_aspect]
    if tags_list:
        transformed.append(global_tags_aspect)

    return transformed

# Get the current flowFile and session
flowFile = session.get()
if flowFile is not None:
    json_attributes = flowFile.getAttribute("JSONAttributes")
    try:
        input_json = json.loads(json_attributes)
        transformed_json = transform_json(input_json)
        session.write(flowFile, lambda out: out.write(json.dumps(transformed_json).encode('utf-8')))
        session.transfer(flowFile, REL_SUCCESS)
    except Exception as e:
        log.error("Error al transformar MCP: " + str(e))
        session.transfer(flowFile, REL_FAILURE)
