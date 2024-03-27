import json
import os

# 读取文件中的所有数据
def get_data(filepath):
    # 打开 train.json文件读取数据
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
    return data

# 统计文件后缀及数量
def count_file_extensions(data):
    # 创建一个字典用于存储文件后缀及其出现次数
    extension_counts = {}

    # 遍历每个字符串列表中的文件名
    for d in data:
        for f in d['gt_files']:
            # 使用字符串操作提取文件后缀
            _, extension = os.path.splitext(f)
            # 将后缀添加到字典中，并统计出现次数
            extension_counts[extension] = extension_counts.get(extension, 0) + 1
    sorted_extensions = sorted(extension_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_extensions

# 统计gt_files数量
def count_gtfiles_num(data):
    gtfile_num_counts = {}
    for d in data:
        l = len(d['gt_files'])
        gtfile_num_counts[l] = gtfile_num_counts.get(l,0) + 1
    sorted_filenums = sorted(gtfile_num_counts.items(),key=lambda x: x[1], reverse=True)
    return sorted_filenums


if __name__ == "__main__":
    filepath = "../data/retrieval/data.json"
    data = get_data(filepath)
    # extension_counts = count_file_extensions(data)
    # print(extension_counts)
    gtfile_num_counts = count_gtfiles_num(data)
    print(gtfile_num_counts)
