# API design

This document describes the web API for RANaaS implementation. The API provides endpoints which allow interaction between user and the deployed RAN stack

## Endpoints

Current endpoints available for users

### `/api/ran_resources/`

`POST`: Request provisioning of RAN resources. The response to this request contains details of the resources provisioned, and a unique ID, which allows interaction with the resources.

### `/api/ran_resources/{id}/`

`GET`: Inspect information of the resources currently available. Returns information available from the database.

`DELETE`: Free up the allocated resources and remove any database entries associated to them.

## Ideas

These are potential endpoints/features that could be useful.

### `/api/ran_resources/{id}/status/`

`GET`: Provides real-time status information about the resources currently in use with the reference id. The information could be fetched directly from the cluster.

## Resource definition format

A well-defined format could be used for specifying the properties and amount of resources a client wishes to provision through the API. For example, JSON or YAML could be useful. Example of potential resource definition format below:

```json
{
    "resources": [
        {
            "type": "ru",
            "name": "ru.1",
            "connections": ["du.1"]
        },
        {
            "type": "ru",
            "name": "ru.2",
            "connections": ["du.1"]
        },
        {
            "type": "du",
            "name": "du.1",
            "connections": ["ru.1", "ru.2", "cu.1"]
        },
        {
            "type": "cu",
            "name": "cu.1",
            "connections": ["du.1"]
        }
    ]
}
```

Here, the amount of resources and connections between them would be clearly defined. Each resource is also given a unique name. Another idea related to this is that LLM's could be leveraged here to facilitate resource planning, once a definition format is established.
