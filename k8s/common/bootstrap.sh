#!/bin/bash

set -eoux pipefail


LOG_DIR=/var/log/kubernetes
LOG_FILE="${LOG_DIR}/bootstrap.log"
sudo mkdir -p -m 755 "${LOG_DIR}" && sudo chown ubuntu:ubuntu "${LOG_DIR}"

bootstrap() {
  # disable swap
  swapoff -a

  ##################################
  # Install container runtime
  ##################################
  echo "Installing container runtime..."
  # enable ipv4 packet forwarding
  # sysctl params required by setup, params persist across reboots
  cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
  net.ipv4.ip_forward = 1
EOF

  # Apply sysctl params without reboot
  sudo sysctl --system

  # verify net.ipv4.ip_forward is 1
  sysctl net.ipv4.ip_forward

  # install containerd
  sudo apt-get update
  sudo apt-get install -y ca-certificates curl gnupg
  sudo install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --yes --dearmor -o /etc/apt/keyrings/docker.gpg
  sudo chmod a+r /etc/apt/keyrings/docker.gpg
  echo \
    "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update
  sudo apt-get install -y containerd.io

  # Configure cgroup drivers
  # since ubuntu is using systemd, we need to configure containerd to use the same systemd cgroup driver
  # by setting SystemdCgroup = true
  # https://kubernetes.io/docs/setup/production-environment/container-runtimes/#systemd-cgroup-driver
  cat <<EOF | sudo tee /etc/containerd/config.toml
  version = 2
  [plugins]
    [plugins."io.containerd.grpc.v1.cri"]
    [plugins."io.containerd.grpc.v1.cri".containerd]
        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
          [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
            runtime_type = "io.containerd.runc.v2"
            [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
              SystemdCgroup = true
EOF
  # Ensure cri is not included in the disabled_plugins list within /etc/containerd/config.toml
  sed -i 's/disabled_plugins = \[\"cri\"\]/\#disabled_plugins \= \[\"cri\"\]/g'  /etc/containerd/config.toml
  # restart containerd after config change
  sudo systemctl restart containerd

  ##################################
  # Configure crictl used for troubleshooting container runtime (containerd-specific config)
  # https://kubernetes.io/docs/tasks/debug/debug-cluster/crictl/
  ##################################
  echo "Installing crictl..."
  CRICTL_VERSION=v1.32.0
  ARCHITECTURE=$(dpkg --print-architecture)
  wget https://github.com/kubernetes-sigs/cri-tools/releases/download/${CRICTL_VERSION}/crictl-${CRICTL_VERSION}-linux-${ARCHITECTURE}.tar.gz
  tar -xvf crictl-${CRICTL_VERSION}-linux-${ARCHITECTURE}.tar.gz
  sudo install -o root -g root -m 0755 crictl /usr/local/bin/
  rm -f crictl-${CRICTL_VERSION}-linux-${ARCHITECTURE}.tar.gz

  # configure crictl to use containerd
  echo "Configuring crictl for container runtime debugging..."
  crictl config runtime-endpoint unix:///var/run/containerd/containerd.sock

  ##################################
  # Install kubeadm, kubelet, kubectl
  #
  # kubeadm: the command to bootstrap the cluster
  # kubelet: the component that runs on all of the machines in your cluster and does things like starting pods and containers
  # kubectl: the command line util to talk to your cluster
  # https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#installing-kubeadm-kubelet-and-kubectl
  ##################################
  KUBERNETES_VERSION=v1.32
  echo "Installing kubeadm, kubelet, kubectl ${KUBERNETES_VERSION}..."

  # Kubernetes v1.32 specific install
  # Update apt package index and install pkgs needed to use the k8s apt repository
  mkdir -p -m 755 /etc/apt/keyrings
  sudo apt-get update && \
      sudo apt-get install -y apt-transport-https ca-certificates curl gpg

  # Download the public signing key for the k8s package repositories
  curl -fsSL https://pkgs.k8s.io/core:/stable:/${KUBERNETES_VERSION}/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

  # Add the appropriate k8s apt repo
  # This overwrites any existing configuration in /etc/apt/sources.list.d/kubernetes.list
  echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/${KUBERNETES_VERSION}/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list

  # Update apt package index, install kubelet, kubeadm and kubectl, and pin their version
  sudo apt-get update && \
      sudo apt-get install -y kubelet kubeadm kubectl && \
      sudo apt-mark hold kubelet kubeadm kubectl

  # Enable the kubelet service before running kubeadm init
  sudo systemctl enable --now kubelet

  ##################################
  # Configure bash
  ##################################
  echo -e "Configure bash..."
  echo "source <(kubectl completion bash)" >> /home/ubuntu/.bashrc

  echo -e "Setup has been completed."

  # Version info
  echo -e "\n- containerd:"
  containerd -v

  echo -e "\n- runc:"
  runc --version

  echo -e "\n- crictl:"
  crictl -v

  echo -e "\n- kubectl:"
  kubectl version --client=true

  echo -e "\n- kubelet:"
  kubelet --version

  echo -e "\n- kubeadm:"
  kubeadm version
}

bootstrap >> "${LOG_FILE}" 2>&1
