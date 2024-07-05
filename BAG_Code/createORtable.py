import numpy as np
from itertools import product

def create_OR_table(probs, ONE = 0.999):
    if len(probs) == 0:
        return np.array([[1 - 0.99999, 0.99999]])
    else:
        npa = len(probs)
        q = 1 - np.array(probs)
        cpt = np.zeros((2, 2 ** npa))
        
        vals = list(product([0, 1], repeat=npa))
        
        for i in range(2 ** npa):
            c = [j for j, val in enumerate(vals[i]) if val == 1]
            tmp = np.prod(q[c])
            if tmp == 1:
                cpt[0, i] = ONE
            else:
                cpt[0, i] = tmp
        
        cpt[1, :] = 1 - cpt[0, :]
        
        return cpt.T

if __name__ == '__main__':
    # Example usage:
    probabilities = [0.3, 0.8]  # Example probabilities
    result_table = create_OR_table(probabilities)

    # Printing the resulting table
    print(result_table)