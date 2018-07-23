# get_Cluster_center_n_words
词向量文件中，用以获取聚类中心N个词

# 输入：训练好的K-means聚类算法词向量（pkl）；sogou.word.word，数据格式：word，list[1]，list[2]...
# 输出：聚类中心周围n个词，格式：类别 + 词*N
# 功能部件：1.数据加载 2.数据存储 3.可视化表示词云（未完成） 4.计算cos值（衡量相近程度） 5.获取聚类中心N个词
