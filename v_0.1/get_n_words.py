# 输入：训练好的K-means聚类算法词向量（pkl）；sogou.word.word，数据格式：word，list[1]，list[2]...
# 输出：聚类中心周围n个词，格式：类别 + 词*N
# 功能部件：1.数据加载 2.数据存储 3.可视化表示词云（未完成） 4.计算cos值（衡量相近程度） 5.获取聚类中心N个词
# Author: 千山漫雪空
# verson: v0.1
# encoding: utf-8

from sklearn.externals import joblib
import numpy as np


class cluster_kmeans(object):
    def __init__(self, vec_filename, word_filename):
        self.vec_file = joblib.load(vec_filename)
        self.word_filename = word_filename
        self.dic = {}
        self.vec = []

    def load_data(self):
        with open(self.word_filename, 'r', encoding='utf-8') as f:  # word中数据写入
            for element in f:
                element_list = element.split(' ')
                word_name = element_list[0]
                del element_list[len(element_list) - 1]
                del element_list[0]
                if len(element_list) == 0:
                    continue
                else:
                    self.dic[word_name] = list(map(eval, element_list))    # 数据写入结束

        for word_vec in self.vec_file.cluster_centers_:
            vec_list = np.ndarray.tolist(word_vec)
            self.vec.append(vec_list)

        print('数据加载完毕   =。=')

    def save_result(self, save_file, result, n):  # 传入list
        count = 0
        save_file_m = save_file + '_聚类中心_' + str(n) + '词.txt'
        with open(save_file_m, 'a', encoding='utf-8') as f:
            for i in range(len(result)):
                for j in range(len(result[i])):
                    f.write(str(result[i][j]))
                    f.write('\n')
                    if j == len(result[i]) - 1:
                        f.write('-'*20)
                        f.write('\n')
                    count += 1
            print('\r当前文本保存进度：{:.2f}%'.format(100*count / (len(result))))  # 文本保存进度条

    def cluster(self, n):  # n代表取前几个周围的向量。函数功能：获取聚类中心n个词
        result_list = []
        count = 0
        for li in self.vec:  # 这里vec是一个2维的数组，li相当于一次取一行进行处理
            deal_n_dict = {}
            compare_list = []
            name_list = []

            for key in self.dic:  # 建立字典，词与value相对应
                value = cluster_kmeans.get_distance(self, list_vec=li, list_word=self.dic[key])
                if key not in deal_n_dict:
                    deal_n_dict[key] = value  # 建立结束
            for key in deal_n_dict:
                compare_list.append(deal_n_dict[key])
            compare_list.sort()
            compare_list.reverse()
            for i in compare_list[:n]:
                reflact_dict = dict(zip(deal_n_dict.values(), deal_n_dict.keys()))
                name_list.append(reflact_dict[i])

                count += 1
                print('\r当前进度：{:.2f}%'.format(10*count/(n * len(self.vec))), end='')   # 结果列表加载进度条

            result_list.append(name_list)

        print('结果列表加载完毕  =。=')
        # print(result_list)
        return result_list

    def get_distance(self, list_vec, list_word):
        A = 0
        B = 0
        AB = 0
        for i in range(len(list_word)):
            A = A + list_vec[i]*list_vec[i]
            B = B + list_word[i]*list_word[i]
            AB = AB + list_word[i]*list_vec[i]
        distance = AB/(A**0.5*B**0.5)
        return distance

    def visualization(self):
        pass


if __name__ == '__main__':
    a = r''  # 聚类结束后的文件（包含聚类中心向量等数据）
    b = r''  # 原始训练好的词向量文件
    save_file_name = r''  # 具体到文件后缀之前的名字
    k = cluster_kmeans(vec_filename=a, word_filename=b)
    k.load_data()
    result_li = k.cluster(10)
    k.save_result(result=result_li, save_file=save_file_name, n=10)
