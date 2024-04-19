# Rules for Mulval:
'Error in parsing trace_output.P' -> check if there is a space in each rule_description, don't use coma, pas d'accents non plu.

#GOAT
## Architecture du lab :
Installation classique de GOAD
Installation d'une machine kali linux pour pouvoir faire les exploits sans être en permanence avec mes privilèges root sur la machine Ubuntu du serveur.
Connection à la machine kali avec la commande 'vagrant ssh' depuis le dossier '/data/${USER}/DossierKali' 
Ajout d'un pont pour rediriger les paquets entre kali et le réseau de GOAT 
'ip route add 192.168.56.0/24 via <ip-of-your-ubuntu>'
-> semble non nécéssaire finalement.


## Outils pour les attaques :
https://github.com/fortra/impacket
crackmapexec with 'alias cme='crackmapexec''
