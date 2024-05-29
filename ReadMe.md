# Rules for Mulval:
'Error in parsing trace_output.P' -> check if there is a space in each rule_description, don't use coma, pas d'accents non plus.
Tout doit être relié à une cause source, sinon les probabilités de branches locales ne sont pas prises en compte.

# Attack graphs
## Packet attacks on mulval
Extending Attack Graphs to Represent Cyber-Attacks in Communication Protocols and Modern IT Networks https://ieeexplore.ieee.org/document/9277665

## Honeypots on AAD or honeytockens
Proposing and Deployment of Attractive Azure AD Honeypot With Varying Security Measures To Evaluate Their Performance Against Real Attacks https://essay.utwente.nl/85992/1/Khan_MA_faculty.pdf
Honey Infiltrator: Injecting Honeytoken Using Netfilter https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10190694&tag=1

## Decoys 
Resource-aware Cyber Deception for Microservice-based Applications (Une des premieres ressources d'Emil - uses a legacy cloned version of a service so that it is realistic and with vulnerabilities - optimisation of the positions of the decoys due to the probability that an attacker go throught (prend-il en compte le fait que le but soit que l'attacker passe par 1 et pas par un maximum ?)) https://arxiv.org/pdf/2303.03151
Deception Maze: A Stackelberg Game-Theoretic Defense Mechanism for Intranet Threats (à regarder plus en détails mais réfléchit à une façon optimale de mettre des honeytockens credentials sur des hosts pour que l'attackant finisse dans le honeypot) https://ieeexplore.ieee.org/document/9500765


## Others 
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

## Exactly what I am supposed to do:
Concept for real time attacker profiling with honeypots, by skill based attacker maturity model: https://ieeexplore.ieee.org/document/10432876
 - objectif: utiliser les honeypots pour du real-time
 - différences par rapport à ce que je veux faire : les honeypots sont statics, principalement à l'entrée et pas propre à l'AD
 - en vrai je ne comprends pas ce qu'ils apportent
 - ils font une classification statique et des honeypots vraiment génériques 

Real-time processing of cybersecurity system data for attacker profiling (Profiling basé sur 7 clusters et de l'apprentissage): https://ieeexplore.ieee.org/document/9119254

Concept for real time attacker profiling with honeypots, by skill based attacker maturity model: https://jit.ndhu.edu.tw/article/view/1777/1783

## Honeypots:
Approaches for Preventing Honeypot Detection and Compromise (avoir une known vulnerability shows that it is a honeypot, en revanche présentes différentes techniques de randomness qui le rendent moins détectable): https://ieeexplore.ieee.org/document/8635603

HoneyTrack: An improved honeypot(Ils renvoient tout le trafic annormal vers une voie de sortie différente, mais c'est implémenté au niveau du firewall : est-ce que c'est possible de récupérer toutes les actions du hacker et que ses packets soient traités differement ?): https://ieeexplore.ieee.org/document/10063105

Engaging Attackers with a Highly Interactive Honeypot System Using ChatGPT(The proposed approach involves using ChatGPT, a large language model, to create a highly interactive honeypot that engages attackers in conversations and tricks them into revealing their tactics and motives. Peut-etre simuler des humains dans les compôrtements de bots avec de l'IA générative ? En vrai je pense plus simple de faire un truc de l'ordre du random bien calibré): https://ieeexplore.ieee.org/document/10392228

Honeypot-based intrusion detection system: A performance analysis(Encore une fois, c'est basé sur une redirection générale de tous les paquets du hacker sur le honeynet): https://ieeexplore.ieee.org/document/7724682

Deceptive directories and “vulnerable” logs: a honeypot study of the LDAP and log4j attack landscape (Vraiment orienté LDAP): https://ieeexplore.ieee.org/document/9799363

## Windows on mulval
Windows Access Control Demystified (s'interresse plus particulièrement aux accès sur une machine windows à partir de mulval) : https://www.cs.princeton.edu/~appel/papers/winval.pdf 
Automatic Configuration Vulnerability Analysis (encore sur windows mais s'étend aux logiciels installés) https://www.cs.princeton.edu/techreports/2007/773.pdf

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
The file renamemachine.py can be found here : https://github.com/ShutdownRepo/impacket/blob/CVE-2021-42278/examples/renameMachine.py
'Reset the computer name back to the original name' : replace samaccount$ by samaccountname$

