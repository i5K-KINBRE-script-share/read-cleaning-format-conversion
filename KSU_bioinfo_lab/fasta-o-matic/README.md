##Fasta-O-Matic: a tool to sanity check and if needed reformat FASTA files

<a href="url"><img src="https://raw.githubusercontent.com/i5K-KINBRE-script-share/read-cleaning-format-conversion/master/KSU_bioinfo_lab/fasta-o-matic/sequence_data_tools.png" align="left" width="348" ></a>

Fasta-O-Matic is a quality control script that makes FASTA format files compatible for a variety of downstream bioinformatics tools. 

All of the scripts you will need to run the commands below as well as the sample datasets will be copied to your computer as you follow the instructions below. You should type or paste the text in the beige code block into your terminal as you follow along with the instructions below.

If you would like a quick primer on basic linux commands and running programs from the commandline try these concise lessons from Software Carpentry http://swcarpentry.github.io/shell-novice/. 

We will be using a sample FASTA file of DNA sequences assembled from Escherichia coli genomic DNA.  Specifically, the genome was fragmented for a demonstration dataset from gi|170079663|ref|NC_010473.1| Escherichia coli str. K-12 substr. DH10B chromosome, complete genome.

Fasta-O-Matic runs quality checking of the FASTA file format. File format errors are categorized as fatal or non-fatal by Fasta-O-Matic. The tool will repair improperly formatted files, return the file name of the reformatted file and report the issue to the user based on a user-defined list of quality checks if the issues are non-fatal. If a fatal formatting issue is found Fasta-O-Matic will exit and report the error without creating a reformatted file. If no error is found no new file is created.

Fasta-O-Matic is designed to prepare adapter FASTA files for Trimmomatic but can be used as a general pre-processing tool in bioinformatics workflows (e.g. to automatically wrap FASTA files so that they can be read by BioPerl).

As you work through this example your should read about the software by generating and reading the help menu. Find out about FASTA format at http://blast.ncbi.nlm.nih.gov/blastcgihelp.shtml. 

###Step 1: Clone the Git repositories 

Install the KSU custom software using the code below:

```
cd

git clone https://github.com/i5K-KINBRE-script-share/read-cleaning-format-conversion.git
```

Fasta-O-Matic runs with either Python2.7+ or Python3.3+. Find out about all the options for Fasta-O-Matic by reading the help menu:

```
python ~/read-cleaning-format-conversion/KSU_bioinfo_lab/fasta-o-matic/fasta_o_matic.py --help
```

###Step 2: Create project directory

Make a project output directory.

```
mkdir ~/out_fasta_o_matic
```

###Step 3: Examine the input FASTA file.

Using the code below to view the sample FASTA file:

```
less ~/read-cleaning-format-conversion/KSU_bioinfo_lab/sample_data/NC_010473_mock_scaffolds.fna
```

Observe that the first FASTA record (sequence in the file) is improperly wrapped. Some lines are a set length while others vary in length. Additionally some lines of sequence are longer than recommended by NCBI. NCBI recommends that sequence length for all lines of text be shorter than 80 characters (http://blast.ncbi.nlm.nih.gov/blastcgihelp.shtml). While this is only a recommended aspect of the FASTA file format, some bioinformatic tools (e.g. BioPerl) will not load unwrapped or improperly wrapped FASTA files.

Additionally, The FASTA headers have spaces within the header. This is accepted FASTA format but presents problems for some analysis tools.

Type `q` to exit the `less` viewer.

Run the command below to view the final line of the FASTA file:

```
tail ~/read-cleaning-format-conversion/KSU_bioinfo_lab/sample_data/NC_010473_mock_scaffolds.fna
```

This FASTA file is also missing the last newline. When a FASTA file is missing the last new line often it means that the file content is correct but the researcher overlooked finishing the file with a newline (e.g. the adapter sequence FASTA files for Trimmomatic). It could also be a sign that the FASTA file has been corrupted (e.g. a file transfer failed before completing the transfer).

The lack of the final newline can cause serious problems in downstream analysis. For example FASTA files are commonly joined by concatenating one file to another. A missing final new line would cause the last sequence from one file to be merged with the first header from the next file. This new chimeric sequence and the now header-less sequence that would follow could not be properly loaded by downstream tools as all tools depend on headers to identify and separate sequences.


###Step 4: Automatically check for formatting issues and reformat as needed.

By default Fasta-O-Matic checks/reformats wrapping, newlines and headers with spaces. Run the following to reformat all three issues at once.

```
python ~/read-cleaning-format-conversion/KSU_bioinfo_lab/fasta-o-matic/fasta_o_matic.py -f ~/read-cleaning-format-conversion/KSU_bioinfo_lab/sample_data/NC_010473_mock_scaffolds.fna -o ~/out_fasta_o_matic -c
```

Check your results:

```
less ~/out_fasta_o_matic/NC_010473_mock_scaffolds_wrap_h.fasta
```

###Step 5: Selectively reformat (skipping header conversion)


You may also wish to only check/reformat a FASTA file for specific problems (e.g. you are not concerned with spaces in the FASTA headers). You can pass a space separated list of QC steps with the `-s` or `--qc_steps` flag. The options are one or more of the following three steps: `wrap` `new_line` `header_whitespace`.

Try for example:

```
python ~/read-cleaning-format-conversion/KSU_bioinfo_lab/fasta-o-matic/fasta_o_matic.py -f ~/read-cleaning-format-conversion/KSU_bioinfo_lab/sample_data/NC_010473_mock_scaffolds.fna -o ~/out_fasta_o_matic -s wrap new_line -c
```

Check your results with:

```
less ~/out_fasta_o_matic/NC_010473_mock_scaffolds_wrap.fasta
```
