## This script normalizes jsons in a folder to attain powerbi dataset friendly
# It takes the file with the most attributes and prepares a master hashmap and 
# uses it on all the remaining files to have a standard attribute set by means 
# backfill in either direction i.e., source to destination as well as 
# destination to source whenever it learns that the other file has additional 
# attributes or lack of it.
# PS: this script is attribute agnostic, however script assumes that json has 
# the base list of attributes.

BASEDIR = 'c:\\Users\\dev\\Projects\\kpi-backfill'

from pathlib import Path
import json
import shutil
from jycm.helper import make_ignore_order_func
from jycm.jycm import YouchamaJsonDiffer
from jycm.helper import dump_html_output, open_url


def empty_vals(json_elem):
    if isinstance(json_elem, list):
        return [empty_vals(elem) for elem in json_elem]
    elif isinstance(json_elem, dict):
        return {key: empty_vals(value) for key, value in json_elem.items()}
    else:
        if isinstance(json_elem, int):
            return 0 
        elif isinstance(json_elem, float):
            return 0.0
        elif isinstance(json_elem, str):
            return ""
        else:
            return json_elem
        
# iterate over files in
# that directory
data = {}
data1 = {}
jsons = {}
files = Path(BASEDIR).glob('*.*')
c=0
for file in files:
    if  '.git' not in file.name and '.py' not in file.name:
        print(file)
        with open(file) as json_file:
            if '.json' in file.name:
                data = json.load(json_file)
                jsons[c] = data
                c = c + 1
                # Print the type of data variable
                print("Type:", type(data))
            
                # Print the data of dictionary
                print("\nPVehicle:", data['meta'])
                print("Type:", type(data['certification']['peak acceleration']))

print(len(jsons), " " , jsons)
# for i, jsn in jsons:
#     print(i, " ", jsn)
left = jsons[0]
right = jsons[1]
ycm = YouchamaJsonDiffer(left, right)

diff_result = ycm.get_diff() # new API
print("Type diff_result:", type(diff_result))
for diff in dict(diff_result):
    #print(type(diff), " ", str(diff.replace(':','')), " ", diff_result[diff])
    out_file = open(BASEDIR+"\\"+str(diff.replace(':',''))+".txt", "w")
    json.dump(diff_result[diff], out_file, indent=4, skipkeys=True,sort_keys=True)

## take just4vispairs.txt as json and backfill both the files
diff_data=[]
with open('just4vispairs.txt') as json_file:
    diff_data = json.load(json_file)

for diff in diff_data:
    print(diff['left'], " ", diff['right'], " : ", type(diff['left']), " - ", type(diff['right']))
    if "str" in str(type(diff['left'])):
        if "__NON_EXIST__" in diff['left']:
            patch = {diff['right_path']: diff['right']}
            #print("left side", left, " -- ", patch)
            left.update(empty_vals(patch))
    if "str" in str(type(diff['right'])):
        if "__NON_EXIST__" in diff['right']:
            patch = {diff['left_path']: diff['left']}
            #print("right side", right, " -- " , patch)
            right.update(empty_vals(patch))

# normalized files are here.
left_file = open(BASEDIR+"\\left.txt", "w")
json.dump(left, left_file, indent=4, skipkeys=True)
right_file = open(BASEDIR+"\\right.txt", "w")
json.dump(right, right_file, indent=4, skipkeys=True)

dirpath = Path(BASEDIR+"\\diff") # / BASEDIR+"\\diff"
if dirpath.exists() and dirpath.is_dir():
    shutil.rmtree(dirpath)
# you can directly view it by clicking the index.html file inside the folder
url = dump_html_output(left, right, diff_result, BASEDIR+"\\diff")

# if you want to open it from python
open_url(url)