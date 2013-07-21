#!/usr/bin/perl
#
# Bradley JSC Olson
# Kansas State University
#
# Script determines if fastq sequences are paired line-by-line in two separate files
# Usage: ./check4properpairing.pl file1.fastq file2.fastq
#

use strict;
use warnings;
use Bio::SeqIO;
use 5.010;

my $io1=Bio::SeqIO->new(-file=>"<$ARGV[0]", -format=>'fastq');
my $io2=Bio::SeqIO->new(-file=>"<$ARGV[1]", -format=>'fastq');

my @seq_ids1;
while (my $seq1=$io1->next_seq)
{
	push(@seq_ids1, $seq1->id);
}

my @seq_ids2;
while (my $seq2=$io2->next_seq)
{
	push(@seq_ids2, $seq2->id);
}

my $i=0;
my $j=0; #Counts the number of mis-paired reads
foreach (@seq_ids1)
{
	if ($seq_ids1[$i] ne $seq_ids2[$i])
	{
		print "These two Sequences are mis-matched! $seq_ids1[$i], $seq_ids2[$i]\n";
		$j++;
	}
	$i++;
}

if ($j == 0) #If no mis-matched reads are paired, print that all is ok
{
	print "All reads are properly paired\n";
}
	