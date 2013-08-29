#!/usr/bin/env perl

##### Script converts FAST and QAUL files to FASTQ format. It is a slight modification of a script posted to SeqAnwsers http://seqanswers.com/forums/showthread.php?t=2775 
##### Usage: fasta2fastq [base filename (e.g. filename minus ".fasta"] 

use strict;
use warnings;

my $offset = 33; # I think this was 33 for sanger FASTQ, change this if required!
my $count = 0;
my %seqs;
my $qual =$ARGV[0].".qual";
my $fasta =$ARGV[0].".fasta";
my $fastq =$ARGV[0].".fastq";
die ("Usage: fasta2fastq [base filename (e.g. filename minus .fasta]") unless  (scalar @ARGV) == 1;

open FASTA, $fasta or die "cannot open fasta: $!\n";
open QUAL, $qual or die "cannot open qual: $!\n";
open FASTQ, ">$fastq";

$/ = ">";
while (<FASTA>)
{
	unless ($count == 0)
	{
		chomp;
		my ($fdef, @seqLines) = split /\n/;
		my $seq = join '', @seqLines;
		$seqs{$fdef} = $seq;
#		print "$seqs{$fdef}\n";
	}
	$count++;
}
close FASTA;
$count = 0;
# my $qual0 = overrideDefault(33, 'qual_zero');
my $qual0 =33;
while (<QUAL>)
{
	unless ($count == 0)
	{
		chomp;
		my ($qdef, @qualLines) = split /\n/;
		my $qualString = join ' ', @qualLines;
		$qualString =~ s/\s+/ /g;
		my @quals = split / /, $qualString;
		print FASTQ "@","$qdef\n";
		print FASTQ "$seqs{$qdef}\n";
		print FASTQ "+\n";
		foreach my $qual (@quals)
		{
            unless ($qual eq ''){print FASTQ chr($qual + $qual0)};
		}
		print FASTQ "\n";
	}
	$count++;
}

close QUAL;