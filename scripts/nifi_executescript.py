import json
from org.apache.nifi.processor.io import StreamCallback
from java.io import InputStream, OutputStream

# Define the transformation function
def transform_json(input_json):
    # Define the mapping from the original JSON to the MCP structure
    transformed = [{
        "entityType": "dataset",
        "entityUrn": "urn:li:dataset:(urn:li:dataPlatform:nifi," + input_json.get('packageName', 'Unknown Name') + ",PROD)",
        "aspect": {
            "__type": "DatasetProperties",
            "name": input_json.get("packageName", "Unknown Name"),
            "description": input_json.get("packageDescription", "No description available"),
            "customProperties": {
                "resource_rights": input_json.get("resourceRights", "Unknown Resource Rights"),
                "spatial_uri": input_json.get("spatialURI", "Unknown Spatial URI"),
                "keywords": input_json.get("keywords", ["Unknown Keyword"]),
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
    }]
    
    return transformed

# Get the current flowFile and session
flowFile = session.get()
if flowFile is not None:
    # Get the attribute "jsonattributes" from the flowFile
    json_attributes = flowFile.getAttribute("JSONAttributes")
    
    # Parse the JSON string from the attribute
    input_json = json.loads(json_attributes)
    
    # Transform the incoming JSON to the desired MCP format
    transformed_json = transform_json(input_json)
    
    # Write the transformed JSON back to the content of the flowFile
    session.write(flowFile, lambda outputStream: outputStream.write(json.dumps(transformed_json).encode('utf-8')))
    
    # Transfer the flowFile to the next processor
    session.transfer(flowFile, REL_SUCCESS)
