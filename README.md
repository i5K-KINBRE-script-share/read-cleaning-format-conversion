Read cleaning and format conversion
===================================

KSU_bioinfo_lab
---------------

##Fasta-O-Matic: a tool to sanity check and if needed reformat FASTA files

<a href="url"><img src="https://raw.githubusercontent.com/i5K-KINBRE-script-share/read-cleaning-format-conversion/master/KSU_bioinfo_lab/fasta-o-matic/sequence_data_tools.png" align="left" width="348" ></a>

Fasta-O-Matic is a quality control script that makes FASTA format files compatible for a variety of downstream bioinformatics tools. 
As the shear volume of bioinformatic sequence data increases the only way to take advantage of this content is to more completely automate robust analysis workflows. Analysis bottlenecks are often mundane and overlooked processing steps. Idiosyncrasies in reading and/or writing bioinformatics file formats can halt or impair analysis workflows by interfering with the transfer of data from one informatics tools to another. Fasta-O-Matic automates handling of common but minor format issues that otherwise may halt pipelines. The need for automation must be balanced by the need for manual confirmation that any formatting error is actually minor rather than indicative of a corrupt data file. To that end Fasta-O-Matic reports any issues detected to the user with optionally color coded and quiet or verbose logs.

Fasta-O-Matic can be used as a general pre-processing tool in bioinformatics workflows (e.g. to automatically wrap FASTA files so that they can be read by BioPerl). It was also developed as a sanity check for bioinformatic core facilities that tend to repeat common analysis steps on FASTA files received from disparate sources. Fasta-O-Matic can be set with format requirements specific to downstream tools as a first step in a larger analysis workflow.

DEPENDENCIES: 

Fasta-O-Matic runs with either Python2.7+ or Python3.3+.

USAGE:

'''
'''
Cite as: Jennifer Shelton et al.. (2015). read-cleaning-format-conversion: read-cleaning-format-conversion tools Version 1.0.0. Zenodo. 10.5281/zenodo.17585

[![DOI](https://zenodo.org/badge/12929/i5K-KINBRE-script-share/read-cleaning-format-conversion.svg)](http://dx.doi.org/10.5281/zenodo.17585)

**WrapFasta.pl** - Wrapping sequence is recommended by NCBI for fasta format. Some programs will return errors if this is not done properly. Here are a couple examples of this type of error: "Each line of the fasta entry must be the same length except the last." or "Each line of the qual file must be less than 65,536 characters."
 
If you are receiving a similar error from a program you are trying to run then WrapFasta.pl will create a reformatted fasta file from your improperly wrapped file.

DEPENDENCIES: 

WrapFasta.pl requires the following BioPerl libraries: Bio::SeqIO and Bio::Seq.

    USAGE: WrapFasta.pl -f [FASTA filename]

**fasta2fastq.pl** - Script converts FASTA and QUAL files to FASTQ format. It is a slight modification of a script posted to SeqAnwsers http://seqanswers.com/forums/showthread.php?t=2775 

    USAGE: fasta2fastq -b [base filename e.g. filename minus .fasta] -d [directory]

**filter_by_length.pl** -Script output fasta records less then the set minimum length.

    USAGE: filter_by_length.pl [FASTA filename or filenames]

**pre_post_cleaning_metrics.pl** - This script summarizes average read lengths etc before and after cleaning for multiple single end or paired end files. Output log files from prinseq (v prinseq-lite-0.20.3) are taken as the input and cleaning metrics are written to the file pre_post_clean_reads.csv.

    USAGE: perl pre_post_cleaning_metrics.pl [.log filename/s]

**run_broken_pair_removal.sh** - Runs the broken pair removal script from the velvet package on multiple files. This script can convert illumina headers so that they end in "/1" or "/2" if your reads are not illumina cassava (post v1.8) you should comment out lines 28 and 29. This script uses a script called stats.sh to monitor and report resource usage on a SGE cluster like Beocat at KSU. But this section (lines 36-42) also can be commented out.

    USAGE: run_broken_pair_removal.sh [filenames_minus_1.fastq or _2.fastq]
  
**run_prinseq.sh** - paired end read cleaning with prinseq. This script can convert illumina headers so that they end in "/1" or "/2" if your reads are not illumina cassava (post v1.8) you should comment out lines 28 and 29. This script uses a script called stats.sh to monitor and report resource usage on a SGE cluster like Beocat at KSU. But this section (lines 36-42) also can be commented out.

    USAGE: bash run_prinseq.sh [filenames_minus_R1_001_h.fastq or _R2_001_h.fastq]

**sanger2fastq.pl** - Script converts older paired sanger reads (with an ANC, FASTA, and QUAL file) to FASTQ format. The headers and files will be similar to Illumina mate pair output (i.e. RF orientation). You will need to customize line 14 to 64 to import your data because the sanger ANC files seem to have a variable order to the columns. The conversion from FASTA to FASTQ is a modification of a script posted to SeqAnwsers http://seqanswers.com/forums/showthread.php?t=2775 
Uses the '.anc' file to split reads into forward and reverse files and makes the header pairs identical except for a trailing /1 or /2

    USAGE: sanger2fasta_qual.pl 

**sanger2fastq_brokenpair_rm.pl** - Script output unbroken pairs and singletons, sequences with more than two template_ids in the anc file are removed

    USAGE: sanger2fastq_brokenpair_rm.pl 

**make_contigs_from_fasta.pl** Script breaks scaffolds at Ns and outputs a new multi fasta file with one entry pre contig 

```USAGE: perl make_contigs_from_fasta.pl [fasta]```
  
**stats.sh** - see prinseq.sh
