import math
import copy
from copy import deepcopy
from decimal import *

file_read = open('input03.txt', 'r')
file_write = open('output.txt', 'w')
query_flag = 0
input_val = []

output_query = []
utility = []
dec_network = []
table = {}
bayesNet = []

dec_graph = {}
for line in file_read.read().strip().split("\n"):
    if line == "******" and not query_flag:
        output_query = input_val
        input_val = []
        query_flag = 1
    elif line == "******" and query_flag:
        dec_network = input_val
        input_val = []
    else:
        input_val.append(line)

if input_val and dec_network:
    utility = input_val
elif input_val:
    dec_network = input_val

new_var = 1
new_lst = []
name = ""
for dec in dec_network:
    if dec == "***":
        new_var = 1
        table[name] = new_lst
        new_lst = []
    elif new_var == 1:
        new_var = 0
        # dec = ''.join(dec.split())
        i = 0
        for ele in list(dec.split()):
            if i == 0:
                name = ele
                bayesNet.append(name)
            if i > 1:
                new_lst.append(ele)
            i += 1
        dec_graph[name] = new_lst
        new_lst = []
    else:
        # dec = ''.join(dec.split())
        new_lst.append(dec.split())

if new_lst:
    table[name] = new_lst


def enumerationAsk(X, e, vars1):
    print "inside enumeration ASK"
    print X, e, vars1
    QX = {}
    QX['-'] = 1.0
    QX['+'] = 1.0
    print "Exit enumeration ASK"
    return QX


def findProbability(query):
    print "Entering findProbability"
    print query
    lst = query.strip().split("|")
    value = 1.0;
    ovar = lst[0].split(',')
    if len(lst) > 1:
        e = lst[1].strip().split(",")
        edict = dict((x.strip()[0], '+' if x.strip()[4] == '+' else '-') for x in e)
        for x in ovar:
            x_split = x.split()
            if x_split[2] == '+':
                value = value * enumerationAsk(x_split[0], edict, bayesNet).get('+')
                edict.update({x_split[0]: '+'})
            else:
                value = value * enumerationAsk(x_split[0], edict, bayesNet).get('-')
                edict.update({x_split[0]: '-'})
        file_write.write(str(Decimal(str(value)).quantize(Decimal('.01'))))
    else:
        for x in ovar:
            edict = {}
            x_split = x.split()
            if x_split[2] == '+':
                value = value * enumerationAsk(x_split[0], edict, bayesNet).get('+')
                edict.update({x_split[0]: '+'})
            else:
                value = value * enumerationAsk(x_split[0], edict, bayesNet).get('-')
                edict.update({x_split[0]: '-'})
        file_write.write(str(Decimal(str(value)).quantize(Decimal('.01'))))

    print "Exiting findProbability"
    return


def update_split_value(x_split, dict_ele):
    if x_split[2] == '+':
        dict_ele.update({x_split[0]: True})
    else:
        dict_ele.update({x_split[0]: False})


def findExpectedUtility(query):
    print "Entering findExpectedUtility"
    print query
    dict_ele = {}

    lst = query.strip().strip().split("|")
    for x in lst[0].strip().split(','):
        x_split = x.strip().split()
        update_split_value(x_split, dict_ele)

    if len(lst) > 1:
        for x in lst[1].strip().split(","):
            x_split = x.strip().split()
            update_split_value(x_split, dict_ele)


    return


def findMaxExpectedUtility(query):
    print query
    return


qtype = ""
new_query = ""
for query in output_query:
    flag = 0
    i = 0
    while 1:
        if query[i] == '(':
            flag = 1
        elif flag == 0:
            qtype += query[i]
        elif flag == 1:
            if query[i] == ')':
                break
            if query[i] != "=" or (query[i-1] != "=" and query[i] != " "):
                new_query += query[i]
        i += 1

    if qtype == 'P':
        findProbability(new_query)
    elif qtype == 'EU':
        findExpectedUtility(new_query)
    elif qtype == 'MEU':
        findMaxExpectedUtility(new_query)
    qtype = ""
    new_query = ""

eutility = {}
flag = 0
rest = []
name = []
for x in utility:
    if flag == 0:
        first = x.split('|')
        name = first[1].split()
        flag = 1
    else:
        rest.append(x.split())
eutility["nodes"] = name
eutility["values"] = rest

print "Decision graph: " , dec_graph
print "table: ", table
print "Utility: ", eutility
