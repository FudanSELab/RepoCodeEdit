import json

# 读取所有repo_names
def get_repo_names():
    file_path = '../../data/repo_names.txt'
    repo_names = []
    # 打开文件并逐行读取数据
    with open(file_path, 'r') as file:
        for line in file:
            # 去除每行末尾的换行符，并添加到列表中
            repo_names.append(line.rstrip())
    return repo_names

# 读取数据
def get_data(filepath):
    # 打开 train.json文件读取数据
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
    return data

def generate_test_data(repo_names):
    for repo_name in repo_names:
        new_name = repo_name.split('/')[-1]
        repo_json_path = "/home/fdse/wy/RepoCodeEdit/data/retrieval/repo_data_jsons/" + new_name + ".json"
        repo_data = get_data(repo_json_path)
        repo_test_json = "/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/" + new_name +".json"
        with open(repo_test_json,'w') as f:
            json.dump(repo_data[:10],f,indent=2)

def test(repo_names):
    for repo_name in repo_names:
        new_name = repo_name.split('/')[-1]
        repo_test_json = "/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/" + new_name +".json"
        repo_data = get_data(repo_test_json)
        print(len(repo_data))
        for d in repo_data:
            if not d['gt_files']:
                print("哈哈哈哈哈哈哈哈哈")
        print('-'*80)

if __name__ == "__main__":
    repo_names = get_repo_names()
    # generate_test_data(repo_names)
    test(repo_names)