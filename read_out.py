#! python3


def get_searches(fname):

    searches = [] 
    with open(fname,encoding="utf-8") as f:
        lines = f.readlines()
        
    for line in lines:
        parts = line.strip().split("\t")
        search = "%s %s" % (parts[1],parts[2])
        searches.append(search)
        
    return searches
        
searches = get_searches("out.txt")
for search in searches:
    print(search)
