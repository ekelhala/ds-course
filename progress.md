# 6/3/2025

API and worker service can interact. API sends requests to create or delete deployments to the worker service, and worker service performs these actions and reports the result. MongoDB is used to store the configurations of the RAN deployments.

There is a Grafana dashboard with metrics such as amounts of requests processed by API and worker.

Nginx load balancer is used in front of the API service and metrics-service.

[Video Link](https://unioulu-my.sharepoint.com/:v:/r/personal/ekelhala20_univ_yo_oulu_fi/Documents/2025-03-06%2009-16-29.mp4?csf=1&web=1&e=4DlGO2&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)