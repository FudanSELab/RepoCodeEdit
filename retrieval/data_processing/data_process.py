import os
import json
import pandas as pd

# 获得SWE-bench_bm25_13K数据集的所有原始parquet文件路径
def get_parquet_files(folder_path):
    f_files = []
    # 使用 os.walk()函数遍历文件夹下的所有文件和子文件夹
    for root,dirs,files in os.walk(folder_path):
        for file in files:
            # 输出文件路径
            file_path = os.path.join(root, file)
            f_files.append(file_path)
    return f_files

# 将parquet文件转变为list数据
def convert_parquet_to_list(file_path):
    # 读取 Parquet 文件
    df = pd.read_parquet(file_path)
    # 处理 df数据，转换成list数据
    dict_list = df.to_dict(orient='records')
    return dict_list

# 将 SWE-bench_bm25_13K数据集存储为json文件保存，分为train、dev、validation、test文件
def store_dataset_json():
    # 获得 SWE-bench_bm25_13K数据集的原始parquet文件路径
    p_files = get_parquet_files('../../data/SWE-bench_bm25_13K')
    train_list = []
    dev_list = []
    validation_list = []
    test_list = []
    # 遍历每一个文件
    for p_file in p_files:
        list_data = convert_parquet_to_list(p_file)
        if 'train' in p_file:
            train_list += list_data
        elif 'dev' in p_file:
            dev_list += list_data
        elif 'validation' in p_file:
            validation_list += list_data
        else:
            test_list += list_data
    # 将train列表数据转换为 JSON 格式的字符串，并存入json文件
    json_str = json.dumps(train_list, indent=4)  # indent 参数用于指定缩进格式，可选项
    with open('../../data/SWE-bench_bm25_13K/train.json', 'w') as json_file:
        json_file.write(json_str)
    # 将dev列表数据转换为 JSON 格式的字符串，并存入json文件
    json_str = json.dumps(dev_list, indent=4)  # indent 参数用于指定缩进格式，可选项
    with open('../../data/SWE-bench_bm25_13K/dev.json', 'w') as json_file:
        json_file.write(json_str)
    # 将validation列表数据转换为 JSON 格式的字符串，并存入json文件
    json_str = json.dumps(validation_list, indent=4)  # indent 参数用于指定缩进格式，可选项
    with open('../../data/SWE-bench_bm25_13K/validation.json', 'w') as json_file:
        json_file.write(json_str)
    # 将test列表数据转换为 JSON 格式的字符串，并存入json文件
    json_str = json.dumps(test_list, indent=4)  # indent 参数用于指定缩进格式，可选项
    with open('../../data/SWE-bench_bm25_13K/test.json', 'w') as json_file:
        json_file.write(json_str)

if __name__ == "__main__":
    store_dataset_json()

