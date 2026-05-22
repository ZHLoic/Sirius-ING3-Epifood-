# Install K8S multimaster

## Sources
https://www.youtube.com/watch?v=6Gwg80eEuQk
https://github.com/frankisinfotech/k8s-HA-Multi-Master-Node


# install haproxy
```sh
sudo apt update && sudo apt install -y haproxy
```

Appliquer la conf ha dans le fichier /etc/haproxy/haproxy.cfg
```sh
sudo systemctl restart haproxy
sudo systemctl status haproxy
```

au cas pour tester avant d'appliquer
```sh
haproxy -c -f /etc/haproxy/haproxy.cfg
```

# Install packages machine K8S master ET worker
passer en root
```sh
sudo su -
```

Désactiver le swap
```sh
swapoff -a; sed -i '/swap/d' /etc/fstab
```

install Docker version 29.5.2
```sh
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu jammy stable" \
  > /etc/apt/sources.list.d/docker.list
apt update && apt install -y docker-ce docker-ce-cli containerd.io
```

install kubernetes version 1.35
```sh
# Clé GPG
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.35/deb/Release.key \
  | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

# Dépôt officiel
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] \
  https://pkgs.k8s.io/core:/stable:/v1.35/deb/ /" \
  > /etc/apt/sources.list.d/kubernetes.list

apt update

apt install -y kubelet kubeadm kubectl
apt-mark hold kubelet kubeadm kubectl  # empêche les mises à jour automatiques


# Générer la config par défaut
containerd config default > /etc/containerd/config.toml

# Activer SystemdCgroup (obligatoire avec kubeadm)
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

# Redémarrer containerd
systemctl restart containerd
```

faire un clone Vsphere de la VM pour faire le master 02 et les worker

# Setup


```sh
kubeadm init --control-plane-endpoint="<ip-LB>:6443" --upload-certs --apiserver-advertise-address=<ip-Master> --pod-network-cidr=192.168.0.0/16
```

après ca pour ajouter un noeud au cluster
```sh
# add master

kubeadm join 172.31.250.254:6443 --token nix4wf.npi2u8k1jw0uqj2z \
        --discovery-token-ca-cert-hash sha256:719e315d412aa1efcb0246275557ebd16f503dbba7d16990f0b5521eb17e9727 \
        --control-plane --certificate-key 44c765fedf0434bbd1e03424e478b67beac2dfa12f142dbfd448136cced245bf

# add worker
kubeadm join 172.31.250.254:6443 --token nix4wf.npi2u8k1jw0uqj2z \
        --discovery-token-ca-cert-hash sha256:719e315d412aa1efcb0246275557ebd16f503dbba7d16990f0b5521eb17e9727
```


# Acceder au cluster

copier la conf depuis une des machines dans /home/Adriend671/.kube/config
la coller dans le home du user désiré puis:
```sh
kubectl --kubeconfig=/home/Adriend671/.kube/config apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.31.5/manifests/calico.yaml
```