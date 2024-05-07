# Rules for Mulval:
'Error in parsing trace_output.P' -> check if there is a space in each rule_description, don't use coma, pas d'accents non plus.
Tout doit être relié à une cause source, sinon les probabilités de branches locales ne sont pas prises en compte.

# Attack graphs
Bibliography for attack graphs latest updates https://www.sciencedirect.com/science/article/pii/S0167404823003206 
Or this one of 2020 by wilder https://www.sciencedirect.com/science/article/pii/S0167404822004734
https://ieeexplore.ieee.org/document/9763050 III C sur la Posterior Probability Calculation
On probability of a CVE exploit https://www.first.org/epss/
CVE used by threat actors but very old with very few vulnerabilities : https://dl.acm.org/doi/fullHtml/10.1145/3465481.3465758
Microsoft will now use CWE is CVE publications https://www.cve.org/Media/News/item/news/2024/04/23/Microsoft-CWE-Root-Cause-Mapping-CVEs and it is already on NVD
Use of the CWE tree to establish corelations https://ieeexplore.ieee.org/document/10172785 . They map commits to CWE thanks to the tree
Sur le même sujet : https://ieeexplore.ieee.org/document/8330232 build another graph if we want to improve compared to CWE 1000
The italien CSIRT made a classification of the most related CVE exploits thanks to TTP, which corresponds to the techniques that the attacker is able to do. https://www.csirt.gov.it/contenuti/analisi-delle-principali-vulnerabilita-sfruttate-in-campagne-cyber-pubblicamente-attribuite-ad-attori-di-matrice-russa-e-relative-mitigazioni-al01-220512-csirt-ita

Attacker skills : https://www.mdpi.com/2078-2489/11/11/537 Evaluation of Attackers’ Skill Levels in Multi-Stage Attacks
Evaluation of Attackers' Skill Levels in Multi-Stage Attacks: https://www.webofscience.com/wos/woscc/full-record/WOS:000593363600001
Evaluation of Attacker Skill Level for Multi-stage Attacks: https://www.webofscience.com/wos/woscc/full-record/WOS:000569985400161
Peut-etre util pour réfléchir à l'integration de 0-day https://scholar.google.com/scholar_lookup?title=Fighting+N-day+vulnerabilities+with+automated+CVSS+vector+prediction+at+disclosure&conference=Proceedings+of+the+15th+International+Conference+on+Availability,+Reliability+and+Security&author=Elbaz,+C.&author=Rilling,+L.&author=Morin,+C.&publication_year=2020&pages=1%E2%80%9310
Incorporating attacker capabilities in risk estimation and mitigation: https://doi.org/10.1016/j.cose.2015.03.001
Attacker-parametrised attack graphs (ils font du profilage avant l'attaque mais pas pendant. Ils definissent un set de capabilities puis font toutes les combinaisons de capabilities et construisent tous les graphs possibles): https://ora.ox.ac.uk/objects/uuid:b156c235-d097-4ba4-bd5a-927833f02ea0
Towards modelling adaptive attacker’s behaviour: https://link.springer.com/chapter/10.1007/978-3-642-37119-6_23
A probabilistic study on the relationship of deceptions and attacker skills: https://ieeexplore.ieee.org/abstract/document/8328465

## Exactly what I a, supposed to do:
Concept for real time attacker profiling with honeypots, by skill based attacker maturity model: https://ieeexplore.ieee.org/document/10432876
 - objectif: utiliser les honeypots pour du real-time
 - différences par rapport à ce que je veux faire : les honeypots sont statics, principalement à l'entrée et pas propre à l'AD
 - en vrai je ne comprends pas ce qu'ils apportent 
Real-time processing of cybersecurity system data for attacker profiling (Profiling basé sur 7 clusters et de l'apprentissage): https://ieeexplore.ieee.org/document/9119254
Concept for real time attacker profiling with honeypots, by skill based attacker maturity model: https://jit.ndhu.edu.tw/article/view/1777/1783

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

