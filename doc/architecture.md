# Service architecture for RANaaS service using srsRAN and Kubernetes

The proposed architecture consists of an API microservice that receives resource requests from core network operators, and forwards them to a worker microservice that provisions the required resources (virtualized CU and DU), and connects the DU to a number of RUs.

After finishing its work, the worker service reports back to the API service, which sends a reponse containing connection details in order to connect the core network to the provisioned CU.


