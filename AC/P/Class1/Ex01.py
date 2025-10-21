from Functions import *
import importlib
import re 


def ngram_count(text, ngram):
    count = 0
    for i in range(len(text) - len(ngram) + 1):
        if text[i:i+len(ngram)] == ngram:
            count += 1
    return count


def new_section():
    print("\n" + "="*50 + "\n")

groupNumber = 16
fName = "work"+str(groupNumber)
work = importlib.import_module(fName, package=None)

eStats = [0.0827031042166906, 0.0162276080084299, 0.0304341066523865, 0.0375304461987597, 0.122672701204028, 0.0212717442001071, 0.0213201126293424, 0.0502686175266458, 0.0748777833439859, 0.00192437250600287, 0.00767676069719636, 0.0423189206930505, 0.0274732678056280, 0.0709564856881273, 0.0748432344659607, 0.0196341273817133, 0.00130594758935204, 0.0634870182590820, 0.0662509285010969, 0.0866554958627719, 0.0301577156281850, 0.0101919190174299, 0.0179861458999119, 0.00233550415450258, 0.0183247249045587, 0.00117120696505381]

cText = back_from_number(work.msg1)
new_section()
print("This is the encrypted text we need to decrypt: \n")
print(cText)
new_section()

print("From the analysis of the plots of the <English Language stats> and the <Cypher Text stats>, we can make some assumptions:\n" \
"\t1. In the english language, E is the most commun letter. In the cypher text, N appears way more than any other letter, so we can make a guess that E was substituted by N\n" \
"\t\t- (E --> N)\n" \
"\t2. In the english language, T is the second most common. In the cypher text, the second most common letter is Q, however R is very close.\n" \
"\t   That means either (T --> Q) or (T --> R) could be the original substitution used.\n" \
"\t3. What to do next? Test each combination and decide which one makes more sense based on the bigrams (TE or ET) it creates. \n" \
"NOTE: In english, according to the bigram TE is sligtly more common than ET")
new_section()


print("Test 1: (E --> N) and (T --> Q) substitution combination")
#              ABCDEFGHIJKLMNOPQRSTUVWXYZ
originalKey = "0000N00000000000000Q000000"
iKey = parcialInverseKey(originalKey) 
dText = parcialCipherMono(cText, iKey) 
TECount = ngram_count(dText, "TE")
ETCount = ngram_count(dText, "ET") 
print("Number of bigram <TE>: ", TECount)
print("Number of bigram <ET>: ", ETCount)
print("Is the number of <TE> bigger than <ET>? R.: ", "yes" if TECount > ETCount else "no")
new_section()


print("Test 2: (E --> N) and (T --> R) substitution combination")
#              ABCDEFGHIJKLMNOPQRSTUVWXYZ
originalKey = "0000N00000000000000R000000"
iKey = parcialInverseKey(originalKey) 
dText = parcialCipherMono(cText, iKey) 
TECount = ngram_count(dText, "TE")
ETCount = ngram_count(dText, "ET") 
print("Number of bigram <TE>: ", TECount)
print("Number of bigram <ET>: ", ETCount)
print("Is the number of <TE> bigger than <ET>? R.: ", "yes" if TECount >= ETCount else "no")
new_section()

print("Analysis of the tests:\n" \
"1. In english, according to source like Norvigs English letter-pair statistics, the British National Corpus, and " \
"classic frequency tables, the bigram <TE> is sligtly more common than <ET>, however they have basically the same frequency.\n" \
"2. In Test 1, a lot more bigrams were created, however it is very uneven and for the wrong side, which is odd and higly unlikely." \
"For that reason we will guess that (T --> R) is right.\n" \
"3. In english, the third most common letter is A. In the cipher text it is R, however we already used R, so we will go back to the second most common, which is Q." \
"So we will test if the next substitution being (A --> Q) works.")
new_section()

print("Test 1: (A --> Q)")
#              ABCDEFGHIJKLMNOPQRSTUVWXYZ
originalKey = "Q000N00000000000000R000000"
iKey = parcialInverseKey(originalKey) 
dText = parcialCipherMono(cText, iKey) 
print(dText)

print("\nStats of this test: ")
print("Number of <TE> occurances -- Should be VERY common:          ", ngram_count(dText, "TE"))
print("Number of <TA> occurances -- Should be common:               ", ngram_count(dText, "TA"))
print("Number of <ET> occurances -- Should be VERY common:          ", ngram_count(dText, "ET"))
print("Number of <AT> occurances -- Should be EXTREMELY common:     ", ngram_count(dText, "AT"))
print("Number of <EA> occurances -- Should be VERY common:          ", ngram_count(dText, "EA"))
print("Number of <AE> occurances -- Should be rare:                 ", ngram_count(dText, "AE"))
print("Number of <TEA> occurances -- Should be common:              ", ngram_count(dText, "TEA"))
print("Number of <TAE> occurances -- Should be rare:                ", ngram_count(dText, "TAE"))
print("Number of <ETA> occurances -- Should be common:              ", ngram_count(dText, "ETA"))
print("Number of <EAT> occurances -- Should be VERY common:         ", ngram_count(dText, "EAT"))
print("Number of <AET> occurances -- Should be VERY rare:           ", ngram_count(dText, "AET"))
print("Number of <ATE> occurances -- Should be VERY common:         ", ngram_count(dText, "ATE"))


