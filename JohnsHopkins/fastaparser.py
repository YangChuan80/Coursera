filename='dna1.fasta'
try:
    f=open(filename)

except IOError:
    print('Cannot find this file!')

seq={}
for line in f:
    line=line.rstrip()

    if line[0]=='>':
        words=line.split()
        name=words[0][1:]
        seq[name]=''

    else:
        seq[name]=seq[name]+line
f.close()



     

k=list(seq.keys())

longest=0
shortest=100000000

seq_orf={}
for name, sequence in seq.items():
    if longest<len(sequence):
        longest=len(sequence)

    if shortest>len(sequence):
        shortest=len(sequence)

    frame1=sequence[0:]
    frame2=sequence[1:]
    frame3=sequence[2:]

    frame=frame3
    
    #//////detect the ORF////////////////////////

    judge=0
    seq_orf[name]=[]
    start_judge=0
    
    for i in range(0, len(frame), 3):
        if frame[i:i+3]=='ATG' and start_judge==0:
            start=i
            judge=1
            start_judge=1
          
        if (frame[i:i+3]=='TAA' or frame[i:i+3]=='TAG' or frame[i:i+3]=='TGA') and judge==1:
            end=i+3
            seq_orf[name].append(frame[start:end])
            
            judge=0
            start_judge=0
            
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#///////////////////////////////////////////////////////
            
longest_orf=0
shortest_orf=100000000

for name, orf_list in seq_orf.items():
    for orf in orf_list:
        if longest_orf<len(orf):
            longest_orf=len(orf)
            longest_name=name
            longest_seq=orf

        if shortest_orf>len(orf):
            shortest_orf=len(orf)
question_list=seq_orf['gi|142022655|gb|EQ086233.1|97']

for l in question_list:
    print('lenght is: ', len(l))



print('Longest Sequence: ', longest)
print('Shortest Sequence: ', shortest)
print('Longest ORF: ', longest_orf)
#print('Longest Reverse ORF: ', longest_reverse_orf)
print('Longest ORF name: ', longest_name)

print('Position of Longest ORF: ', seq[longest_name].find(longest_seq))

#print('gi|142022655|gb|EQ086233.1|97: ', l)
            
seq_list=list(seq.values())
'''
print(len(seq_list))

repeat_list=[]

for seq in seq_list:
    for i in range(len(seq)):
        repeat=seq[i:i+7]
        repeat_list.append(repeat)

repeat_set=set(repeat_list)
print(len(repeat_set))

count_list=[]
s_freq={}


for s in list(repeat_set):
    s_freq[s]=0
    for seq in seq_list:
        for i in range(len(seq)-7):
            if s == seq[i:i+7]:
                s_freq[s]+=1

l=list(s_freq.values()).sort()
                

'''



        
    

