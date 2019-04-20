# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 20:15:20 2019

@author: huashuo
"""

import json
import matplotlib.pyplot as plt

dic1 = {}
sups = []
confs = []
lifts = []
with open('rules.json','r') as f:
    lines = f.readlines()
    for l in lines:
        load_dic = json.loads(l)
        X = load_dic['X_set'][0][0]
        Y = load_dic['Y_set'][0][0]
        sup = load_dic['sup']
        conf = load_dic['conf']
        lift = load_dic['lift']
        sups.append(load_dic['sup'])
        confs.append(load_dic['conf'])
        lifts.append(load_dic['lift'])
        if X not in dic1.keys():
            new = dict()
            new[Y] = [[sup],[conf]]
            dic1[X] = new
        else:
            if Y not in dic1[X].keys():
                dic1[X][Y] = [[sup],[conf]]
            else:
                dic1[X][Y][0].append(sup)
                dic1[X][Y][1].append(conf)
                

#for k in dic1.keys():
#    print(k)

plt.scatter(sups,confs,c=lifts,s=20,cmap='Reds')
plt.xlabel('sup')
plt.ylabel('conf')
cb = plt.colorbar()
cb.set_label('lift')
plt.show()