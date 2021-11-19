

## Setup

### Setup cluster

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

Follow the instructions in [Istio documentation](https://istio.io/latest/docs/setup/platform-setup/kind/):

```bash
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.1.0/aio/deploy/recommended.yaml
$ kubectl create clusterrolebinding default-admin --clusterrole cluster-admin --serviceaccount=default:default
$ token=$(kubectl get secrets -o jsonpath="{.items[?(@.metadata.annotations['kubernetes\.io/service-account\.name']=='default')].data.token}"|base64 --decode)
$ kubectl proxy
```

Login to dashboard with the token: [http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/](http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/).