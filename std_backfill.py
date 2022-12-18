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
from jycm.helper import make_ignore_order_func
from jycm.jycm import YouchamaJsonDiffer
from jycm.helper import dump_html_output, open_url
from jycm.jycm import YouchamaJsonDiffer
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
                jsons[c]=data
                c = c + 1
            else:
                data1 = json.load(json_file)
       
        # Print the type of data variable
        print("Type:", type(data))
    
        # Print the data of dictionary
        print("\nPeople1:", data['meta'])
        #print("\nPeople2:", data['people2'])
        print("Type:", type(data['certification']['peak acceleration']))
print(len(jsons), " " , jsons)
# for i, jsn in jsons:
#     print(i, " ", jsn)
left = jsons[0]
right = jsons[1]
ycm = YouchamaJsonDiffer(left, right)

diff_result = ycm.get_diff() # new API

# legacy usage:
# ycm.diff()
# diff_result = ycm.to_dict()

# you can find generated html in the folder
output_dir = "/Users/xxx/jycm-example-1"
# you can directly view it by clicking the index.html file inside the folder
url = dump_html_output(left, right, diff_result, BASEDIR+"\\diff")

# if you want to open it from python
open_url(url)