import json
from org.apache.nifi.processor.io import StreamCallback
from java.io import InputStream, OutputStream
import time


def transform_json(input_json):
    # Get 'keywords' as a string
    keywords_str = input_json.get("keywords", "[]")
    try:
        tags = json.loads(keywords_str)
    except Exception:
        tags = []

    urn = "urn:li:dataset:(urn:li:dataPlatform:nifi," + input_json.get('packageName', 'Unknown Name') + ",PROD)"

    # Get current timestamp in milliseconds
    current_time_ms = int(time.time() * 1000)

    transformed = [
        {
            "entityType": "dataset",
            "entityUrn": urn,
            "aspect": {
                "__type": "DatasetProperties",  # Aspecto del dataset
                "name": input_json.get("packageName", "Unknown Name"),
                "description": input_json.get("packageDescription", "No description available"),
                "tags": tags,
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
        },
        {
            "entityType": "dataset",
            "entityUrn": urn,
            "aspect": {
                "__type": "Ownership",
                "owners": [
                    {
                        "owner": "urn:li:corpGroup:AEMET",
                        "type": "DATAOWNER",
                        "source": {
                            "type": "MANUAL",
                            "url": "https://www.aemet.es"
                        }
                    }
                ],
                "lastModified": {
                    "actor": "urn:li:corpGroup:AEMET",
                    "time": current_time_ms
                }
            }
        },
        {
            "entityType": "dataset",
            "entityUrn": urn,
            "aspect": {
                "__type": "Domains",
                "domains": ["urn:li:domain:meteorologia"]
            }
        },
        {
            "entityType": "dataset",
            "entityUrn": urn,
            "aspect": {
                "__type": "GlossaryTerms",
                "terms": [
                    {"urn": "urn:li:glossaryTerm:precipitations"}
                ],
                "auditStamp": {
                    "time": current_time_ms,
                    "actor": "urn:li:corpGroup:AEMET"
                }
            }
        },
        {
            "entityType": "dataset",
            "entityUrn": urn,
            "aspect": {
                "__type": "GlobalTags",
                "tags": [
                    {
                        "tag": "urn:li:tag:precipitations",
                        "context": "Dataset contains precipitation data"
                    }
                ]
            }
        }      
    ]

    return transformed


# Get the current flowFile and session
flowFile = session.get()
if flowFile is not None:
    json_attributes = flowFile.getAttribute("JSONAttributes")
    input_json = json.loads(json_attributes)
    transformed_json = transform_json(input_json)
    session.write(flowFile, lambda outputStream: outputStream.write(json.dumps(transformed_json).encode('utf-8')))
    session.transfer(flowFile, REL_SUCCESS)
