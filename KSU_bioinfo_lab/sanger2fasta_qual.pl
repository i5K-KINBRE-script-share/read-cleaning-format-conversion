#!/usr/bin/perl
#### Usage: sanger2fasta_qual.pl -b [base filename e.g. filename minus qual, anc, or fasta] -d [directory]
use strict;
use warnings;
use Getopt::Long; # allows me to call arguments by name instead of order

### declare variables for files, temporary seq_ids, and sequences and set default value for output ###
my (%header_hash,@row);
my ($file_out,$insert_size,$insert_sd,$template_id,$ti,$trace_end,$trace_name);
my $dir="/homes/bioinfo/Tcas/sanger_reads/"; # default directory
my $base="tribolium_castaneum.003"; # default base filename
## /homes/bioinfo/Tcas/sanger_reads/qual.tribolium_castaneum.004

### import my arguments ###
GetOptions(
'b|base:s' => \$base,
'd|directory:s' => \$dir)or die "Usage: sanger2fasta_qual.pl -b [base filename e.g. filename minus qual, anc, or fasta] -d [directory]!\n";

### open files ###
open(IN_ANC,"<${dir}anc.${base}") or die $!; 	# you need to request a warning because we are opening with "open" not BioPerl
open(IN_FASTA,"<${dir}fasta.${base}") or die $!; 	# you need to request a warning because we are opening with "open" not BioPerl
open(IN_QUAL,"<${dir}qual.${base}") or die $!; 	# you need to request a warning because we are opening with "open" not BioPerl
open(FASTA_R1,">${dir}${base}_R1.fasta");
open(FASTA_R2,">${dir}${base}_R2.fasta");
open(QUAL_R1,">${dir}${base}_R1.qual") ;
open(QUAL_R2,">${dir}${base}_R2.qual") ;

while (<IN_ANC>)
{
    @row= split("\t");
    ($insert_size,$insert_sd,$template_id,$ti,$trace_end,$trace_name)=($row[29],$row[30],$row[53],$row[54],$row[56],$row[58]);
#    ($insert_size,$insert_sd,$template_id,$ti,$trace_end,$trace_name)=($row[26],$row[27],$row[56],$row[57],$row[59],$row[61]);
	$header_hash{$ti}=">template_id=$template_id insert_size=$insert_size insert_sd=$insert_sd $trace_end\n";
}
while (<IN_FASTA>)
{
	if (/^>/)
	{
        /\|ti\|(\S+)/;
        my $header="$header_hash{$1}";
        if ($header =~ /(.*) F(\n)/)
		{
            print FASTA_R1 "$1/1$2";
			$file_out = "R1";
		}
		elsif ($header =~ /(.*) R(\n)/)
		{
            print FASTA_R2 "$1/2$2";
			$file_out = "R2";
		}
	}
	elsif ($file_out eq "R1")
	{
		print FASTA_R1;
	}
	elsif ($file_out eq "R2")
	{
		print FASTA_R2;
	}
}
while (<IN_QUAL>)
{
	if (/^>/)
	{
        /\|ti\|(\S+)/;
        my $header="$header_hash{$1}";
        if ($header =~ /(.*) F(\n)/)
		{
            print QUAL_R1 "$1/1$2";
			$file_out = "R1";
		}
		elsif ($header =~ /(.*) R(\n)/)
		{
            print QUAL_R2 "$1/2$2";
			$file_out = "R2";
		}
	}
	elsif ($file_out eq "R1")
	{
		print QUAL_R1;
	}
	elsif ($file_out eq "R2")
	{
		print QUAL_R2;
	}
}
