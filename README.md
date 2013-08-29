fastq-tools
===========

KSU_bioinfo_lab
---------------
sanger2fasta_qual.pl - Uses the '.anc' file to split reads into forward and reverse files and makes the header pairs identical except for a trailing /1 or /2

fasta2fastq.pl- Script converts FASTA and QUAL files to FASTQ format. It is a slight modification of a script posted to SeqAnwsers http://seqanswers.com/forums/showthread.php?t=2775 

pre_post_cleaning_metrics.pl - This script summarizes average read lengths etc before and after cleaning for multiple single end or paired end files. Output log files from prinseq (v prinseq-lite-0.20.3) are taken as the input and cleaning metrics are written to the file pre_post_clean_reads.csv.

run_broken_pair_removal.sh - Runs the broken pair removal script from the velvet package on multiple files. This script can convert illumina headers so that they end in "/1" or "/2" if your reads are not illumina cassava (post v1.8) you should comment out lines 28 and 29. This script uses a script called stats.sh to monitor and report resource usage on a SGE cluster like Beocat at KSU. But this section (lines 36-42) also can be commented out.
  
run_prinseq.sh - paired end read cleaning with prinseq. This script can convert illumina headers so that they end in "/1" or "/2" if your reads are not illumina cassava (post v1.8) you should comment out lines 28 and 29. This script uses a script called stats.sh to monitor and report resource usage on a SGE cluster like Beocat at KSU. But this section (lines 36-42) also can be commented out.

sort_fastq_by_length.pl - Script finds insert length in custom headers and exports files sorted by insert length

stats.sh - see prinseq.sh
