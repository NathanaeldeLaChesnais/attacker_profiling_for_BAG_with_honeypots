import numpy as np
from itertools import product

def create_AND_table(probs):
    if len(probs) == 0:
        return np.array([[0, 1]])
    else:
        npa = len(probs)
        pop = np.full(npa, 0.01)
        q = np.array(probs)
        cpt = np.zeros((2, 2 ** npa))
        
        vals = list(product([0, 1], repeat=npa))
        
        for i in range(2 ** npa):
            c = [j for j, val in enumerate(vals[i]) if val == 1]
            c_prime = [j for j, val in enumerate(vals[i]) if val == 0]
            tmp = np.prod(q[c]) * np.prod(pop[c_prime])
            cpt[1, i] = tmp
        
        cpt[0, :] = 1 - cpt[1, :]
        
        return cpt.T

if __name__ == '__main__':
    # Example usage:
    probabilities = [0.7, 0.8, 0.6]  # Example probabilities
    result_table = create_AND_table(probabilities)

    # Printing the resulting table
    print(result_table)