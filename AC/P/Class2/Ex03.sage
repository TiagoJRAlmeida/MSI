def entropy(probs):
    return -sum(p * log(p, 2) for p in probs if p > 0)

c_size = 2^8

# Question 1: p = 251
p = 251
probs = [2/c_size]*5 + [1/c_size]*(p-5)
H_251 = entropy(probs)
print("Entropy for p=251:", N(H_251))

# Question 2: p = 256 (uniform)
p = 256
probs_uniform = [1/c_size]*p
H_uniform = entropy(probs_uniform)
print("Entropy for p=256 (uniform):", N(H_uniform))