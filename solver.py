
##Load words into initial dict
initwords = []
lfreq = {}

wordfile = open('words.txt', 'r')
Lines = wordfile.readlines()

wordcount = 0
#read words from word list
for line in Lines:
    initwords.append(line[:-1])
    for l in line:
        if l in lfreq.keys():
            lfreq[l] += 1
        else:
            lfreq[l] = 1
    wordcount += 1
wordfile.close()

#create letter frequency
for l in lfreq:
    lfreq[l] = lfreq[l] / wordcount

#score words
words = {}
for i in initwords:
    score = 0
    for j in i:
        score += lfreq[j]
    words[i] = score

#return best word from dict
def get_best_guess(dwords):
    return max(dwords, key=dwords.get)

#cull words in word dictionary
def cullwords(word, wresult, dwords):
    past_l = {} #correct for letter duplicates
    for i in word:
        if i in past_l.keys():
            past_l[i] += 1
        else:
            past_l[i] = 1
    
    for i in range(len(word)): #same length as wresult
        if wresult[i] == '2': #same letter and same pos
            for w in list(dwords):
                if w[i] != word[i]:
                    del dwords[w]
        elif wresult[i] == '0': 
            if past_l[word[i]] == 1: #only one copy of this letter and not in word
                for w in list(dwords):
                    if word[i] in w:
                        del dwords[w]
            elif past_l[word[i]] > 1: #sometimes you can have 1 yellow and 1 blank of the same letter so this corrects for that
                past_l[word[i]] -= 1
                for w in list(dwords):
                    if word[i] == w[i]:
                        del dwords[w]
        elif wresult[i] == '1': #letter in word not same pos
            for w in list(dwords):
                if word[i] == w[i]:
                    del dwords[w]
                if word[i] not in w:
                    del dwords[w]


print("-----------------------------------------")
print('Wordle helper will recommend a word to put into wordle online.')
print('''After inputting your word online, in the command line create a length 5 string where
0 corresponds to no match, 1 corresponds to correct letter, incorrect pos, and 2 is correct letter and pos''')
print('''Example: secret word is tries and inputted recommended word is tears. 
User input when requested would be: '21012' because the t and s are in the correct positions, e and r are in incorrect 
positions and a is not in tries at all.''')
print("-----------------------------------------")         
print('First recommendation: ' + 'roast')
print("-----------------------------------------")

tries = 5 #5 tries given that first word already chosen
solved = False
guess = 'roast' #start with roast because it is near optimal word (contains most used letters)
while tries > 0 and not solved:
    wordleresult = str(input('input 5 char 0/1/2 result here: \n'))
    if wordleresult == '22222':
        solved = True
        print('Congradulations! Wordle solved.')
    else:
        cullwords(guess, wordleresult, words)
        guess = get_best_guess(words)
        del words[guess]
        if len(words) == 0:
            print('final word is: ' + guess)
            solved = True
        else: 
            print('Next word recommendation: ' + guess)
    tries -= 1
