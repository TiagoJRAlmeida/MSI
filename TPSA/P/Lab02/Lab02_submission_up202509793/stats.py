import sys
import re

if len(sys.argv) != 3:
    print("ERROR: You must give 2 file arguments to compare!")
    print("Usage: python3 stats.py <file1.txt> <file2.txt>")
    sys.exit(1)


fileName1 = sys.argv[1]
fileName2 = sys.argv[2]

with open(fileName1, "r") as f1:
    subs1 = set(f1.read().strip().split("\n"))

with open(fileName2, "r") as f2:
    subs2 = set(f2.read().strip().split("\n"))

print('''
====================================
|              STATS               |
====================================
''')

print("- Number of subdomains found")
print("    ", fileName1, ": ", len(subs1))
print("    ", fileName2, ": ", len(subs2))

commonSubs = set()
file1Exclusives = set()
file2Exclusives = set()
invalidCommonSubs = 0
invalidFile1Subs = 0
invalidFile2Subs = 0
allSubs = subs1.union(subs2)

for sub in allSubs:
    if (sub in subs1) and (sub in subs2):
        commonSubs.add(sub)
        invalidCommonSubs += 1 if not re.search(r'chime.com', sub) else invalidCommonSubs
    elif sub in subs1:
        file1Exclusives.add(sub)
        invalidFile1Subs += 1 if not re.search(r'chime.com', sub) else invalidFile1Subs
    elif sub in subs2:
        file2Exclusives.add(sub)
        invalidFile2Subs += 1 if not re.search(r'chime.com', sub) else invalidFile2Subs
    else:
        print("\nERROR: Subdomain ", sub, " not found in either file!")

print("\n- Number of subdomains found")
print("     By both tools : ", len(commonSubs))
print("     By just", fileName1, ": ", len(file1Exclusives))
print("     By just", fileName2, ": ", len(file2Exclusives))

print("\n- Number of INVALID subdomains found (no <chime.com>)")
print("     By both tools : ", invalidCommonSubs)
print("     By just", fileName1, ": ", invalidFile1Subs)
print("     By just", fileName2, ": ", invalidFile2Subs)
print("\n====================================\n")


# Uncomment the following lines to get some data when necessary

print("Common Subdomains: \n")
print(commonSubs)

print("\n\n====================================\n")

print("Unique subdomains to", fileName1, ": \n")
print(file1Exclusives)

print("\n\n====================================\n")

print("Unique subdomains to", fileName2, ": \n")
print(file2Exclusives)

print("\n====================================\n")
sys.exit(0)