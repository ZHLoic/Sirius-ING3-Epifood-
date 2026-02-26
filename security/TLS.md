# Configuration TLS
Contexte : Les communications TLS (https) ont été configurées UNIQUEMENT entre le Front Client et le Reverse Proxy grâce à un certificat auto-signé sur la VM du RP.
Le reste des communications, celles qui sont internes au système, sont toujours en http.

## VMs
VM Front -> IP : 172.31.250.120 \
VM Reverse Proxy (Nginx) -> IP : 172.31.252.204

## Scénarios de Test
### Configuration du port d'écoute de nginx
Commande à taper sur la VM Reverse Proxy :

*sudo ss -tulpn | grep :443*

-> Nginx doit bien écouter ce port

### Vérification du Certificat TLS
Commande à taper sur la VM Reverse Proxy : 

*openssl s_client -connect 172.31.252.204:443*

-> Affichage du certificat avec les protocoles TLS

### Tester Https avec curl
Commande à taper sur la VM Reverse Proxy :

*curl -vk https://172.31.252.204*

-> Affichage de la page de connexion (Redirection Front)