
## 1. Prerequisites

Install `multipass` which is a lightweight VM manager for managing Ubuntu VMs on your local machine.

```sh
brew install --cask multipass
```

## 2. K8s Control Plane VM

Launch an Ubuntu VM with 4GB of RAM and 2 CPUs meeting the minimum requirements for running a Kubernetes cluster using kubeadm.
```sh
multipass launch --name k8s-control-plane --cpus 2 --memory 2G --disk 4G 22.04 -v
```

Get IP of the VM
```sh
multipass list

Name                    State             IPv4             Image
k8s-control-plane       Running           192.168.64.2     Ubuntu 22.04 LTS
```

SCP the bootstrap script to the control plane VM and run it.
```sh
multipass transfer k8s/common/bootstrap.sh k8s-control-plane:/home/ubuntu/bootstrap.sh
multipass transfer k8s/control-plane/kubeadm-init.sh k8s-control-plane:/home/ubuntu/kubeadm-init.sh
multipass exec k8s-control-plane -- bash bootstrap.sh
multipass exec k8s-control-plane -- bash kubeadm-init.sh
```

SCP the kubeconfig file from the control plane VM to your local machine.
```sh
multipass transfer k8s-control-plane:/home/ubuntu/.kube/config ~/.kube/k8s-control-plane-admin.config
kubectl --kubeconfig ~/.kube/k8s-control-plane-admin.config get nodes
```

## 3. K8s Worker Node VM

Launch a worker node VM.
```sh
multipass launch --name k8s-worker-node --cpus 2 --memory 2G --disk 3G 22.04 -v
```

Get the kubeadm join command from the control plane VM.
```sh
export KUBEADM_JOIN_COMMAND=$(multipass exec k8s-control-plane -- bash grep "kubeadm join" /var/log/kubernetes/kubeadm-init.log)
echo ${KUBEADM_JOIN_COMMAND}
```

SCP the bootstrap script to the worker node VM and run it.
```sh
multipass transfer k8s/common/bootstrap.sh k8s-worker-node:/home/ubuntu/bootstrap.sh
multipass exec k8s-worker-node -- bash bootstrap.sh
```

Run the kubeadm join command on the worker node VM.
```sh
multipass exec k8s-worker-node -- bash -c "${KUBEADM_JOIN_COMMAND}"
```

Verify that the worker node is joined to the cluster.
```sh
kubectl --kubeconfig ~/.kube/k8s-control-plane-admin.config get nodes
```

## 4. Cleanup

Stop the VMs.
```sh
multipass stop k8s-control-plane && multipass delete k8s-control-plane && multipass purge
multipass stop k8s-worker-node
```

Networking modes CNI:
- https://www.redhat.com/en/blog/kubernetes-pods-communicate-nodes
- https://rendoaw.github.io/2017/10/Calico-and-Kubernetes-part-1
- https://joshrosso.com/c/calico-routing-modes/
