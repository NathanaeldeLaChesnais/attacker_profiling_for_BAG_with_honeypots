class Noeud:
    def __init__(self, valeur):
        self.valeur = valeur
        self.enfants = []

    def ajouter_enfant(self, enfant):
        self.enfants.append(enfant)

    def __str__(self):
        if self.enfants:
            return f"({self.valeur} {' '.join(str(enfant) for enfant in self.enfants)})"
        else:
            return f"{self.valeur}"

def construire_arbre(expression):
    noeud_actuel = None
    pile_parents = []
    mots = expression.split()
    print(mots)
    parent = Noeud('parent')

    for mot in mots:
        if mot == '(':
            print('parent:', parent)
            if parent:
                pile_parents.append(parent)
            parent = Noeud('parent')
        elif mot == ')':
            parent = pile_parents.pop()
        elif mot in ('&', '|'):
            parent.valeur = mot
        else:
            enfant = Noeud(mot)
            parent.ajouter_enfant(enfant)
            print('enfant:', enfant)

    return parent

def afficher_arbre(noeud, niveau=0):
    if noeud:
        print("  " * niveau + str(noeud))
        for enfant in noeud.enfants:
            afficher_arbre(enfant, niveau + 1)

expression = "Responder & ( impacket | Metasploit )"
arbre = construire_arbre(expression)
print("Arbre de l'expression:", expression)
print(afficher_arbre(arbre))
