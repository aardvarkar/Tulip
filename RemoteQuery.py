import webbrowser
import requests
import base64

raw=requests.get("https://raw.githubusercontent.com/marcottelab/AG3C_starvation_tc/master/operon_analysis/GeneProductSet.txt")
with open("convertedOutput.txt","w") as file_convert:
        for cnt, line in enumerate(raw):
                file_convert.write(line)
#webbrowser.open("http://david.abcc.ncifcrf.gov/api.jsp?type=OFFICIAL_GENE_SYMBOL&ids=caiF,caiE,caiD,caiC,caiB,caiA,caiT,fixA,fixB,fixC,&tool=summary&annot=GOTERM_BP_ALL,GOTERM_CC_ALL,GOTERM_MF_ALL,")
