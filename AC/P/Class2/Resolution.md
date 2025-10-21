# AC Lab02 - Resolution

## Ex01

- Set S = {0, 1, ..., 250}
- Prime number *p* = 251
- Set C = {00000000, 00000001, ..., 11111111} = {0, 1, ..., 251, 252, 253, 254, 255}
- Function D(C) := C (mod *p*)
- D produces the values {0, 1, ..., 250, 0, 1, 2, 3, 4}

---

### Calculate the probability of each value in S to be produced by D.

- D produces 256 different numbers. len(D) = 256. 
- The values of S {0, 1, 2, 3, 4} have the probability of 2/256 ~= 0.008, while the other valus have a probability of 1/256 ~= 0.004.


### Repeat the above considering now the set C to be the set of all bit strings of length 64

- New Set C = (0, 1, ..., 2**(64) - 1)
- $2^{64}$ mod 251 = 69
- $\frac{2^{64} - 69}{251} = 73493004277727297$ 
- Distribution D = (0, 1, ..., 250, 0, 1, 2, 3, 4, ..., 68)
- len(D) = $2^{64}$

The values (0, 1, ..., 68) from S have the probability:
$$
Prob_1 = \frac{73493004277727297 + 1}{2^{64}} \approx 0.004
$$

The rest of the values (69, 70, ..., 250) from S have the probability:
$$
Prob_2 = \frac{73493004277727297}{2^{64}} \approx 0.004
$$


### Are these distributions uniform? If not, can you think of a way to quantify how distant they are from uniform?

- Neither of the distributions are uniform, because not all the values they create have the same probability.   
- Lets quantify how distant which one was from uniform.

---

- **For the first case**, the distribution would be uniform if C = (0, 1, ..., 250), and len(C) = 251
- That way, all of the values would have probability 1/251 ~= 0.004, and the entropy would be:
$$
H(U) = -\frac{1}{251} \log_2(\frac{1}{251}) \times 251 = -\log_2(\frac{1}{251}) = \log_2(251) \approx 7.97 bits
$$

- The original entropy was: 
$$
H(D) = -\frac{2}{256}\log_2(\frac{2}{256}) \times 5 + -\frac{1}{256}\log_2(\frac{1}{256}) \times 246 \approx 7.96 bits
$$

- How far is it from the uniform distribution? 
$$
|H(U) - H(D)| \approx 0.0106 bits
$$

--- 

- **For the second case**, the distribution would be uniform if C = (0, 1, ..., 250), and len(C) = $2^{64} - 69 = 18446744073709551547$.
- $\frac{2^{64} - 69}{251} = 73493004277727297$ <--- Number of times each value appears in the distribution.
- That way, all of the values would have probability:
$$
Prob = \frac{\frac{2^{64} - 69}{251}}{2^{64} - 69} = \frac{73493004277727297}{18446744073709551547} = \frac{1}{251} \approx 0.004
$$

- The entropy would be:
$$
H(U) = (-\frac{1}{251} \cdot \log_2(\frac{1}{251})) \times 251 = log_2(251) \approx 5.86 \approx 7.97 bits
$$

- The original entropy was:
$$ 
H(D) = -\frac{73493004277727297 + 1}{2^{64}} \cdot \log_2(\frac{73493004277727297 + 1}{2^{64}}) \times 69 - \frac{73493004277727297}{2^{64}} \cdot \log_2(\frac{73493004277727297}{2^{64}}) \times (251 - 69) \approx 7.97 bits
$$

- How far is it from the uniform distribution? 
$$
|H(U) - H(D)| \approx 1.0 \times 10^{-13}
$$

---

- **Conclusion:** The second case (64 bits case) is a lot closer to being an uniform distribution than the first one (8 bits case).

---

## Ex02

### Repeat question #1 but take p = $2^8$, i.e., a power of 2

- Set S = {0, 1, ..., 250}
- Prime number $p = 2^8 = 256$
- Set C = {00000000, 00000001, ..., 11111111} = {0, 1, ..., 251, 252, 253, 254, 255}
- Function D(C) := C (mod *p*)

---
 
#### Calculate the probability of each value in S to be produced by D.

- D produces 256 different numbers. len(D) = 256. 
- Every value of S appears only once on the distribution D, so all of the values have the same probability.
- $Pr[S=s] = \frac{1}{256} \approx 0.004$


#### Repeat the above considering now the set C to be the set of all bit strings of length 64

- New Set C = (0, 1, ..., $2^{64}$ - 1)
- $2^{64} mod 256 = 0$
- Number of times each value appears $= \frac{2^{64}}{2^{8}} = 2^{56}$ 
- Distribution D = (0, 1, ..., 255)
- len(D) = $2^{64}$

- Every value of S appear $2^{56}$ times on the distribution D, so all of the values have the same probability.
- $Pr[S=s] = \frac{2^{56}}{2^{64}} = \frac{1}{2^8} = \frac{1}{256} \approx 0.004$


#### Are these distributions uniform? If not, can you think of a way to quantify how distant they are from uniform?

Yes, these distributions are uniform because all of the values they create appear the same number of times which means all values have the same probability. 

---

## Ex03

Solved on the file `Ex03.sage`. Can be run in https://sagecell.sagemath.org/

**Output:**

```
Entropy for p=251: 7.96093750000000
Entropy for p=256 (uniform): 8.00000000000000
```

---

## Ex04