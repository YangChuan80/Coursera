# Build BCF
samtools mpileup -f wu_0.v7.fas -g out.full.sorted.bam > out.full.mpileup.bcf
samtools mpileup -f wu_0.v7.fas -g out.local.sorted.bam > out.local.mpileup.bcf

# Call Variants
bcftools call -m -v -O v out.full.mpileup.bcf > out.full.vcf
bcftools call -m -v -O v out.full.mpileup.bcf > out.local.vcf
