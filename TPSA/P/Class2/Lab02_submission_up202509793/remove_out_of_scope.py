import sys
import re

if len(sys.argv) != 3:
    print("ERROR: You must give 2 file arguments to compare!")
    print("Usage: python3 remove_out_of_scope.py <subs.txt> <out_of_scope.txt>")
    sys.exit(1)


allSubsFile = sys.argv[1]
outOfScopeFile = sys.argv[2]

with open(allSubsFile, "r") as f1:
    allSubs = set(f1.read().strip().split("\n"))

with open(outOfScopeFile, "r") as f2:
    outOfScopeSubs = set(f2.read().strip().split("\n"))

inScopeSubs = set([sub for sub in allSubs if sub not in outOfScopeSubs])

with open("subs_in_scope.txt", "w") as f:
    for sub in inScopeSubs:
        f.write(f"{sub}\n")