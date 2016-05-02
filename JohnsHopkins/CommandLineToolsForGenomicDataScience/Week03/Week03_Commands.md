# Week 03
### 1. How many sequences were in the genome?

`$ more wu_0.v7.fas | grep '>' | wc -l`

**Answer: 7**

### 2. What was the name of the third sequence in the genome file? Give the name only, without the “>” sign.

`$ more wu_0.v7.fas | grep '>' `

**Answer: Chr3**

### 3. What was the name of the last sequence in the genome file? Give the name only, without the “>” sign.

`$ more wu_0.v7.fas | grep '>' `

**Answer: mitochondria**

### 4. How many index files did the operation create?

> $ **bowtie2-build**  [reference_fasta_file.fasta]  [index_file]

`$ mkdir idx`

`$ bowtie2-build wu_0.v7.fas idx/wu_0_idx`

**Answer: 6**

## 5. What is the 3-character extension for the index files created?

**Answer: bt2**

### 6. How many reads were in the original fastq file?

`$ more wu_0_A_wgs.fastq | wc -l`

**Answer: 147354**

### 7. How many matches (alignments) were reported for the original (full-match) setting? Exclude lines in the file containing unmapped reads.

> $ **bowtie2-p** 4 **-x**  [fasta_index_file]  **-U**  [in.fastq]  **-S**  [out.sam]

`$ bowtie2 -p 4 -x idx/wu_0_idx -U wu_0_A_wgs.fastq -S out.full.sam`

- Results: 
    
    147354 reads; of these:

    147354 (100.00%) were unpaired; of these:

    9635 (6.54%) aligned 0 times

    93780 (63.64%) aligned exactly 1 time

    43939 (29.82%) aligned >1 times

    93.46% overall alignment rate


**Answer: 137719**

### 8. How many matches (alignments) were reported with the local-match setting? Exclude lines in the file containing unmapped reads.

`$ bowtie2 -p 4 -x idx/wu_0_idx -U wu_0_A_wgs.fastq -S out.local.sam --local`

- Results: 
    147354 reads; of these:

    147354 (100.00%) were unpaired; of these:

    6310 (4.28%) aligned 0 times

    84939 (57.64%) aligned exactly 1 time

    56105 (38.07%) aligned >1 times

    95.72% overall alignment rate

Then do:

- SAM to BAM

> $ **samtools view -bT** [reference_fasta_file.fasta] [in.sam] **>** [out.bam]

`samtools view -bT wu_0.v7.fas out.full.sam > out.full.bam`

`samtools view -bT wu_0.v7.fas out.local.sam > out.local.bam`


- Sort BAM

> $ **samtools sort** [original.bam] **-o** [sorted.bam]

`samtools sort out.full.bam -o out.full.sorted.bam`

`samtools sort out.local.bam -o out.local.sorted.bam`


- Index BAM

> $ **samtools index** [sorted.bam]

`samtools index out.full.sorted.bam`

`samtools index out.local.sorted.bam`

**Answer: 141044**

### 9. How many reads were mapped in the scenario in Question 7?

**Answer:  137719**

### 10. How many reads were mapped in the scenario in Question 8?

- Same to the Q7 & Q8

**Answer: 141044**


### 11. How many reads had multiple matches in the scenario in Question 7? 

`43939 (29.82%) aligned >1 times`

### 12. How many reads had multiple matches in the scenario in Question 8? Use the format above. You can တ†nd this in the bowtie2 summary; note that by default bowtie2 only reports the best match for each read.

`56105 (38.07%) aligned >1 times`

### 13. How many alignments contained insertions and/or deletions, in the scenario in Question 7?

- Use **CIGAR** sections to solve this:

`$ cat out.full.sam | grep -v '^#' | cut -f6 | grep 'D' | wc -l`


`$ cat out.full.sam | grep -v '^#' | cut -f6 | grep 'I' | wc -l`

`$ cat out.full.sam | grep -v '^#' | cut -f6 | grep 'D' | grep 'I' | wc -l`

- line1 + line2 - line3

**Answer: 1429 + 1395 - 42 = 2782**

