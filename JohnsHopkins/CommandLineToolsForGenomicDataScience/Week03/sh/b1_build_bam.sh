# Aligning
bowtie2 -p 4 -x idx/wu_0_idx -U wu_0_A_wgs.fastq -S out.full.sam
bowtie2 -p 4 -x idx/wu_0_idx -U wu_0_A_wgs.fastq -S out.local.sam --local

# SAM to BAM
samtools view -bT wu_0.v7.fas out.full.sam > out.full.bam
samtools view -bT wu_0.v7.fas out.local.sam > out.local.bam

# Sort BAM
samtools sort out.full.bam -o out.full.sorted.bam
samtools sort out.local.bam -o out.local.sorted.bam

# Index BAM
samtools index out.full.sorted.bam
samtools index out.local.sorted.bam
