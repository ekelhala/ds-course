# API design

This document describes the web API for RANaaS implementation. The API provides endpoints which allow interaction between user and the deployed RAN stack

## Endpoints

Current endpoints available for users

### `/api/ran_resources/`

`POST`: Request provisioning of RAN resources. The response to this request contains details of the resources provisioned, and a unique ID, which allows interaction with the resources.

### `/api/ran_resources/{id}/`

`GET`: Inspect information of the resources currently available. Returns information available from the database.

`DELETE`: Free up the allocated resources and remove any database entries associated to them.
