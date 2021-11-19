

# Kubeflow Pipelines

## Local setup

### Setup cluster with `kind`

[Install `kind`](https://kind.sigs.k8s.io/docs/user/quick-start/#installation):

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-darwin-amd64
chmod +x ./kind
mv ./kind ~/bin/kind
```

[Create cluster](https://kind.sigs.k8s.io/docs/user/quick-start/#creating-a-cluster):

```bash
$ kind create cluster --name kind
```

Switch `kubectl` context:

```bash
$ kubectl config use-context kind-kind
```

### Setup Kubernetes dashboard

> This step is optional.

Follow the instructions in [Istio documentation](https://istio.io/latest/docs/setup/platform-setup/kind/):

```bash
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.1.0/aio/deploy/recommended.yaml
$ kubectl create clusterrolebinding default-admin --clusterrole cluster-admin --serviceaccount=default:default
$ token=$(kubectl get secrets -o jsonpath="{.items[?(@.metadata.annotations['kubernetes\.io/service-account\.name']=='default')].data.token}"|base64 --decode)
$ kubectl proxy
```

Login to dashboard with the token: [http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/](http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/).

### Setup Kubeflow pipelines

Follow the instructions [here](https://www.kubeflow.org/docs/components/pipelines/installation/localcluster-deployment/) for deploying Kubeflow on `kind` cluster.

```bash
export PIPELINE_VERSION=1.7.1
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
```

Start Kubeflow Pipelines dashboard:

```bash
$ kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```

and navigate to [`http://localhost:8080`](http://localhost:8080).

### Delete Kubeflow

```bash
export PIPELINE_VERSION=1.7.1
kubectl delete -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"
kubectl delete -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
```
