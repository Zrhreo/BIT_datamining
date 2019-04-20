# -*- coding:UTF-8 -*-
"""
@author: ZhaoRenhao
"""
import os
from association import Association
import json
import pandas as pd
import matplotlib.pyplot as plt
from interval import Interval

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, str):
            return str(obj);
        return json.JSONEncoder.default(self, obj)

class Data(object):
    def __init__(self):

        # 属性列名文件路径
        self.dataset_path = r'../winemag-data-130k-v2.csv'

        # 结果文件路径
        self.result_path = r'./results'

    def process_nom_features(self):
        """
        处理一批标称属性，获取所有可能的取值及其对应个数（包括缺失值的个数）
        :param feature_list: 属性列表
        :return: 一个字典，key为所有可能取值，value为取值对应的个数
        """
        out_path = self.result_path
        association = Association()
        filename = self.dataset_path

        # 遍历全部属性
        columns = []
        #连续属性离散化
        dataload = pd.read_csv(filename)
        dataload['price'] = pd.cut(dataload['price'],[0,8,12,16,20,24,28,32,36,60,100,3300])
        dataload['points'] = pd.cut(dataload['points'],20)
        
        dataload = dataload[['country','points','price','province','region_1','variety']]
        for feature_name in dataload.keys():
            print("Dealing with feature: {}".format(feature_name))
            columns.append(list(dataload[feature_name]))

        rows = list(zip(*columns))
        # 将数据转为数据字典存储
        dataset = []
        feature_names = list(dataload.keys())
        for data_line in rows:
            data_set = []
            for i , value in enumerate(data_line):
                if value == value:
                    data_set.append((feature_names[i], value))
            if data_set:
                dataset.append(data_set)
        
        # 获取频繁项集
        freq_set , support_data = association.apriori(dataset)
        support_data_out = sorted(support_data.items(), key= lambda d:d[1],reverse=True)
        #print(support_data_out)
        # 获取强关联规则列表
        big_rules_list = association.generate_rules(freq_set, support_data)
        big_rules_list = sorted(big_rules_list, key= lambda x:x[3], reverse=True)
        big_rules_list = sorted(big_rules_list, key= lambda x:x[4], reverse=True)
        #print(big_rules_list)
        
        # 将频繁项集输出到结果文件
        freq_set_file = open('freq_set.json', 'w',encoding='utf-8')
        for (key, value) in support_data_out:
            result_dict = {'set':None, 'sup':None}
            set_result = list(key)
            sup_result = value
            result_dict['set'] = set_result
            result_dict['sup'] = sup_result
            json_str = json.dumps(result_dict, cls=MyEncoder)
            freq_set_file.write(json_str+'\n')
        freq_set_file.close()
        
        # 将关联规则输出到结果文件
        rules_file = open('rules.json', 'w',encoding='utf-8')
        for result in big_rules_list:
            result_dict = {'X_set':None, 'Y_set':None, 'sup':None, 'conf':None, 'lift':None}
            X_set, Y_set, sup, conf, lift, cosine= result
            result_dict['X_set'] = list(X_set)
            result_dict['Y_set'] = list(Y_set)
            result_dict['sup'] = sup
            result_dict['conf'] = conf
            result_dict['lift'] = lift
            result_dict['cosine'] = cosine
            json_str = json.dumps(result_dict,cls=MyEncoder, ensure_ascii=False)
            rules_file.write(json_str + '\n')
        rules_file.close()
        
if __name__ == '__main__':
    data = Data()
    data.process_nom_features()