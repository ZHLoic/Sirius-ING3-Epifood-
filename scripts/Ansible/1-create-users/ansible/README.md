Executer le script run pour deployer les clés des utilisateurs listé dans users.conf dans toutes les vms de l'infra
Si un utilisateur n'as pas de profil github mettre sa clé dans le repertoire files

source :
    - pour ansible :https://youtu.be/pHeZ8UlAQ_8?si=U0IKC6RoveOpXAAe      -->     https://gitlab.com/xavki/raspberry-tricks
    - partie sh a la mano


pour exec le playbook sur une parite deulement de l'inventaire:
```ssh
ansible-playbook -i list_servers.yml -u epifood -k -K -b users.yml -l '<groupe|host|expression>'
```

exemple
```ssh
#prendre que K8S
ansible-playbook -i list_servers.yml -u epifood -k -K -b users.yml -l 'K8S'

#prendre ce qui est dans NCC mais pas ces fils
ansible-playbook -i list_servers.yml -u epifood -k -K -b users.yml -l 'NCC:!K8S:!PG:!HA'
```