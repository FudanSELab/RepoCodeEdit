input=$1
index=$2

python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input $input \
  --index $index \
  --generator DefaultLuceneDocumentGenerator \
  --threads 1 \
  --storePositions --storeDocvectors --storeRaw