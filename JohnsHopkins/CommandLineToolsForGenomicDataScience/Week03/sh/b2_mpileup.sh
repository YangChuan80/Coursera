# M Pile up to VCF
samtools mpileup -f wu_0.v7.fas -uv out.full.sorted.bam > out.full.mpileup.vcf
samtools mpileup -f wu_0.v7.fas -uv out.local.sorted.bam > out.local.mpileup.vcf
