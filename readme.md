## build and push
export HW_NUMBER=2.1
scripts/build-push.sh

## install with kube

### prerequirements
#### create namespace
kubectl apply -f k8s/namespace_otus.json
kubectl config set-context --current --namespace=otus


#### enable ingress
minikube addons enable ingress


### install db
helm install otus-hw-db bitnami/postgresql -f k8s/db/values.yaml

### install hello-app
kubectl apply -f k8s/hello-app


### install db
helm install otus-hw-db bitnami/postgresql -f https://github.com/krtvand/otus-hw-2/blob/master/k8s/db/values.yaml

### install hello-app
kubectl apply -f https://github.com/krtvand/otus-hw-2/tree/master/k8s/hello-app



