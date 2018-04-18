
import collections
import numpy as np
import csv
import math

# Files included in project
gt_file = "../resources/part_1_1__Ground_Truth.tsv"
s1_file = "../resources/part_1_1__Results_SE_1.tsv"
s2_file = "../resources/part_1_1__Results_SE_2.tsv"
s3_file = "../resources/part_1_1__Results_SE_3.tsv"

files = [s1_file,s2_file,s3_file]
NS = len(files)


# First of all let's store all query's doc's in  a dictionary

qdict = collections.defaultdict(set)

# Read  ground truth file to populate dictionary
# query id will be the key
# and value will be a set of relevant doc ids

with  open(gt_file,'r') as gt:
    for line in gt.readlines()[2:]:
        t = line.strip().split()
        qdict[int(t[0])].add(int(t[1])) # the ranking is determined by position in list
gt.close()


# We do the same for search engines  query results
s_dicts = []


for i in range(NS):
    s_dicts.append(collections.defaultdict(list)) # to store query  results
    with  open(files[i],'r') as s_file:
        for line in s_file.readlines()[2:]:
            t = line.strip().split()
            s_dicts[i][int(t[0])].insert(int(t[2]),int(t[1])) # the ranking is determined by position in list
    s_file.close()



## k-recision@k measure.
def kprecision():

    ind = [1,3,5,10]
    s_count = [[] for i in range(len(s_dicts))]
    s_info = [[] for i in range(len(s_dicts))]
    for key in qdict.keys():
        S = set(qdict[key]) # retrieve relevant doc for query
        if (len(S)> 0):
            for i in range(len(s_dicts)):
                sr = list(s_dicts[i][key])
                s_mean = []

                for k in ind:
                    s_mean.append(len(set(S) & set(sr[:k]))/k)
                s_count[i].append(s_mean)

    for i in range(len(s_dicts)):
        #s_info[i] = [sum(x)/len(s_count[i]) for x in zip(*s_count[i])]
        s_info[i] = [round(sum(x)/len(s_count[i]),3) for x in zip(*s_count[i])]

    return s_info



# r-precision measure
def rprecision():
    count = []
    s_count = [[] for i in range(len(s_dicts))]
    s_info = [[] for i in range(len(s_dicts))]
    for key in qdict.keys():
        S = set(qdict[key]) # retrieve relevant doc for query
        K = len(S)
        if(K >0):
            for i in range(len(s_dicts)):# for every search engine do thi
                sr = list(s_dicts[i][key])
                s_count[i].append(len(set(S) & set(sr[:K]))/K)
            
    for i in range(len(s_dicts)): # for every search engine do this
        s_info[i] = [np.mean(s_count[i]),min(s_count[i]),np.percentile(s_count[i],25),np.percentile(s_count[i],50),np.percentile(s_count[i],75),max(s_count[i])]
    s_info2 = [[round(x[i],3) for i in range(len(x))]for x in s_info]
    return s_info2


def first_relevant_doc_index(rset, qlist):
   # print(len(rset),len(qlist))
    for i in range(len(qlist)):
        if qlist[i] in rset:
            return 1/(i+1);
    return 0


## MRR
def MRR():
    Q = len(qdict.keys())
    s_sum = [0 for i in range(len(s_dicts))]
    mrr = [[] for i in range(len(s_dicts))]
    for key in qdict.keys():
        rset = qdict[key]
        for i in range(len(s_dicts)): # for every search engine
            s_sum[i] = s_sum[i] +first_relevant_doc_index(rset,s_dicts[i][key])

    for i in range(len(s_dicts)):
        mrr[i] = [round(1/Q * s_sum[i],3)]

    return mrr



def nDCG():
    ind = [1, 3, 5, 10]
    s_count = [[] for i in range(len(s_dicts))]
    s_info = [[] for i in range(len(s_dicts))]
    for key in qdict.keys():
        S = set(qdict[key])  # retrieve relevant doc for query
        if (len(S) > 0):
            for i in range(len(s_dicts)):
                sr = list(s_dicts[i][key])
                s_mean = []
                for k in ind:
                    s_mean.append(DCG(S,sr,k)/iDCG(k))
                s_count[i].append(s_mean)

    for i in range(len(s_dicts)):
        s_info[i] = [round(sum(x) / len(s_count[i]),3) for x in zip(*s_count[i])]

    return s_info

def relevance(S,sr,k):
    d = math.log2(k) if k > 1 else 1
    if sr[k] not in S:
        return 0
    return 1/d



def DCG(S,sr,k):
    R = 0;
    for i in range(1,k+1):
        R = R + relevance(S,sr,i)
    return R

def iDCG(k):
    R =1
    if k == 1:
        return R
    else:
        for i in range(2,k+1):
            R = R + 1/math.log2(i)
    return R


# Take in parameters some data, and write them in file
def writeCsv(filename,header,data):
    with open(filename, 'w+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for i in range(len(data)):
            dict = {}
            for j in range(len(header)):
                dict[header[j]] = data[i][j]
            writer.writerow(dict)


#to print k-precision result in an csv file
def print_kprecision():
    filename = 'p_at_k.csv'
    header = ['Search Engine', 'Mean(P@1)', 'Mean(P@3)', 'Mean(P@5)', 'Mean(P@10)']
    data = kprecision()
    data[0].insert(0, 'SE_1')
    data[1].insert(0, 'SE_2')
    data[2].insert(0, 'SE_3')
    writeCsv(filename, header, data)


def print_rprecision():
    filename = 'R-Precision.csv '
    header = ['Search Engine','Mean(R-Precision_Distrbution)','min(R-Precision_Distrbution)','1°_quartile (R-Precision_Distrbution)','MEDIAN(R-Precision_Distrbution','3°_quartile (R-Precision_Distrbution)','MAX(R-Precision_Distrbution)']
    data = rprecision()
    data[0].insert(0,'SE_1')
    data[1].insert(0,'SE_2')
    data[2].insert(0,'SE_3')
    writeCsv(filename,header,data)

def print_MRR():
    filename = 'MRR.csv'
    header = ['Search Engine', 'MRR']
    data = MRR()
    data[0].insert(0, 'SE_1')
    data[1].insert(0, 'SE_2')
    data[2].insert(0, 'SE_3')
    writeCsv(filename, header, data)

def print_ndcg():
    filename = 'nDCG.csv'
    header = ['Search Engine', 'Mean(nDCG@1)', 'Mean(nDCG@3)', 'Mean(nDCG@5)', 'Mean(nDCG@10)']
    data = nDCG()
    data[0].insert(0, 'SE_1')
    data[1].insert(0, 'SE_2')
    data[2].insert(0, 'SE_3')
    writeCsv(filename, header, data)

print_kprecision()
print_rprecision()
print_MRR()
print_ndcg()




