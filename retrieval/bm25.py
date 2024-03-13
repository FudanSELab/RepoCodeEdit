from pyserini.search import LuceneSearcher
import json
import os
from RepoCodeEdit.definitions import REPO_INDEX_PATH,REPO_JSONS_PATH
from transformers import CodeLlamaTokenizer
from utils import index_pipeline
from tqdm import tqdm


# 创建检索器对象
# searcher = LuceneSearcher('/home/fdse/zqc/fake_repo')

# 分词器
tokenizer = CodeLlamaTokenizer.from_pretrained('/home/fdse/zqc/codellama-7b')

repo_paths = {"json/path":"repo_path"}

CONTEXT_SIZE = 13000

# 设置相似度计算方法为 BM25
# searcher.set_bm25(k1=0.82, b=0.68)

# 执行检索
# hits = searcher.search('Capital')

# print(hits)
# 打印检索结果
# for i,hit in enumerate(hits):
    # print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.6f}')

# 给定一个json文件，在某个commit下，读取其中的issue，并到对应的仓库中检索文件
def retrieve(issue:str,searcher):
    results = []
    hits = searcher.search(issue)
    for hit in hits:
        results.append(hit.docid)
    return results    

# 给定一个有关issue信息的json文件，得到其中每个issue的检索结果，并计算一些指标
def cal_recall(json_path,repo_path):
    total_recall = 0
    total_example = 0
    with open(json_path,'r') as f:
        jsons = json.load(f)
        total_example = len(jsons)
        repo_name = jsons[0]['repo_name']
        index_path = os.path.join(REPO_INDEX_PATH,repo_name)
        searcher = LuceneSearcher(index_path)
        for js in tqdm(jsons):
            issue = js['issue']
            commit_id = js['base_commit']
            index_path = index_pipeline(commit_id,repo_path)
            searcher = LuceneSearcher(index_path)
            searcher.set_bm25(k1=0.82, b=0.68)
            retrieved_files = retrieve(issue,searcher)
            gt = js['gt_files']  
            retrieved_files = filter_retrieved_files(retrieved_files,context_size=CONTEXT_SIZE)
            #TODO 根据rf和gt计算单个issue的recall    
            total_recall = single_recall(retrieved_files,gt)/total_example
    return total_recall

# 计算单个issue的recall
def single_recall(retrieved,ground_truth):
    correct = 0;
    total = len(ground_truth)
    for gt in ground_truth:
        if gt in retrieved:
            correct += 1
    return correct/total

# 给定一个BM25返回的文件列表，以及一个给定的窗口大小，把文件列表缩减到能够填满窗口
def filter_retrieved_files(retrieved_files,context_size):
    current_size = 0;
    filtered_files = []
    for file in retrieved_files:
        code_tokens = count_token(file)
        if current_size+code_tokens<context_size:
            filtered_files.append(file)
            current_size += code_tokens
        else:
            break
    return filtered_files

# 计算一个文件含有多少个token(使用LlamaTokenizer)
def count_token(code_file):
    with open(code_file,'r') as f:
        content = f.read()
        tokenized_content = tokenizer.tokenize(content)
        return len(tokenized_content)

# 对所有仓库计算平均recall值
def cal_recall_for_all_repo():
    recall = 0;
    for path in tqdm(repo_paths):
        recall += cal_recall(path,repo_paths[path])/len(repo_paths)
    return recall