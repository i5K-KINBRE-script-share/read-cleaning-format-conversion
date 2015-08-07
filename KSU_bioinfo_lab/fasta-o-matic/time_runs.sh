#!/usr/bin/bash
start_time=`date +%s`

python ~/read-cleaning-format-conversion/KSU_bioinfo_lab/fasta-o-matic/fasta_o_matic.py -f ~/test_fasta_o_matic/input/GCF_000164845.1_Vicugna_pacos-2.0.1_genomic_FAKE.fna -o ~/test_fasta_o_matic/out -c -s wrap

end_time=`date +%s`
echo execution time was `expr $end_time - $start_time` s.

python ~/read-cleaning-format-conversion/KSU_bioinfo_lab/fasta-o-matic/fasta_o_matic.py -f ~/test_fasta_o_matic/input/GCF_000164845.1_Vicugna_pacos-2.0.1_genomic_FAKE.fna -o ~/test_fasta_o_matic/out1 -c