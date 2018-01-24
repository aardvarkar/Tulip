import sys
import csv

for i in range(1,11):
    
    
    input_list=[]
    input_file="input"+str(i)+".txt"
    with open(input_file,"r") as file1:
        for cnt, line in enumerate(file1):
            gene_id=line[:-1]
            input_list.append(gene_id)

    output_list=[]
    convert_file="GeneProductSet.txt"
    count=0
    with open(convert_file,"r") as file2:
        file2_content=csv.reader(file2, delimiter='\t')
        for line in file2_content:
            if line[0] in input_list:
                output_list.append(line[1])

    with open("output"+str(i)+".txt","w") as file3:
        for i in output_list:
            file3.write(i + "\n")
