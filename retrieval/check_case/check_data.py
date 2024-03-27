import json

# 筛选作为样本观察的数据，data_file为所有数据的文件，repo_name对应哪一个repo，data_num是数据量
def filter_sample_data(data_file,repo_name,data_num,store_path):
    # 读取JSON文件
    with open(data_file, 'r') as f:
        data = json.load(f)
    # 筛选数据
    filtered_data = []
    num = 0
    for d in data:
        # 在这里可以添加筛选条件
        if d['repo_name'] == repo_name:
            filtered_data.append(d)
            num += 1
            if num == data_num:
                break
    # 将筛选后的数据保存到另一个JSON文件
    with open(store_path, 'w') as f:
        json.dump(filtered_data, f, indent=4)  # 使用indent参数可以使输出更易读

if __name__ == "__main__":
    data_file = "/home/fdse/wy/RepoCodeEdit/data/retrieval/data.json"
    repo_name = "docker/compose"
    store_path = "/home/fdse/wy/RepoCodeEdit/data/retrieval/" + repo_name.split('/')[1] + ".json"
    filter_sample_data(data_file,repo_name,20,store_path)