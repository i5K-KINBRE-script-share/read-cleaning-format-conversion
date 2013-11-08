#!/usr/bin/perl

use strict;
use warnings;

# this script breaks scaffolds at Ns and outputs a new multi fasta file with one entry pre contig 
# USAGE: perl make_contigs_from_fasta.pl [fasta]

open FASTA, '<', $ARGV[0] or die "Couldn't open $ARGV[0]: $!";
open CONTIGFA, '>', "$ARGV[0]"."_contig.fasta" or die "Couldn't create $ARGV[0]_contig.fasta: $!";


my $counter=-1;
my $sum=0;
$/=">";
while (<FASTA>)
{
    ++$counter;
    if ($counter >= 1)
    {
        my ($header,@seq)=split/\n/;
        my $seq=join '', @seq;
        $seq =~ s/>//g;
        my @contigs= split(/N+/,$seq);
        my $contig_counter=1;
        foreach my $broken (@contigs)
        {
            print CONTIGFA ">${header}|Scaffold${counter}|Contig${contig_counter}\n";
            print CONTIGFA "$broken\n";
            ++$contig_counter;
        }

    }
    
}


