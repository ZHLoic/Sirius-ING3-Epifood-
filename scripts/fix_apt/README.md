apt marche plus dans certaines machines.
Pour réparer ca si le service fwupd-refresh est en erreur
si quand sudo apt update on a :
sudo apt update
Get:1 file:/cdrom jammy InRelease
Ign:1 file:/cdrom jammy InRelease
Get:2 file:/cdrom jammy Release
Err:2 file:/cdrom jammy Release
  File not found - /cdrom/dists/jammy/Release (2: No such file or directory)
Hit:3 http://archive.ubuntu.com/ubuntu jammy InRelease
Hit:4 http://archive.ubuntu.com/ubuntu jammy-updates InRelease
Hit:5 http://archive.ubuntu.com/ubuntu jammy-backports InRelease
Hit:6 http://archive.ubuntu.com/ubuntu jammy-security InRelease
Reading package lists... Done
E: The repository 'file:/cdrom jammy Release' no longer has a Release file.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.

alors :
sudo vim /etc/apt/sources.list
commenter la ligne deb [check-date=no] file:///cdrom jammy main restricted

jusqu'ici le problème est survenu sur les vm:
- apache airflow
- idp

Ces deux VM ont eu auparavant une collision d'ip (meme machine-id le dhcp qui panique puis aucune vm a du reseau), mais tout à été fix.

Résultat: TODO script qui va supprimer ou commenter la ligne en question dans une vm bien particulière