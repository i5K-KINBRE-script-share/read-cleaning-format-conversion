#!/usr/bin/perl
###############################################################################
#
#	USAGE: perl SeqByInterval.pl [first sequence number] [second sequence number] [fasta]
#
#	Description: Takes two numbers "x" and "y" as input and creates a new file with only sequence number "x" and sequence number "y" from the original fasta file. For example "perl SeqByInterval.pl 1 3 test.fasta" would create a new fasta with only the first three fasta entries.
#  Created by jennifer shelton
#
###############################################################################
use strict;
use warnings;
use File::Basename; # enable manipulating of the full path
# use List::Util qw(max);
# use List::Util qw(sum);
use Bio::SeqIO;
use Bio::Seq;
use Bio::DB::Fasta;
###############################################################################
##############                Initialize variables           ##################
###############################################################################
# my $dirname = dirname(__FILE__);
my $start = $ARGV[0];
my $stop = $ARGV[1];
my $fasta_in = $ARGV[2];

my (${filename}, ${directories}, ${suffix}) = fileparse($fasta,qr/\.[^.]*/); # directories has trailing slash includes dot in suffix
my $fasta_out = "${directories}${filename}_interval.fa";
my $count = 1;
###############################################################################
##############          Open output fasta                    ##################
###############################################################################
my $seq_out = Bio::SeqIO->new(-file => ">$fasta_out", -format => 'fasta');
###############################################################################
##############          Open input fasta                    ##################
###############################################################################
my $seq_in = Bio::SeqIO->new(-file => "<$fasta_in", -format => 'fasta');
###############################################################################
##############                      Run                      ##################
###############################################################################
while (my $seq = $seq_in->next_seq)
{
    if (($count >= $start) && ($count <= $stop))
    {
        $seq_out->write_seq($seq);
    }
    ++$count;
}

print "done\n";