### 14. How many alignments contained insertions and/or deletions, in the scenario in Question 8?

`$ cat out.local.sam | grep -v '^#' | cut -f6 | grep 'D' | wc -l`


`$ cat out.local.sam | grep -v '^#' | cut -f6 | grep 'I' | wc -l`

`$ cat out.local.sam | grep -v '^#' | cut -f6 | grep 'D' | grep 'I' | wc -l

- line1 + line2 - line3

**Answer: 1223 + 1476 - 85 = 2614**

### 15. How many entries were reported for Chr3?
- Perform M Pile Up

> $ **samtools mpileup -f**  [reference.fasta]  **-uv**  [sorted_indexed.bam]  **>**  [candidate_entry_vcf_file.vcf]

- Above is the candidate variant vcf file.

`$ samtools mpileup -f wu_0.v7.fas -uv out.full.sorted.bam > out.full.mpileup.vcf`

`$ samtools mpileup -f wu_0.v7.fas -uv out.local.sorted.bam > out.local.mpileup.vcf`

- Then count the number:

`$ cat out.full.mpileup.vcf | grep -v '^#' | cut -f1 | grep 'Chr3' | wc -l`

**Answer: 360295**

### 16. How many entries have ‘A’ as the corresponding genome letter?

`$ cat out.full.mpileup.vcf | grep -v '^#' | cut -f4 | grep '^A$' | wc -l`

**Answer: 1150985**

### 17. How many entries have exactly 20 supporting reads (read depth)?

`$ cat out.full.mpileup.vcf | grep -v '^#' | cut -f8 | grep 'DP=20' | wc -l`

**Answer: 1816**

### 18. How many entries represent indels?

`$ cat out.full.mpileup.vcf | grep -v '^#' | cut -f8 | grep 'INDEL' | wc -l`

**Answer: 1972**

### 19. How many entries are reported for position 175672 on Chr1?

`$ cat out.full.mpileup.vcf | grep -v '^#' | cut -f1,2 | grep 'Chr1' | cut -f2 | grep '^175672$' | wc -l `

*Answer: 2*

### 20. How many variants are called on Chr3?

- First, we should build BCF file.
- Second, we use BCFTools call to generate a variant VCF file.

 > $ **samtools mpileup -f**  [reference.fast]  **-g**  [sorted_indexed.bam]  **>**  [variant.bcf]

`$ # Build BCF`

`$ samtools mpileup -f wu_0.v7.fas -g out.full.sorted.bam > out.full.mpileup.bcf`

`$ samtools mpileup -f wu_0.v7.fas -g out.local.sorted.bam > out.local.mpileup.bcf`

`$ # Call Variants`

> $ **bcftools call**  -m -v -O v [variant.bcf]  **>**  [variant_call_format_file.vcf]

`$ bcftools call -m -v -O v out.full.mpileup.bcf > out.full.vcf`

`$ bcftools call -m -v -O v out.full.mpileup.bcf > out.local.vcf`

- Then count the 'Chr3'

`$ cat out.full.vcf | grep -v '^#' | cut -f1 | grep 'Chr3' | wc -l`

**Answer: 398**

### 21. How many variants represent an A->T SNP? If useful, you can use ‘grep –P’ to allow tabular spaces in the search term.

`$ cat out.full.vcf | grep -v '^#' | cut -f4-5 | grep -P '^A\tT$' | wc -l`

**Answer: 392**

### 22. How many entries are indels?

`$ cat out.full.vcf | grep -v '^#' | cut -f8 | grep 'INDEL' | wc -l`

**Answer: 320**

### 23. How many entries have precisely 20 supporting reads (read depth)?

`$ cat out.full.vcf | grep -v '^#' | cut -f8 | grep 'DP=20' | wc -l`

**Answer: 2**

### 24. What type of variant (i.e., SNP or INDEL) is called at position 11937923 on Chr3?

`$ cat out.full.vcf | grep -v '^#' | cut -f1,2,4,5 | grep 'Chr3' | cut -f2,3,4 | grep '11937923'`

`11937923	G	A`

**Answer: SNP**
