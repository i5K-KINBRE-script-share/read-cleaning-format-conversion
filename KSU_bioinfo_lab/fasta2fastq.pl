#!/usr/bin/env perl

##### Script converts FASTA and QUAL files to FASTQ format. It is a slight modification of a script posted to SeqAnwsers http://seqanswers.com/forums/showthread.php?t=2775 
##### Usage: fasta2fastq -b [base filename e.g. filename minus .fasta] -d [directory]

use strict;
use warnings;
use Getopt::Long; # allows me to call arguments by name instead of order

### import my arguments ###
GetOptions(
'b|base:s' => \$base,
'd|directory:s' => \$dir) or die "Usage: fasta2fastq -b [base filename e.g. filename minus .fasta] -d [directory]!\n";

my $offset = 33; # I think this was 33 for sanger FASTQ, change this if required!
my $count = 0;
my %seqs;
my $qual =${dir}.${base}.".qual";
my $fasta =${dir}.${base}.".fasta";
my $fastq =${dir}.${base}.".fastq";

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
	}
	$count++;
}
close FASTA;
$count = 0;
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
