# Rules for Mulval:
'Error in parsing trace_output.P' -> check if there is a space in each rule_description, don't use coma, pas d'accents non plus.
Tout doit être relié à une cause source, sinon les probabilités de branches locales ne sont pas prises en compte.

# GOAT
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

## Changes to do in the exploits
The attacks done in this project are all from https://mayfly277.github.io/categories/ad/ 
Some of them are not perfect for my configuration, here are the changes I had to do.
### part 5
Clear the SPNs of our new computer (with dirkjan krbrelayx tool addspn) : bien utiliser https://github.com/dirkjanm/krbrelayx pour addspn.py
The file renamemachine.py can be fount here : https://github.com/ShutdownRepo/impacket/blob/CVE-2021-42278/examples/renameMachine.py
'Reset the computer name back to the original name' : replace samaccount$ by samaccountname$

