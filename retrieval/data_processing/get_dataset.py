from datasets import load_dataset

def download_dataset(dataset_name):
    # 使用 load_dataset 函数加载数据集
    dataset = load_dataset(dataset_name)
    return dataset

if __name__ == '__main__': 
    # 获取 Huggingface上的数据集
    dataset_name = "princeton-nlp/SWE-bench_bm25_13K"
    dataset = download_dataset(dataset_name)
    print(type(dataset))



