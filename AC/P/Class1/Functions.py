import string
import matplotlib.pyplot as plt

# Transforms any upper character in its "natural" order (𝐴→0,𝐵→1,…,𝑍→25).
def encodeOne(c):
    assert c in string.ascii_uppercase
    return ord(c)-ord('A')


# Encondes the string passed as argument so that instead of char, its a list 
# of numbers representative of each char.
def encode(w):
    return [encodeOne(i) for i in list(w)]


# Reverse of encondeOne. Transforms number into letter (in uppercase)
def decodeOne(n):
    assert 0 <= n < 26
    return chr(ord('A') + n)


# Reverse of encode. Receives a list of numbers as arg, transforms each one
# into the respective char and returns the string that is formed.
def decode(w):
    return "".join([decodeOne(n) for n in w])

# Uses the key as a "hash map" to transform the char c into another one,
# according to the key passed.
def cipherMonoOne(c, key):
    assert c in string.ascii_uppercase
    return key[ord(c) - ord('A')]


# Uses cipherMonoOne to cipher each char of the text and returns the encrypted text.
def cipherMono(w, key):
    return "".join([cipherMonoOne(c, key) for c in w])


def parcialCipherMonoOne(c, key):
    assert c in string.ascii_uppercase
    cipherC = key[ord(c) - ord('A')]
    return cipherC if cipherC != "0" else " "


def parcialCipherMono(w, key):
    return "".join([parcialCipherMonoOne(c, key) for c in w])


# Transforms a list of numbers into a string.
def back_from_number(lst):
    orda = ord('A')
    foo = [chr(orda+c-1) for c in lst]
    return "".join(foo)


def inverseKey(key):
    nk = [0 for _ in range(26)]
    l = 0
    for i in key:
        nk[encodeOne(i)] = chr(ord('A')+l)
        l += 1
    return "".join(nk)


def parcialInverseKey(key):
    nk = ["0" for _ in range(26)]
    l = 0
    for i in key:
        if i == "0":
            l += 1
            continue
        else:
            nk[encodeOne(i)] = chr(ord('A')+l)
            l += 1
    return "".join(nk)
    

def stats(text):
    assert len([True for c in text if c in string.ascii_uppercase]) == len(text)
    st = [0 for i in range(26)] # Initiates the list with twenty-six 0
    for c in text:
        st[encodeOne(c)] += 1
    l = sum(st)
    return [x for x in map(lambda x: float(x/l),st)]


def bar(title, sts):
    plt.figure(figsize = (26, 10))
    plt.bar([c for c in string.ascii_uppercase], sts, color ='Blue', width = 0.7)
    plt.title(title)
    plt.show(block=False)


def D(text, ref):
    p = stats(text)
    return sum([(ref[i]-p[i])**2 for i in range(26)])