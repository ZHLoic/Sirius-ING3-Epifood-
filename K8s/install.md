# Sources
https://www.youtube.com/watch?v=vX2n05t0AQg&t=167s
https://docs.docker.com/engine/install/ubuntu/

# Adresse 
master1 :172.31.252.172

# Setup système
## MàJ paquet
```sh 
sudo apt update && sudo apt upgrade
sudo apt dist-upgrade
```

## Install services
```sh 
sudo apt install -y apt-transport-https gnupg ca-certificates curl software-properties-common inetutils-traceroute
```

suppr package au cas ou truc bizarre
```sh 
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```
## Install docker
https://docs.docker.com/engine/install/ubuntu/
### Add Docker's official GPG key:
```sh
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

### Add the repository to Apt sources:
```sh 
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update

sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

## User docker
```sh 
sudo usermod -aG docker $USER
```

## Param special K8s
```sh 
sudo swapoff -a
```

Dans le fichier /etc/fstab commenter la ligne
```sh 
/swap.img
```

```sh 
sudo modprobe overlay
sudo modprobe br_netfilter
```

Dans le fichier /etc/modules-load.d/k8s.conf coller:
```sh 
overlay
br_netfilter
```
Dans le fichier /etc/sysctl.d/k8s.conf coller:
```sh 
net.ipv4.ip_forward=1
```

vérifier que net.ipv4.ip_forward = 1 avec
```sh
sudo sysctl --system
```

```sh
sudo containerd config default | sudo tee /etc/containerd/config.toml>/dev/null 2>&1
cd /etc/containerd
```

Dans le fichier /etc/containerd/config.toml modifier SystemdCgroup = false en :
```sh
SystemdCgroup = true
```

```sh
sudo systemctl status containerd
sudo systemctl restart containerd
sudo systemctl status containerd
```

https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
```sh
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.35/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
sudo chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg # allow unprivileged APT programs to read this keyring

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.35/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt update
sudo apt-get install kubelet kubeadm kubectl -y 
sudo apt-mark hold kubelet kubeadm kubectl
```

```sh
shutdown now
```
faire le template