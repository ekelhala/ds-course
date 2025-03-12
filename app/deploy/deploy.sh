#! /bin/bash
# deploy database
kubectl apply -f ./db
# deploy core services
kubectl apply -f ./core
# deploy monitoring
kubectl apply -f ./monitoring