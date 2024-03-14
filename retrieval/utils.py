import json
import sys
sys.path.append("../..")
import os
import subprocess
from RepoCodeEdit.definitions import REPO_INDEX_PATH,REPO_JSONS_PATH,REPO_FJSONS_PATH

# 获取一个仓库的所有.py文件的路径
def get_repo_files(repo_path):
    results = []
    items = os.listdir(repo_path)
    for item in items:
        item_path = os.path.join(repo_path,item)
        if os.path.isdir(item_path):
            results.extend(get_repo_files(item_path))
        else:
            if item_path.endswith('.py'):
                results.append(item_path)
    return results

# 把一个仓库的所有.py文件装入一个json中,id为其文件路径，content为代码内容
def py2json(repo_path):
    jsons = []
    py_files = get_repo_files(repo_path)
    for file in py_files:
        with open(file,'r',encoding='utf-8') as py:
            content = py.read()
            js = {"id":file,"contents":content}
            jsons.append(js)
    return jsons

# 把一个json文件中的json写入一个仓库路径下
def create_json_file(jsons,repo_name,commit_id):
    json_path = os.path.join(REPO_JSONS_PATH,f"{repo_name}_{commit_id[:6]}.json")
    with open(json_path,'w',encoding='utf-8') as out:
        json.dump(jsons,out,indent=2)
    return json_path

# 使用create_index.sh脚本为指定仓库创建一个索引用于检索
def create_index(repo_json_path,repo_name,commit_id,filename=False):
    suffix = ""
    if filename:
        suffix = "filename"
    index_path = os.path.join(REPO_INDEX_PATH,f"{repo_name}_{suffix}_{commit_id}")
    subprocess.run(["sh","./create_index.sh",repo_json_path,index_path])
    return index_path

# 给定某个仓库及commit_id，为该状态的仓库建立索引
def content_index_pipeline(commit_id,repo_path):
    switch2commit(commit_id,repo_path)
    json_path = create_json_file(py2json(repo_path),repo_path.split('/')[-1],commit_id)
    return create_index(REPO_JSONS_PATH,repo_path.split('/')[-1],commit_id),json_path

# 给定某个仓库及commit_id，为该状态下仓库中的文件名建立索引
def filename_index_pipeline(commit_id,repo_path):
    switch2commit(commit_id,repo_path)
    json_path = repo_filename2doc(repo_path,repo_name,commit_id)
    return create_index(REPO_JSONS_PATH,repo_path.split('/')[-1],commit_id,True),json_path


# 切换某个仓库的状态到某个commit下
def switch2commit(repo_path,commit_id):
    subprocess.run(["sh","change_commit.sh",repo_path,commit_id])

# 给定某个仓库，获得仓库下所有的文件名，并把文件名们单独作为一个文档放进json中
def repo_filename2doc(repo_path,repo_name,commit_id):
    jsons = []
    repo_files = get_repo_files(repo_path)
    for filename in repo_files:
        js = {"id":filename,"content":'/'.join(filename.split('/')[-2:])}
        jsons.append(js)
    output_path = os.path.join(REPO_FJSONS_PATH,f"{repo_name}_filenames_{commit_id[:6]}.json")
    with open(output_path,'w',encoding='utf-8') as f:
        json.dump(jsons,f,indent=2)
    return output_path

if __name__ == "__main__":
    index_pipeline('/home/fdse/zqc/fake_repo')