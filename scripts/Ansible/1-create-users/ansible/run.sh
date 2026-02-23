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

ansible-playbook -i list_servers.yml -u epifood -k -K -b users.yml