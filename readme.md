## build and push
export HW_NUMBER=2.1
scripts/build-push.sh

## install with kube

### install db
helm install otus-hw-db bitnami/postgresql -f k8s/db/values.yaml

### install hello-app
kubectl apply -f k8s/hello-app

