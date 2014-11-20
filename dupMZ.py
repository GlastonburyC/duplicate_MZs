# Set up neccessary variables
import sys
mz={}
sample=[]
sample_index=[]
sample_id=[]
new_header=[]
header_mz=[]
header_sample=[]
 
info=["SNP","A1","A2"]
x=sys.argv[1]
 
# Load a list of MZ twins that need to be duplicated. Column[1] = co-twin not genotyped, Column[0] = twin present in gen file.
with open("MZs_to_duplicate.txt",'r') as mz_duplication_list:
    header_mz=next(mz_duplication_list)
    for line in (line.strip().split() for line in mz_duplication_list):
        mz[line[0]]= line[1]
 
#open the sample file which acts as a header for the .gen file
with open("merge.chr19.pos1-5000000.sample.txt",'r') as sample_file:
    header_sample=next(sample_file)
    for line in (line.strip().split() for line in sample_file):
        sample.append(line[0])
# Find the index position of every MZ that needs to be duplicated in the sample file. Add 3 to 'correct' the index for gen file
# Create a list sample_id that records what the new sample file will look like with the duplicate twins.
with open("header%s.txt"%x,'w') as header:
    header.write("\n".join(str(x) for x in info)+"\n")
    for i,j in enumerate(sample):
        header.write(j+'\n')
        for item in mz.keys():
            if j == item:
                sample_index.append(i+3)
                header.write(mz[item]+'\n')
 
with open("header%s.txt"%x,'r') as new_header_file:
    for line in (line.strip().split() for line in new_header_file):
        new_header.append(line[0])
#open the .gen file and the new output .gen file. For each line, if the index position matches the sample_index 
# (corresponding to a MZ that needs duplicating) write that column twice, else write it once.
with open("chr%s.bimbam"%x,'r') as genfile:
    with open("chr%s_MZadded.bimbam"%x,'w') as genout:
        genout.write(','.join(new_header) + '\n')
        for line in genfile:
            line = line.rstrip()
            fields=line.split(",")
            for index in range(0,len(fields)):
                if index in sample_index:
                    genout.write(","+fields[index]+","+fields[index])
                else:
                    if index == 0:
                        genout.write(fields[index])
                    else:
                        genout.write(","+fields[index])
            genout.write('\n')
            
