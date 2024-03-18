import json
import os

repo_jsons = {}
with open('/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons/data.json') as f:
    jsons = json.load(f)
    for js in jsons:
        repo_name = js['repo_name']
        new_js = {"repo_name":repo_name,"issue":js['issue'],"commit_id":js["commit_id"],"gt_files":js["gt_files"]}
        if repo_name in repo_jsons:
            repo_jsons[repo_name].append(new_js)
        else:
            repo_jsons[repo_name] = [new_js]

for repo_name in repo_jsons:
    new_name = repo_name.split('/')[-1]
    with open(os.path.join('/home/fdse/zqc/RepoCodeEdit/data/repo_data_jsons',f"{new_name}.json"),'w') as f:
        json.dump(repo_jsons[repo_name],f,indent=2)
