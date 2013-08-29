#!/usr/bin/perl
#use strict;
use warnings;
# USAGE: sort_fastq_by_length.pl -f [contig_FASTQ_filename]
# LONG USAGE: agp2scaffold.pl --fasta [contig_FASTA_filename]
### load my modules ###
use Getopt::Long; # allows me to call arguments by name instead of order
use File::Basename;

### initialize variables for files ###
my $filehandle='';
my %lengths;
my ($path,$fastq);

### import my arguments ###
GetOptions
(
'f|fastq:s' => \$fastq,
);

my($filename, $directories, $suffix) = fileparse($fastq);

### open fastq ###
open(FASTQ,$fastq) or die $!; 	#request a warning

while (<FASTQ>)
{
	#@template_id=TBWDP0452 insert_size=3000 insert_sd=1000/1
	if (/^@\S+ insert_size=(\S+) insert_sd=\S+\/[12]\n/)# if the line is a header
	{
		unless ($lengths{$1})# start the first file
		{
			$lengths{$1}=1;
			$path=$directories.$filename."_".$1.$suffix;
			$filehandle="FASTQ".$1;
			open($filehandle, ">$path");
		}
		elsif ($lengths{$1}=1)
		{
			$filehandle="FASTQ".$1;
		}
	}
	print {$filehandle} $_;
}