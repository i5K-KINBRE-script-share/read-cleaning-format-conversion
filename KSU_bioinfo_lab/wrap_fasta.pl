#!/usr/bin/perl
##################################################################################
#   
#	USAGE: perl wrap_fasta.pl
#
#  Created by jennifer shelton
#  DESCRIPTION: Wraps fasta files to the NCBI recommended 80 bp per line https://www.ncbi.nlm.nih.gov/BLAST/blastcgihelp.shtml. Does not require BioPerl. scripts that wraps lines of fasta file without wrapped sequences or with inconsistently wrapped sequences. NCBI recommends that FASTA sequences be wrapped and BioPerl requires this however not all tools create wrapped FASTA files. Your reformatted fasta file will start with the original filename and end with "_wrapped.fasta".
##################################################################################
use strict;
use warnings;
# use List::Util qw(max);
# use List::Util qw(sum);
use File::Basename; # enable maipulating of the full path
##################################################################################
##############                      notes                       ##################
##################################################################################

my $fasta = $ARGV[0];
open (FASTA, "<", $fasta) or die  "can't open $fasta ! \n";
my (${filename}, ${directories}, ${suffix}) = fileparse($fasta,'\..*');
my $out_fasta = "${directories}${filename}_wrapped.fasta";
open (OUTFASTA,">","$out_fasta") or die "can't open $out_fasta\n";
while (<FASTA>)
{
    if (/^>/)
    {
        print OUTFASTA;
    }
    else
    {
        chomp;
        my $seq=$_;
        print OUTFASTA substr($seq,0,80,'') . "\n" while ($seq);
    }
}
