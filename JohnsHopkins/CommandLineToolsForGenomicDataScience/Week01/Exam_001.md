# Week 1 Exam
1. How many chromosomes are there in the genome?
$ grep '>' apple.genome | wc -l
Answer: 3

2. How many genes?
$ cut -f1 apple.genes | sort -u | wc -l
Answer: 5453

3. How many transcript variants?
$ cut -f2 apple.genes | sort -u | wc -l
Answer: 5456

4. How many genes have a single splice variant?
$ cut -f1 apple.genes | uniq -c | grep ' 1 ' | wc -l
Answer: 5450

5. How may genes have 2 or more splice variants?
$ cut -f1 apple.genes | uniq -c | grep -v ' 1 ' | wc -l
Answer: 3

6. How many genes are there on the ‘+’ strand?
$ cut -f1,4 apple.genes | sort -u | grep '+' | wc -l
Answer: 2662

7. How many genes are there on the ‘-’ strand?
$ cut -f1,4 apple.genes | sort -u | grep '-' | wc -l
Answer: 2791

8. How many genes are there on chromosome chr1?
$ cut -f1,3 apple.genes | sort -u | grep 'chr1' | wc -l
Answer: 1624

9. How many genes are there on each chromosome chr2?
$ cut -f1,3 apple.genes | sort -u | grep 'chr2' | wc -l
Answer: 2058

10. How many genes are there on each chromosome chr3?
$ cut -f1,3 apple.genes | sort -u | grep 'chr3' | wc -l
Answer: 1771

11. How many transcripts are there on chr1?
$ cut -f2,3 apple.genes | sort -u | grep 'chr1' | wc -l
Answer: 1625

12. How many transcripts are there on chr2?
$ cut -f2,3 apple.genes | sort -u | grep 'chr2' | wc -l
Answer: 2059

13. How many transcripts are there on chr3?
$ cut -f2,3 apple.genes | sort -u | grep 'chr3' | wc -l
Answer: 1772

14. How many genes are in common between condition A and condition B?
$ cut -f1 apple.conditionA | sort -u > a.genes
$ cut -f1 apple.conditionB | sort -u > b.genes
$ cut -f1 apple.conditionC | sort -u > c.genes
$ comm -1 -2 a.genes b.genes | sort -u | wc -l
Answer: 2410

15. How many genes are specific to condition A?
 $ comm -2 -3 a.genes b.genes | sort -u | wc -l
Answer: 1205

16. How many genes are specific to condition B?
$ comm -1 -3 a.genes b.genes | sort -u | wc -l
Answer: 1243

17. How many genes are in common to all three conditions?
$ comm -1 -2 a.genes b.genes > ab.genes
$ comm -1 -2 ab.genes c.genes | wc -l
Answer: 1608