print("Analysis of the results: The fact that the bigram <AE> which should be rare appears 6 times is rather weird. As such we will test at maximum the next 5 most probable" \
"susbtitutions to see if there is a better one, if not we will go back to this")
new_section()


print("Test 2: (A --> C)")
#              ABCDEFGHIJKLMNOPQRSTUVWXYZ
originalKey = "C000N00000000000000R000000"
iKey = parcialInverseKey(originalKey) 
dText = parcialCipherMono(cText, iKey) 
print(dText)

print("\nStats of this test: ")
print("Number of <TE> occurances -- Should be VERY common:          ", ngram_count(dText, "TE"))
print("Number of <TA> occurances -- Should be common:               ", ngram_count(dText, "TA"))
print("Number of <ET> occurances -- Should be VERY common:          ", ngram_count(dText, "ET"))
print("Number of <AT> occurances -- Should be EXTREMELY common:     ", ngram_count(dText, "AT"))
print("Number of <EA> occurances -- Should be VERY common:          ", ngram_count(dText, "EA"))
print("Number of <AE> occurances -- Should be rare:                 ", ngram_count(dText, "AE"))
print("Number of <TEA> occurances -- Should be common:              ", ngram_count(dText, "TEA"))
print("Number of <TAE> occurances -- Should be rare:                ", ngram_count(dText, "TAE"))
print("Number of <ETA> occurances -- Should be common:              ", ngram_count(dText, "ETA"))
print("Number of <EAT> occurances -- Should be VERY common:         ", ngram_count(dText, "EAT"))
print("Number of <AET> occurances -- Should be VERY rare:           ", ngram_count(dText, "AET"))
print("Number of <ATE> occurances -- Should be VERY common:         ", ngram_count(dText, "ATE"))


print("Analysis of the results: No matches were found on the rare ngrams, however no trigrams were made at all, even the ones that should be very common, and" \
"the bigram <AT> which should be extreamly common only found 2, compared to the 9 found by the bigrams that should be only common. Overall this is a better guess than" \
"(A --> Q), but the results it creates are still very weird.")
new_section()


print("Test 3: (A --> F)")
#              ABCDEFGHIJKLMNOPQRSTUVWXYZ
originalKey = "F000N00000000000000R000000"

iKey = parcialInverseKey(originalKey) 
dText = parcialCipherMono(cText, iKey) 
print(dText)

print("\nStats of this test: ")
print("Number of <TE> occurances -- Should be VERY common:          ", ngram_count(dText, "TE"))
print("Number of <TA> occurances -- Should be common:               ", ngram_count(dText, "TA"))
print("Number of <ET> occurances -- Should be VERY common:          ", ngram_count(dText, "ET"))
print("Number of <AT> occurances -- Should be EXTREMELY common:     ", ngram_count(dText, "AT"))
print("Number of <EA> occurances -- Should be VERY common:          ", ngram_count(dText, "EA"))
print("Number of <AE> occurances -- Should be rare:                 ", ngram_count(dText, "AE"))
print("Number of <TEA> occurances -- Should be common:              ", ngram_count(dText, "TEA"))
print("Number of <TAE> occurances -- Should be rare:                ", ngram_count(dText, "TAE"))
print("Number of <ETA> occurances -- Should be common:              ", ngram_count(dText, "ETA"))
print("Number of <EAT> occurances -- Should be VERY common:         ", ngram_count(dText, "EAT"))
print("Number of <AET> occurances -- Should be VERY rare:           ", ngram_count(dText, "AET"))
print("Number of <ATE> occurances -- Should be VERY common:         ", ngram_count(dText, "ATE"))


print("Analysis of the results: This created the most balanced result of the 3, having no rare or very rare, having some trigrams, and not having commons outshine the extremely commons." \
"This is the best guess, and probably good enough to keep going.")
new_section()

print("Analysis of the tests:\n" \
"1. From the tests, we guessed that A was substituted by F." \
"2. The 4th most common letter in the English alphabeth is a tie between I and O, so we will start with either one, let's chosse I.")



# bar("English Language stats", eStats)
# bar("Cypher Text stats", stats(cText))

# input("\nPress Enter to close plots and continue...")
# new_section()
