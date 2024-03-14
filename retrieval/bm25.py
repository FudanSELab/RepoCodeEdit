from pyserini.search import LuceneSearcher
import json
import os
import sys
import subprocess
sys.path.append("../..")
from RepoCodeEdit.definitions import REPO_INDEX_PATH
from transformers import CodeLlamaTokenizer
from utils import index_pipeline
from tqdm import tqdm
import datetime


# 创建检索器对象
# searcher = LuceneSearcher('/home/fdse/zqc/fake_repo')

# 分词器
tokenizer = CodeLlamaTokenizer.from_pretrained('/home/fdse/zqc/codellama-7b')

log_path = f"/home/fdse/zqc/RepoCodeEdit/log/log_{datetime.date.today()}.txt"

# repo_paths = {"/home/fdse/zqc/RepoEdit/repos/data/raw_repos/apache/airflow":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/airflow.json",
repo_paths = {
            #   "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/celery/celery":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/celery.json",
            #   "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/conan-io/conan":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/conan.json",
            #   "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/conda/conda":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/conda.json",
            #   "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/dagster-io/dagster":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/dagster.json",
            #   "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/DataDog/integrations-core":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/integrations-core.json",
            #   "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/docker/compose":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/compose.json",
            #   "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/explosion/spaCy":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/spaCy.json",
            #   "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/gitpython-developers/GitPython":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/GitPython.json",
            #   "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/google/jax":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/jax.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/googleapis/google-cloud-python":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/google-cloud-python.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/huggingface/transformers":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/transformers.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/ipython/ipython":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/ipython.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/JohnSnowLabs/spark-nlp":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/spark-nlp.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/jupyterlab/jupyterlab":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/jupyterlab.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/kubeflow/pipelines":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/pipelines.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/Lightning-AI/lightning":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/lightning.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/mesonbuild/meson":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/meson.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/numpy/numpy":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/numpy.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/open-mmlab/mmdetection":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/mmdetection.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/pandas-dev/pandas":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/pandas.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/pantsbuild/pants":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/pants.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/PrefectHQ/prefect":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/prefect.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/pyca/cryptography":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/cryptograpthy.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/pypa/pip":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/pip.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/python/typeshed":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/typeshed.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/Qiskit/qiskit":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/qiskit.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/ray-project/ray":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/ray.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/scipy/scipy":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/scipy.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/tensorflow/models":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/models.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/tiangolo/fastapi":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/fastapi.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/twisted/twisted":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/twisted.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/wagtail/wagtail":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/wagtail.json",
              "/home/fdse/zqc/RepoEdit/repos/data/raw_repos/ytdl-org/youtube-dl":"/home/fdse/zqc/RepoEdit/repos/data/retrieval/youtube-dl.json"
              }

CONTEXT_SIZE = 13000

# 设置相似度计算方法为 BM25
# searcher.set_bm25(k1=0.82, b=0.68)

# 执行检索
# hits = searcher.search('Capital')

# print(hits)
# 打印检索结果
# for i,hit in enumerate(hits):
    # print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.6f}')

# 给定一个issue，到对应的仓库中检索文件
def retrieve(issue:str,searcher,k=10):
    results = []
    try:
        hits = searcher.search(issue,k=k)
        for hit in hits:
            results.append(hit.docid)
    except Exception as e:
        with open(log_path,'a',encoding='utf-8') as log:
            log.write("WARNING RETRIEVE EXCEPTION:\n")
            log.write(e)
    finally:
        return results
    
# 给定一个issue，到对应仓库中检索文件名，返回rank值；到对应仓库中根据文件内容检索，返回rank
def retrieve_with_ranks(issue,searcher,k=10):
    results = []
    try:
        hits = searcher.search(issue,k=k)
        for hit in hits:
            _dict = {"file_path":hit.docid,"rank":hit.score}
            results.append(_dict)
    except Exception as e:
        with open(log_path,'a',encoding='utf-8') as log:
            log.write("WARNING RETRIEVE EXCEPTION:\n")
            log.write(e)
    finally:
        return results


# 给定一个有关issue信息的json文件，得到其中每个issue的检索结果，并计算一些指标
def cal_recall(json_path,repo_path):
    total_recall = 0
    total_example = 0
    with open(json_path,'r') as f:
        jsons = json.load(f)
        total_example = len(jsons)
        for js in tqdm(jsons):
            issue = js['issue']
            commit_id = js['commit_id']
            try:
                index_path,json_path = index_pipeline(commit_id,repo_path)
                searcher = LuceneSearcher(index_path)
                searcher.set_bm25(k1=0.82, b=0.68)
            except:
                continue
            retrieved_files = retrieve(issue,searcher)
            gt = js['gt_files']
            with open(log_path,'a',encoding='utf-8') as log:
                log.write(f"ISSUE: {issue}\n")
                log.write(f"Retrieved_files : {retrieved_files}\n")
                log.write(f"Ground Truth : {gt}\n")
            retrieved_files = filter_retrieved_files(retrieved_files,context_size=CONTEXT_SIZE)
            #根据rf和gt计算单个issue的recall    
            total_recall += single_recall(retrieved_files,gt)/total_example
            with open(log_path,'a',encoding='utf-8') as log:
                log.write(f"Current Recall: {total_recall}\n\n")
                log.write("=========================================================\n\n")
            subprocess.run(["rm",json_path])
            subprocess.run(["rm","-r",index_path])
    return total_recall

# 计算单个issue的recall
def single_recall(retrieved,ground_truth):
    correct = 0
    total = len(ground_truth)
    for gt in ground_truth:
        gt = gt.split('/')
        gt = '/'.join(gt[-2:])
        for rf in retrieved:
            _rf = '/'.join(rf.split('/')[-2:])
            if gt == _rf:
                correct += 1
    return correct/total

# 给定一个BM25返回的文件列表，以及一个给定的窗口大小，把文件列表缩减到能够填满窗口
def filter_retrieved_files(retrieved_files,context_size):
    current_size = 0
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
    recall = 0
    for path in tqdm(repo_paths):
        current_repo_recall = cal_recall(repo_paths[path],path)
        recall += current_repo_recall/len(repo_paths)
        with open("/home/fdse/zqc/RepoCodeEdit/log/result.txt",'a',encoding="utf-8") as r:
            r.write(f"{path.split('/')[-1]}\n Repo Recall: {current_repo_recall}\n")
    with open("/home/fdse/zqc/RepoCodeEdit/log/result.txt",'a',encoding="utf-8") as r:
        r.write(f"Final Recall:\n{recall}")
    return recall

if __name__ == "__main__":
    print(cal_recall_for_all_repo())