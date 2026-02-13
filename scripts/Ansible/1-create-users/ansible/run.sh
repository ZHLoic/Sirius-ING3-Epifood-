#!/bin/bash

## Create and maintain users for Raspberry

echo récupération des clé

#!/bin/bash
# gather ssh public keys from github profile
# no args
# one conf file store username
users_to_fetch=users.conf # end the file with an empty line
machines_to_fetch=machines.conf
if [ ! -f $users_to_fetch ]; then
  echo Erreur : fichier introuvable
  exit 1
fi

dos2unix $users_to_fetch

# refresh pub keys
while IFS= read -r people; do
  fichier=files/$people.key.pub

  if [ -f $fichier ]; then
    echo file found : $people
    echo delete then wget
    rm $fichier
  else
    echo download : $people
  fi
  wget -O $fichier https://github.com/$people.keys
done < $users_to_fetch

echo fin de la récupération des clé
echo déploiement des clé

ansible-playbook -i list_servers.yml -u epifood -k -K -b users.yml
