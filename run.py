import subprocess #For executing tree package using python
import os #For cd into my home directory
import cjson #For parsing json output
import pprint #For fancy output of stats

os.chdir('/home/k/')

#receive an output as Json of tree package
result = subprocess.check_output(['tree', '-afJs'], stderr=subprocess.STDOUT)

#dictionary of lists
#KEYS - levels of recursion
#First value in list - Number of directories
#Second value in list - Number of files
#Third value in list - Files total size per level
stats = {}

#Counter for recursion level
counter = 0

tree = cjson.decode(result)

def count_values(tree):
    global counter
    global stats
    for i in tree:
        if i and not 'error' in i:
            if i["type"] == "directory":
                if counter in stats:
                    stats[counter][0] += 1
                else:
                    stats[counter] = [0, 0, 0]
                    stats[counter][0] += 1
                counter += 1
                count_values(i['contents'])
            if i["type"] == "file":
                if counter in stats:
                    stats[counter][1] += 1
                    stats[counter][2] += i['size']
                else:
                    stats[counter] = [0, 0, 0]
    counter -= 1

with open('/home/k/workfile', 'w') as f:
     f.write(cjson.encode(tree))

count_values(tree)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(stats)