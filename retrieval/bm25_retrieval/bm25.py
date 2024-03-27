from pyserini.search import LuceneSearcher
import json
import os
import sys
sys.path.append("../..")
import subprocess
from definitions import REPO_INDEX_PATH
from transformers import CodeLlamaTokenizer
from utils import content_index_pipeline,filename_index_pipeline
from tqdm import tqdm
import datetime

# 创建检索器对象
# searcher = LuceneSearcher('/home/fdse/zqc/fake_repo')

# 分词器
tokenizer = CodeLlamaTokenizer.from_pretrained('/home/fdse/zqc/codellama-7b')

log_path = f"/home/fdse/zqc/RepoCodeEdit/log/log_{datetime.date.today()}.txt"
log_w_path = f"/home/fdse/zqc/RepoCodeEdit/log/log_w_{datetime.date.today()}.txt"
log_path_wy = f"/home/fdse/wy/RepoCodeEdit/log/log_{datetime.date.today()}.txt"
log_w_path_wy = f"/home/fdse/wy/RepoCodeEdit/log/log_w_{datetime.date.today()}.txt"
# repo_paths = {"/home/fdse/zqc/RepoCodeEdit/data/raw_repos/apache/airflow":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/airflow.json",
repo_paths = {
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/apache/airflow":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/airflow.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/celery/celery":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/celery.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/conan-io/conan":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/conan.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/conda/conda":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/conda.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/dagster-io/dagster":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/dagster.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/DataDog/integrations-core":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/integrations-core.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/docker/compose":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/compose.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/explosion/spaCy":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/spaCy.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/gitpython-developers/GitPython":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/GitPython.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/google/jax":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/jax.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/googleapis/google-cloud-python":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/google-cloud-python.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/huggingface/transformers":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/transformers.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/ipython/ipython":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/ipython.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/JohnSnowLabs/spark-nlp":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/spark-nlp.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/jupyterlab/jupyterlab":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/jupyterlab.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/kubeflow/pipelines":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/pipelines.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/Lightning-AI/lightning":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/lightning.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/mesonbuild/meson":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/meson.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/numpy/numpy":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/numpy.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/open-mmlab/mmdetection":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/mmdetection.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/pandas-dev/pandas":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/pandas.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/pantsbuild/pants":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/pants.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/PrefectHQ/prefect":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/prefect.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/pyca/cryptography":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/cryptograpthy.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/pypa/pip":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/pip.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/python/typeshed":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/typeshed.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/Qiskit/qiskit":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/qiskit.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/ray-project/ray":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/ray.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/scipy/scipy":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/scipy.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/tensorflow/models":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/models.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/tiangolo/fastapi":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/fastapi.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/twisted/twisted":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/twisted.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/wagtail/wagtail":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/wagtail.json",
              "/home/fdse/zqc/RepoCodeEdit/data/raw_repos/ytdl-org/youtube-dl":"/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/youtube-dl.json"
              }

