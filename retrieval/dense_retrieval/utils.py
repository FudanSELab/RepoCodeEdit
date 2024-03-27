import json
import os
import ast
import sys
import subprocess

sys.path.append("../..")

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

# 给定repo_name获得repo_path
def get_repo_path(repo_name):
    repo_path = "/home/fdse/wy/RepoCodeEdit/data/raw_repos/" + repo_name
    return repo_path

# 切换某个仓库的状态到某个commit下
def switch2commit(repo_path,commit_id):
    subprocess.run(["sh","change_commit.sh",repo_path,commit_id])

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
def get_repo_code(repo_path):
    result = []
    py_files = get_repo_files(repo_path)
    for file in py_files:
        with open(file,'r',encoding='utf-8') as py:
            try:
                code = py.read()
            except:
                continue
            js = {"file_path":file,"code":code}
            result.append(js)
    return result

# 抽取python代码中的class和method
def extract_classes_and_functions(code):
    classes = set()
    functions = set()
    # 解析 Python 代码成 AST
    try:
        tree = ast.parse(code)
    except:
        return 0,0
    # 遍历 AST，提取所有函数定义和类定义
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            classes.add(class_name)
        elif isinstance(node, ast.FunctionDef):
            function_name = node.name
            functions.add(function_name)
    return list(classes),list(functions)
    