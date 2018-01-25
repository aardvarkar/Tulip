import sys
import csv
import requests
import os.path
import webbrowser

'''
Pour une liste de genes, affiche dans une page web l'enrichissement de ces genes. Il est possible dans la page web de selectionner le bon organisme si il y a ambiguite.
'''

convertFileName = "GeneProductSet.txt"

if not os.path.isfile(convertFileName):
    rawFile=requests.get("https://raw.githubusercontent.com/marcottelab/AG3C_starvation_tc/master/operon_analysis/GeneProductSet.txt")
    with open(convertFileName,"w") as file_convert:
      for cnt, line in enumerate(rawFile):
        print(line)
        file_convert.write(line)
    file_convert.close()

input_list=[]
input_file=sys.argv[1]
with open(input_file,"r") as file1:
    for cnt, line in enumerate(file1):
        gene_id=line[:-1]
        input_list.append(gene_id)


outputList=[]
count=0
convertFile = open(convertFileName,"r")
convertFileContent=csv.reader(convertFile, delimiter='\t')

for line in convertFileContent:
    if line[0] in input_list:
      outputList.append(line[1])

url = "http://david.abcc.ncifcrf.gov/api.jsp?type=OFFICIAL_GENE_SYMBOL&ids="
for gene in outputList:
    url += gene + ","
url += "&tool=summary&annot=GOTERM_BP_ALL,GOTERM_CC_ALL,GOTERM_MF_ALL,"
webbrowser.open(url)
