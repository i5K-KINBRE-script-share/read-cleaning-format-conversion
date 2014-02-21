#!/bin/perl
##################################################################################
#   
#	USAGE: perl wrap_fasta.pl
#
#  Created by jennifer shelton
# Wraps fasta files to the NCBI recommended 80 bp per line https://www.ncbi.nlm.nih.gov/BLAST/blastcgihelp.shtml
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
my $out_fasta = "${directories}${filename}_wrap.fasta";
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