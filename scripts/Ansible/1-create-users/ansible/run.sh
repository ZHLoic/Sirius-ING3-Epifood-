#!/bin/bash

# gather ssh public keys from github profile
# no args
# one conf file store username

echo récupération des clé

USERS_TO_FETCH=users.conf # end the file with an empty line

if [ ! -f $USERS_TO_FETCH ]; then
  echo Erreur : user file unreacheable
  exit 1
fi

dos2unix $USERS_TO_FETCH

# refresh pub keys
while IFS= read -r PEOPLES; do
  FILES=files/$PEOPLES.key.pub

  if [ -f $FILES ]; then
    echo file found : $PEOPLES
    echo delete then wget
    rm $FILES
  else
    echo download : $PEOPLES
  fi
  wget -O $FILES https://github.com/$PEOPLES.keys
done < $USERS_TO_FETCH

echo keys retrieved succesfully
echo Now it's Ansible's turn :
echo ''
ansible-inventory -i list_servers.yml --graph

echo 'help for the question underneath : <groupe|host|expression>
exemple :
  - all
  - K8S
  - NCC:!K8S:!PG:!HA'

read -p 'Which group should be affected among those :' group

echo ''
echo ''
echo ''
read -p 'Upgrade all packages ? (y/n) : ' upgrade

EXTRA_VARS=""
if [[ "$upgrade" == "y" || "$upgrade" == "Y" ]]; then
    EXTRA_VARS="-e upgrade_packages=true"
    echo "Package upgrade enabled"
else
    echo "Package upgrade skipped"
fi

ansible-playbook -i list_servers.yml -u epifood -k -K -b users.yml -l "$group" $EXTRA_VARS
