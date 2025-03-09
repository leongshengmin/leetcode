#!/bin/bash

set  -eoux pipefail


LOG_FILE="/var/log/kubernetes/kubeadm-init.log"

##################################
# Kubeadm init
##################################

if [[ -f /tmp/kubeadm-init.lock ]]; then
    echo "kubeadm-init is already running"
    echo "To re-run kubeadm-init, delete /tmp/kubeadm-init.lock"
    exit 1
fi

kubeadm_reset() {
    echo "Resetting kubeadm..."
    # reset kubeadm
    yes | kubeadm reset
}

kubeadm_init() {
    touch /tmp/kubeadm-init.lock
    echo "Initializing kubeadm..."
    # get IP of default gateway to use as apiserver-advertise-address
    apiserver_advertise_ip=$(ip route show | grep 'default via' | awk '{print $9}')
    pod_network_cidr="10.244.0.0/16"

    ##################################
    # Initialize control plane using kubeadm init
    ##################################
    mkdir -p /var/log/kubernetes && chmod 755 /var/log/kubernetes
    kubeadm init \
        --pod-network-cidr=${pod_network_cidr} \
        --apiserver-advertise-address=${apiserver_advertise_ip}

    # set kubectl config for ubuntu user
    cat <<EOF | >> /home/ubuntu/.bashrc
    mkdir -p /home/ubuntu/.kube
    sudo cp -i /etc/kubernetes/admin.conf /home/ubuntu/.kube/config
    sudo chown $(id -u):$(id -g) /home/ubuntu/.kube/config
EOF
    # set kubectl config for root user
    echo 'export KUBECONFIG=/etc/kubernetes/admin.conf' >> $HOME/.bashrc
    source $HOME/.bashrc

    # verify kubectl is working
    kubectl get nodes
    kubectl get pod -A  # coredns pods will be in pending state prior CNI setup

    ###################################
    # Install Networking CNI (Calico)
    # https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#pod-network
    # You must deploy a Container Network Interface (CNI) based Pod network add-on so that your Pods can communicate with each other. Cluster DNS (CoreDNS) will not start up before a network is installed.
    ###################################
    CALICO_VERSION=v3.29.2
    echo "Installing Calico networking ${CALICO_VERSION}..."
    # install tigera operator and custom resource definitions
    kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/${CALICO_VERSION}/manifests/tigera-operator.yaml
    # install calico custom resource definitions by creating the necessary CRDs
    curl https://raw.githubusercontent.com/projectcalico/calico/${CALICO_VERSION}/manifests/custom-resources.yaml -O
    sed -i "s|192.168.0.0/16|$pod_network_cidr|g" custom-resources.yaml
    kubectl create -f custom-resources.yaml
    # verify calico pods are running
    until kubectl get pods -n calico-system | grep Running; do
        echo "Waiting for calico pods to be running..."
        sleep 5
    done
    # remove taints on the control plane nodes for scheduling pods
    kubectl taint nodes --all node-role.kubernetes.io/control-plane-
    # verify control plane nodes are schedulable and pods are running normally
    kubectl get nodes -o wide
    kubectl get pod -A
}

reset=${1:-false}
if [[ "${reset}" == "true" ]]; then
    kubeadm_reset >> "${LOG_FILE}" 2>&1
    exit 0
fi
kubeadm_init >> "${LOG_FILE}" 2>&1
