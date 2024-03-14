import json
import os
import subprocess

# 存储所有需要克隆的仓库名称
def store_repo_names(filepath):
    repo_names = []
    # 打开 train.json文件读取数据
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
        for d in data:
            if d['repo'] not in repo_names:
                repo_names.append(d['repo'])
    print(len(repo_names))
    # 将仓库名称存入txt文件，以便使用
    store_file = '../../data/repo_names.txt'
    # 打开文件并写入字符串列表中的每一行
    with open(store_file, 'w') as f:
        for repo in repo_names:
            f.write(repo + '\n')

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

# 判断路径是否为空
def is_path_empty(path):
    # 使用 os.listdir() 函数列出路径下的所有文件和文件夹
    items = os.listdir(path)
    # 如果返回的列表为空，则说明路径下没有任何内容
    return len(items) == 0

# Clone仓库到raw_repo文件夹下
def clone_repo(repo_name):
    # 仓库 URL 和本地路径
    repo_url = f"https://github.com/{repo_name}.git"
    repo_path = "../../data/raw_repos/" + repo_name  # 替换为您希望克隆仓库的路径
    temp_path = "../../data/raw_repos/" + repo_name.split("/")[0]
    if not os.path.exists(temp_path):
        # 使用 git clone 命令克隆仓库
        subprocess.run(["git", "clone", repo_url, repo_path])
        print("Repository cloned successfully!")
    else:
        if is_path_empty(temp_path):
            # 使用 git clone 命令克隆仓库
            subprocess.run(["git", "clone", repo_url, repo_path])
            print("Repository cloned successfully!")

# 将仓库中的py文件保留，其余文件删除
def filter_python_files(repo_name):
    repo_path = "../../data/raw_repo/" + repo_name
    # 遍历文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            # 检查文件是否是 .py 文件
            if file.endswith('.py'):
                # 如果是 .py 文件，则保留，否则删除
                continue
            else:
                # 删除非 .py 文件
                file_path = os.path.join(root, file)
                os.remove(file_path)

if __name__ == "__main__":
    # filepath = "../../data/SWE-bench_bm25_13K/train.json"
    # store_repo_names(filepath)
    repo_names = get_repo_names()
    # 克隆仓库
    for repo_name in repo_names:
        clone_repo(repo_name)
    # 过滤仓库的文件，只保留Python文件
    # for repo_name in repo_names:
    #     filter_python_files(repo_name)