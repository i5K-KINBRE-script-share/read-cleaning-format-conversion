#Warning: Script currently under development!!

```
USAGE: clean_illumina.py [-h] [-v] [-q] [-c] -r READ_LIST [-p PROJECT]
[-a ADAPTER] [-s] [-x] [-m MIN_READ_LENGTH] [-o OUT]
[-d SEQUENCE]
```

DESCRIPTION: Summarize counts of all four DNA bases. Command-line options that
may be omitted (i.e. are NOT required) are shown in square brackets.

```
optional arguments:
-h, --help            show this help message and exit
-v, --verbose         Runs reporting status updates
-q, --quiet           Does not report status updates
-c, --colorized       Colorizes log reports (use if printing to screen)

-r READ_LIST, --read_list  READ_LIST

This is the the full path (path and filename) of the
user provided list of read files. The file should be
tab separated with the first read file, then the
second read file (see example_read_list_PE.tab). If a
sample has multiple fastq files for R1 and R2 separate
these with commas (see
example_read_list_PE_multi.tab). For single end reads
each line should be a path to a fastq file. For single
end reads each line should be a path to a fastq file
(see example_read_list_SE.tab )

-p PROJECT, --project PROJECT

The project id. This will be used to name output
(default=project).

-a ADAPTER, --adapter ADAPTER

The adapter fasta file. This will be used to clean
reads

-s, --single_end      

If your reads are single end use this flag. Without it
the script assumes reads are paired end. Also skip the
second column (the reverse fastq files) when making
your read list

-x, --convert_header  

If the illumina headers do not end in /1 or /2 use
this parameter to indicat that headers need to be
converted. Check your headers by typing "head
FASTA_FULL_PATH" and read more about illumina headers
at http://en.wikipedia.org/wiki/Fastq#Illumina_sequenc
e_identifiers.

-m MIN_READ_LENGTH, --min_read_length MIN_READ_LENGTH

The minimum read length in bp. (Default = 90).

-o OUT, --out OUT     

Output directory (Default=$HOME)
