
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


            flag = False
            for j in range(i+1, len(words)):
                if words[j] in vocabulary:
                    flag = True
            if not flag:
                new_word = ""
                for k in words[i:]:
                    new_word = new_word + k + " "
                new_word = new_word[:-1]
                replace = rep + str(chr(c))
                Hash[replace] = new_word
                words[i] = new_word
                words = words[:i+1]
                words = replacewords(words, words[i], replace)
                string = ""
                for i in words:
                    string = string + i + " "
                print (string, Hash)
                return  (string, Hash)


            replace = rep + str(chr(c))
            c += 1
            Hash[replace] = words[i]
            words = replacewords(words, words[i], replace)

    string = ""
    for i in words:
        string = string + i + " "
    
    string = string.strip()
    print (string, Hash)
    
    return  (string, Hash)

def outputrepair(string, dictionary):
    words = string.split()
    output = []
    for i in words:
        if i[:5] == '_UNK_' and (i in dictionary):
            output.append(dictionary[i])
        else:
            output.append(i)
    string = ""
    for i in output:
        string = string + i + " "
    return string

if __name__ == '__main__':
    #t = raw_input("Enter a string : ")
    t = "hello my get gotyui"
    cat = ['hello', 'my', 'name', 'is', 'hi', 'cat', 'dog', 'the', 'a', '.', ',']
    string, dictionary = inputrepair(t, cat)
    print string
    string = outputrepair(string, dictionary)
    print string
