import json

# 抽取 Patch中的文件名，存储为列表
def extract_files_in_patch(patch):
    modified_files = set()
    lines = patch.split('\n')
    for line in lines:
        if line.startswith('---'):
            if len(line.split(None, 1)) >= 2:
                file_path = line.split(None, 1)[1].strip()
                modified_files.add(file_path)
    return list(modified_files)

# 读取train.json中的所有数据
def get_data(filepath):
    # 打开 train.json文件读取数据
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
    return data

# 生成检索需要的数据
def generate_retrieval_data(raw_data):
    data = []
    for d in raw_data:
        temp = {}
        temp['repo_name'] = d['repo']
        temp['issue'] = d['problem_statement']
        temp['commit_id'] = d['base_commit']
        temp['gt_files'] = extract_files_in_patch(d['patch'])
        data.append(temp)
    # 存入json文件
    json_str = json.dumps(data, indent=4)  # indent 参数用于指定缩进格式，可选项
    with open('../../data/retrieval/data.json', 'w') as json_file:
        json_file.write(json_str)

if __name__ == '__main__':
    file_path = '../../data/SWE-bench_bm25_13K/train.json'
    data = get_data(file_path)
    generate_retrieval_data(data)
