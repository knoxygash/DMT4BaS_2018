import os
from bs4 import BeautifulSoup
import string



folder = "/home/arywatt/PycharmProjects/lyrics_collection__CONVERTED/"
fileList = os.listdir(folder)
N = 10000 # limit of number of file to work on
N_hash_functions = 1120  # number of hash functions to assure a probability >= 0.97
Hash_functions_file = 'hash_functions_file'
hashed_sets = 'hashed_sets'
hashed_sets_all = 'hashed_sets_all'

def isHtml(file):
    h = file.split('.')[-1]
    if (h =='html'):
        return True
    return False


def remove_punctuations(lyrics):
    punctuations = dict.fromkeys(map(ord, '\n' + string.punctuation), "  ")
    l = lyrics.translate(punctuations)
    return l

def jaccard(s1,s2,n) :
    # we use n-shingles of set of words
    ks1 = shingles(' '.join(s1),n)
    ks2 = shingles(' '.join(s2),n)

    return  len(set(ks1) & set(ks2)) / len(set(ks1) | set(ks2))


def shingles(s,k): # return k-shingles of a set
    li = s.strip().split()
    if k<len(li):
        return set([' '.join(li[i:i+k]) for i in range(len(li)-k+1) ])
    return set(s)


def extractLyric(folder,file): # extract lyric from a file
    if(os.path.isfile(folder+file) ):
        ctn = open(folder+file,"r")
        page = BeautifulSoup(ctn.read(),'html.parser')
        elts = page.find('title').string
        title = 'none'

        # checking lyrics and extracting
        lyr = page.find('body')
        lyrics = ""
        if(lyr):
            for x in lyr.find_all('br'):
                x.replace_with(' . ')
            lyrics = lyr.text

        # Close buffer
        ctn.close()
        h = remove_punctuations(title + lyrics).lower()
        #print (shingles(h,3))
        return [file,shingles(h,3)]

def min_Hashing(fileList): # produces the hashed set for all lyrics and save it in a file
    hash_functions = hash_factory()
    with open(hashed_sets_all, 'w+') as ft:
        for file in fileList:
            elmt = extractLyric(folder,file)
            id = elmt[0]
            hashes = [min([hx(t) for t in elmt[1]]) for hx in hash_functions]
            ft.write(id+'\t'+ str(hashes)+'\n')

    return ''


def hash_factory():  #create a list of LSH  hash functions to use
    hash_functions = []
    def hash_function(a,b,n,p):
        return(lambda x: ((a*hash(x)+b)%p)%n )
        #return(lambda x: hash(x))

    with open(Hash_functions_file,'r') as file:
        for line in file.readlines()[2:]:
            a,b,p,n = [int(x) for x in line.strip().split()]
            hash_functions.append(hash_function(a,b,p,n))
    return hash_functions



# Generate LSH matrix
min_Hashing(fileList)

