import json

with_suffix = True


gt_total_file = 0
gt_key_words_in_issue = 0

total_example = 0
gtwords_mentioned_in_issue = 0
with open('/home/fdse/zqc/RepoEdit/repos/data/retrieval/data.json','r') as f:
    jsons = json.load(f)
    total_example = len(jsons)
    for js in jsons:
        ground_truth = js['gt_files']
        issue = js['issue']
        gt_total_file += len(ground_truth)
        mentioned_flag = False
        for gt in ground_truth:
            key_words = gt.split('/')[-1]
            if not with_suffix:
                key_words = key_words.split('.')[0]
                # print(key_words)
            if key_words in issue:
                gt_key_words_in_issue += 1
                mentioned_flag = True
        if mentioned_flag:
            gtwords_mentioned_in_issue += 1

print("是否考虑后缀名(.py等):",with_suffix)
print("Ground Truth的文件数量:",gt_total_file)
print("Ground Truth文件中，文件名在issue中被提到的文件数量",gt_key_words_in_issue)
print("Issue的样本数量:",total_example)
print("Ground Truth文件中，文件名在issue中被提到的样本数量:",gtwords_mentioned_in_issue) 