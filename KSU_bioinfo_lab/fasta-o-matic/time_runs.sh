#!/usr/bin/bash
echo "Hello"
echo "Wrap only Fasta-O-Matic execution:"
#526585/memusg python ~/read-cleaning-format-conversion/KSU_bioinfo_lab/fasta-o-matic/fasta_o_matic.py -f ~/test_fasta_o_matic/input/GCF_000164845.1_Vicugna_pacos-2.0.1_genomic_FAKE.fna -o ~/test_fasta_o_matic/out -c -s wrap -q

/usr/bin/time -v python ~/read-cleaning-format-conversion/KSU_bioinfo_lab/fasta-o-matic/fasta_o_matic.py -f ~/test_fasta_o_matic/input/GCF_000164845.1_Vicugna_pacos-2.0.1_genomic_FAKE.fna -o ~/test_fasta_o_matic/out -c -s wrap -q

echo "All steps Fasta-O-Matic execution:"
#526585/memusg python ~/read-cleaning-format-conversion/KSU_bioinfo_lab/fasta-o-matic/fasta_o_matic.py -f ~/test_fasta_o_matic/input/GCF_000164845.1_Vicugna_pacos-2.0.1_genomic_FAKE.fna -o ~/test_fasta_o_matic/out1 -c -q
/usr/bin/time -v python ~/read-cleaning-format-conversion/KSU_bioinfo_lab/fasta-o-matic/fasta_o_matic.py -f ~/test_fasta_o_matic/input/GCF_000164845.1_Vicugna_pacos-2.0.1_genomic_FAKE.fna -o ~/test_fasta_o_matic/out1 -c -q
echo "Wrap only setk execution:"
#526585/memusg /home/bionano/seqtk/seqtk seq -l 60 /home/bionano/test_fasta_o_matic/input/GCF_000164845.1_Vicugna_pacos-2.0.1_genomic_FAKE.fna > /home/bionano/test_fasta_o_matic/out2/GCF_000164845.1_Vicugna_pacos-2.0.1_genomic_FAKE_seqtk_wrap.fna
/usr/bin/time -v /home/bionano/seqtk/seqtk seq -l 60 /home/bionano/test_fasta_o_matic/input/GCF_000164845.1_Vicugna_pacos-2.0.1_genomic_FAKE.fna > /home/bionano/test_fasta_o_matic/out2/GCF_000164845.1_Vicugna_pacos-2.0.1_genomic_FAKE_seqtk_wrap.fna
echo "Wrap only seqret execution:"
#526585/memusg /home/bionano/EMBOSS-6.5.7/emboss/seqret -sequence ~/test_fasta_o_matic/input/GCF_000164845.1_Vicugna_pacos-2.0.1_genomic_FAKE.fna -outseq /home/bionano/test_fasta_o_matic/out3/GCF_000164845.1_Vicugna_pacos-2.0.1_genomic_FAKE_seqret.fna
/usr/bin/time -v /home/bionano/EMBOSS-6.5.7/emboss/seqret -sequence ~/test_fasta_o_matic/input/GCF_000164845.1_Vicugna_pacos-2.0.1_genomic_FAKE.fna -outseq /home/bionano/test_fasta_o_matic/out3/GCF_000164845.1_Vicugna_pacos-2.0.1_genomic_FAKE_seqret.fna
 