repo_paths_test = {
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/apache/airflow":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/airflow.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/celery/celery":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/celery.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/docker/compose":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/compose.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/conan-io/conan":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/conan.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/conda/conda":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/conda.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/pyca/cryptography":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/cryptography.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/dagster-io/dagster":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/dagster.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/tiangolo/fastapi":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/fastapi.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/gitpython-developers/GitPython":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/GitPython.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/googleapis/google-cloud-python":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/google-cloud-python.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/DataDog/integrations-core":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/integrations-core.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/ipython/ipython":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/ipython.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/google/jax":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/jax.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/jupyterlab/jupyterlab":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/jupyterlab.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/Lightning-AI/lightning":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/lightning.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/mesonbuild/meson":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/meson.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/open-mmlab/mmdetection":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/mmdetection.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/tensorflow/models":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/models.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/apache/mxnet":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/mxnet.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/numpy/numpy":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/numpy.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/pandas-dev/pandas":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/pandas.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/pantsbuild/pants":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/pants.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/pypa/pip":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/pip.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/kubeflow/pipelines":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/pipelines.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/PrefectHQ/prefect":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/prefect.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/Qiskit/qiskit":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/qiskit.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/ray-project/ray":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/ray.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/scipy/scipy":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/scipy.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/explosion/spaCy":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/spaCy.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/JohnSnowLabs/spark-nlp":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/spark-nlp.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/huggingface/transformers":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/transformers.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/twisted/twisted":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/twisted.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/python/typeshed":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/typeshed.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/wagtail/wagtail":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/wagtail.json",
              "/home/fdse/wy/RepoCodeEdit/data/raw_repos/ytdl-org/youtube-dl":"/home/fdse/wy/RepoCodeEdit/data/retrieval/test_data/youtube-dl.json"
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
        # print(len(hits))
        for hit in hits:
            results.append(hit.docid)
    except Exception as e:
        with open(log_path,'a',encoding='utf-8') as log:
            log.write("WARNING RETRIEVE EXCEPTION:\n")
            log.write(e)
    finally:
        return results
    
# 给定一个issue，到对应仓库中检索文件名，返回rank值；到对应仓库中根据文件内容检索，返回rank
# 要对分数进行归一化
def retrieve_with_ranks(issue,searcher,k=10):
    results = []
    max_value = 0
    min_value = 0
    try:
        hits = searcher.search(issue,k=k)
        for i in range(k):
            hits[i].score = k - i
        # for hit in hits:
        #     if hit.score>max_value:
        #         max_value = hit.score
        #     if hit.score<min_value:
        #         min_value = hit.score
        for hit in hits:
            # _dict = {"file_path":hit.docid,"rank":(hit.score-min_value)/(max_value-min_value)}
            _dict = {"file_path":hit.docid,"rank":hit.score}
            results.append(_dict)
    except:
        return results
    return results
        # with open(log_w_path,'a',encoding='utf-8') as log:
        #     log.write("WARNING RETRIEVE EXCEPTION:\n")
        #     log.write(e)

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
            gt = js['gt_files']
            try:
                index_path,json_path = content_index_pipeline(repo_path,commit_id)
            except:
                continue
            try:
                searcher = LuceneSearcher(index_path)
                searcher.set_bm25(k1=0.82, b=0.68)
            except Exception as e:
                print(e)
                subprocess.run(["rm",json_path])
                subprocess.run(["rm","-r",index_path])
                continue
            raw_retrieved_files = retrieve(issue,searcher)
            retrieved_files = filter_retrieved_files(raw_retrieved_files,context_size=CONTEXT_SIZE)
            with open(log_path_wy,'a',encoding='utf-8') as log:
                log.write(f"ISSUE: {issue}\n")
                log.write(f"Raw Retrieved_files : {raw_retrieved_files}\n")
                log.write(f"Final Retrieved_files : {retrieved_files}\n")
                log.write(f"Ground Truth : {gt}\n")
            
            #根据rf和gt计算单个issue的recall    
            total_recall += single_recall(retrieved_files,gt)/total_example
            with open(log_path_wy,'a',encoding='utf-8') as log:
                log.write(f"Current Recall: {total_recall}\n\n")
                log.write("=========================================================\n\n")
            subprocess.run(["rm",json_path])
            subprocess.run(["rm","-r",index_path])
    return total_recall

# 根据filename的rank对file_content的排名进行重排，content的权重默认为0.5
def rerank_content_by_filename(cn_list,fn_list,cn_weight=0.5):
    results = []
    for cn in cn_list:
        key = 0
        file_path = cn['file_path']
        c_score = cn['rank']
        for fn in fn_list:
            if fn['file_path'] == file_path:
                weighted_score = cn_weight*c_score + (1-cn_weight)*fn['rank']
                temp = {"file_path":file_path,"rank":weighted_score}
                results.append(temp)
                key = 1
                break
        if not key:
            weighted_score = cn_weight*c_score + (1-cn_weight)*0
            temp = {"file_path":file_path,"rank":weighted_score}
            results.append(temp)
    # 按照rank得分进行排序
    sorted_result = sorted(results, key=lambda x: x["rank"], reverse=True)
    # 将file_path单独拿出来
    string_list = []
    for sr in sorted_result:
        string_list.append(sr['file_path'])
    return string_list

# 读取json_path中的每一条数据，根据repo_path分别建立【文件名】和【文件内容】的索引，并分别建立searcher
# 根据searcher分别得到每个文件的两个rank得分，设置weight，计算加权recall指标
def cal_weighted_recall(json_path,repo_path):
    total_recall = 0
    total_example = 0
    with open(json_path,'r') as f:
        jsons = json.load(f)
        total_example = len(jsons)
        for js in tqdm(jsons):
            repo_name = js['repo_name']
            issue = js['issue']
            commit_id = js['commit_id']
            gt = js['gt_files']
            if gt:
                try:
                    fn_index_path,fn_json_path = filename_index_pipeline(repo_name,repo_path,commit_id)
                    cn_index_path,cn_json_path = content_index_pipeline(repo_path,commit_id)
                    # filename建立searcher
                    fn_searcher = LuceneSearcher(fn_index_path)
                    fn_searcher.set_bm25(k1=0.62, b=0.48)
                    # content建立searcher
                    cn_searcher = LuceneSearcher(cn_index_path)
                    cn_searcher.set_bm25(k1=0.82, b=0.68)
                except:
                    # 删除临时文件
                    if 'cn_json_path' in locals():
                        subprocess.run(["rm", cn_json_path])
                    if 'cn_index_path' in locals():
                        subprocess.run(["rm", "-r", cn_index_path])
                    if 'fn_json_path' in locals():
                        subprocess.run(["rm", fn_json_path])
                    if 'fn_index_path' in locals():
                        subprocess.run(["rm", "-r", fn_index_path])
                    continue
                retrieved_filename_with_ranks = retrieve_with_ranks(issue,fn_searcher,k=20)
                retrieved_content_with_ranks = retrieve_with_ranks(issue,cn_searcher,k=20)
                print('*'*100)
                print(len(retrieved_filename_with_ranks))
                print(len(retrieved_content_with_ranks))
                print('*'*100)
                # print('-'*90)
                # print(len(retrieved_filename_with_ranks))
                # print(len(retrieved_content_with_ranks))
                # print('-'*90)
                # with open(log_w_path_wy,'a',encoding='utf-8') as log:
                #     log.write(f"Retrieved Filename with ranks : {retrieved_filename_with_ranks}\n")
                #     log.write(f"Retrieved Content with ranks : {retrieved_content_with_ranks}\n")
                raw_retrieved_files = rerank_content_by_filename(retrieved_content_with_ranks,retrieved_filename_with_ranks,cn_weight=0.2)
                retrieved_files = filter_retrieved_files(raw_retrieved_files,context_size=CONTEXT_SIZE)
                with open(log_w_path_wy,'a',encoding='utf-8') as log:
                    log.write(f"Retrieved Filename with ranks : {retrieved_filename_with_ranks}\n")
                    log.write(f"Retrieved Content with ranks : {retrieved_content_with_ranks}\n")
                    log.write(f"ISSUE: {issue}\n")
                    log.write(f"Raw Retrieved_files : {raw_retrieved_files}\n")
                    log.write(f"Final Retrieved_files : {retrieved_files}\n")
                    log.write(f"Ground Truth : {gt}\n")
                
                #根据rf和gt计算单个issue的recall    
                total_recall += single_recall(retrieved_files,gt)/total_example
                with open(log_w_path_wy,'a',encoding='utf-8') as log:
                    log.write(f"Current Recall: {total_recall}\n\n")
                    log.write("=========================================================\n\n")
                subprocess.run(["rm",fn_json_path])
                subprocess.run(["rm","-r",fn_index_path])
                subprocess.run(["rm",cn_json_path])
                subprocess.run(["rm","-r",cn_index_path])
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
    for path in tqdm(repo_paths_test):
        current_repo_recall = cal_recall(repo_paths_test[path],path)
        recall += current_repo_recall/len(repo_paths_test)
        with open("/home/fdse/wy/RepoCodeEdit/log/bm25_result.txt",'a',encoding="utf-8") as r:
            r.write(f"{path.split('/')[-1]}\n Repo Recall: {current_repo_recall}\n")
    with open("/home/fdse/wy/RepoCodeEdit/log/bm25_result.txt",'a',encoding="utf-8") as r:
        r.write(f"Final Recall:\n{recall}")
    return recall

# 对所有仓库计算平均加权recall值
def cal_weighted_recall_for_all_repo():
    weighted_recall = 0
    for path in tqdm(repo_paths_test):
        current_repo_recall = cal_weighted_recall(repo_paths_test[path],path)
        weighted_recall += current_repo_recall/len(repo_paths_test)
        with open("/home/fdse/wy/RepoCodeEdit/log/bm25_w_new20_result.txt",'a',encoding="utf-8") as r:
            r.write(f"{path.split('/')[-1]}\n Repo Weighted Recall: {current_repo_recall}\n")
    with open("/home/fdse/wy/RepoCodeEdit/log/bm25_w_new20_result.txt",'a',encoding="utf-8") as r:
        r.write(f"Final Recall:\n{weighted_recall}")
    return weighted_recall

if __name__ == "__main__":
    # print(cal_recall_for_all_repo())
    print(cal_weighted_recall_for_all_repo())