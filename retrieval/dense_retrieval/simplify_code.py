import os
import sys
# sys.path.append("../..")
import json
from utils import get_repo_path,switch2commit,get_repo_code,get_repo_names,extract_classes_and_functions

# 读取数据
def get_data(filepath):
    # 打开 train.json文件读取数据
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
    return data

# 读取每个repo_name对应的commit_ids
def get_repo_commits():
    with open('/home/fdse/wy/RepoCodeEdit/data/retrieval/repo_commits.json','r') as f:
        repo_commits = json.load(f)
    return repo_commits
        
# 将数据按照 repo_name 进行划分
def distract_data_by_repo(data):
    repo_jsons = {}
    for d in data:
        repo_name = d['repo_name']
        new_js = {"repo_name":repo_name,"issue":d['issue'],"commit_id":d["commit_id"],"gt_files":d["gt_files"]}
        if repo_name in repo_jsons:
            repo_jsons[repo_name].append(new_js)
        else:
            repo_jsons[repo_name] = [new_js]

    for repo_name in repo_jsons:
        new_name = repo_name.split('/')[-1]
        with open(os.path.join('/home/fdse/wy/RepoCodeEdit/data/retrieval/repo_data_jsons',f"{new_name}.json"),'w') as f:
            json.dump(repo_jsons[repo_name],f,indent=2)

# 读取每一个repo.json，保存<repo,commit>对,存为repo_commit.json
def generate_repo_commit(repo_names):
    result = []
    for repo_name in repo_names:
        new_name = repo_name.split('/')[-1]
        repo_json_path = os.path.join('/home/fdse/wy/RepoCodeEdit/data/retrieval/repo_data_jsons',f'{new_name}.json')
        with open(repo_json_path, 'r') as f:
            data = json.load(f)
        commit_ids = []
        for d in data:
            if d['commit_id'] not in commit_ids:
                commit_ids.append(d['commit_id'])
        temp = {}
        temp['repo_name'] = repo_name
        temp['commit_ids'] = commit_ids
        result.append(temp)
    with open('/home/fdse/wy/RepoCodeEdit/data/retrieval/repo_commits.json','w') as f1:
            json.dump(result,f1,indent=2)

# 为每一个repo_name在repo_commit_code中建立repo_name文件夹
def create_repo_dirs(repo_names):
    for repo_name in repo_names:
        new_name = repo_name.split('/')[-1]
        folder_path = os.path.join('/home/fdse/wy/RepoCodeEdit/data/repo_commit_code',new_name)
        os.makedirs(folder_path, exist_ok=True)

# 为每一个<repo,commit>建立json文件
def create_repo_commit_json():
    # repo_names = get_repo_names()
    # 为每一个repo_name在repo_commit_code中建立repo_name文件夹
    # create_repo_dirs(repo_names)
    # 读取每个repo_name对应的commit_ids
    repo_commits = get_repo_commits()
    for repo_commit in repo_commits:
        repo_name = repo_commit['repo_name']
        new_name = repo_name.split('/')[-1]
        commit_ids = repo_commit['commit_ids']
        repo_path = get_repo_path(repo_name)
        for commit_id in commit_ids:
            repo_commit_data = []
            # 切换到该仓库下的commit_id状态
            switch2commit(repo_path,commit_id)
            # 获取repo在该commit_id下的所有py文件
            repo_code = get_repo_code(repo_path)
            for rc in repo_code:
                file_path = rc['file_path']
                code = rc['code']
                file_name = file_path.split('/')[-1]
                classes,functions = extract_classes_and_functions(code)
                if classes or functions:
                    simplified_code = "filename:" + file_name + " class:" + str(classes) + " functions:" + str(functions)
                    repo_commit_data.append({'file_path':file_path,'simplified_code':simplified_code})
            with open(os.path.join('/home/fdse/wy/RepoCodeEdit/data/repo_commit_code',new_name,f"{commit_id[:6]}.json"),'w') as f:
                json.dump(repo_commit_data,f,indent=2)
 
if __name__ == "__main__":
    # 将数据按照 repo_name 进行划分
    # filepath = "/home/fdse/wy/RepoCodeEdit/data/retrieval/data.json"
    # data = get_data(filepath)
    # distract_data_by_repo(data)

    # 读取每一个repo.json，保存<repo,commit>对,存为repo_commit.json
    # repo_names = get_repo_names()
    # generate_repo_commit(repo_names)

    # 为每一个<repo,commit>建立json文件
    create_repo_commit_json()
    