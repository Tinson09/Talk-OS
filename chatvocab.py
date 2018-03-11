
def replacewords(lis, word, rep):
    for i, x in enumerate(lis):
        if x == word:
            lis[i] = rep
    return lis

def inputrepair(string, vocabulary):
    words = string.split()
    rep = "_UNK_"
    c = 97
    Hash = {}
    for i in range(len(words)):
        if not words[i] in vocabulary:
            replace = rep + str(chr(c))
            c += 1
            Hash[replace] = words[i]
            words = replacewords(words, words[i], replace)
    
    string = ""
    for i in words:
        string = string + i + " "
    
    return  (string, Hash)

def outputrepair(string, dictionary):
    words = string.split()
    output = []
    for i in words:
        if i[:5] == '_UNK_':
            output.append(dictionary[i])
        else:
            output.append(i)
    string = ""
    for i in output:
        string = string + i + " "
    return string

if __name__ == '__main__':
    t = raw_input("Enter a string : ")
    cat = ['hello', 'my', 'name', 'is', 'hi', 'cat', 'dog', 'the', 'a', '.', ',']
    string, dictionary = inputrepair(t, cat)
    print string
    string = outputrepair(string, dictionary)
    print string
