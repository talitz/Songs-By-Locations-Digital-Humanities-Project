import xml.etree.ElementTree
import pdb
def get_stanza_text(stanzas):
    ret=[]
    for stanza in stanzas:
        string=""
        for line in range(len(stanza)):
            string=string+stanza[line].text.lstrip().rstrip()+'\n'
        ret.append(string)
    return ret

def get_tree_stanzas(path):
    try:
        e = xml.etree.ElementTree.parse(path).getroot()[1][0][0]
    except:
        return []
    i=0
    ret=[]
    for x in e.findall('{http://www.tei-c.org/ns/1.0}lg'):
        i=i+1
        ret.append(x)
    return ret

def main():
	subdirectories = [d for d in os.listdir('./') if os.path.isdir(os.path.join('./', d))]
    for artists in subdirectories:
	    artist = os.listdir(artists)
	    for song in artist:
	        print song
	        if song != '.DS_Store': 
	            if artists != '.settings':
	                path='./'  + artists +'/'+ song
	                print path
	                arr = get_stanza_text(get_tree_stanzas(path))
	                pdb.set_trace()

if __name__ == "__main__":
    main()