from pyserini.search import LuceneSearcher

# 创建检索器对象
searcher = LuceneSearcher('/home/fdse/zqc/fake_repo')

# 设置相似度计算方法为 BM25
searcher.set_bm25(k1=0.82, b=0.68)

# 执行检索
hits = searcher.search('Capital')

print(hits)
# 打印检索结果
for i,hit in enumerate(hits):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.6f}')
