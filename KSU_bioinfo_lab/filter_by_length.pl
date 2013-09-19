#!/usr/bin/perl
use strict;
use warnings;
use IO::File;
use File::Basename; # enable maipulating of the full path
############################################################################
#
# USAGE: filter_by_length.pl [FASTA filename or filenames]
# Script output fasta records less then the set minimum length. Change minimum length in line 13.
#
############################################################################
my $count=0;
my $min_length=200;
my $outfilename;
################# open files ##############
for my $f (@ARGV)
{
	my $fasta = IO::File->new($f);
	################# screen for length ##############
	$/ = ">";
	open OLD_FASTA,'<', $f or die "Couldn't open $f :$!"; 	# you need to request a warning because we are opening with "open" not BioPerl
	my (${filename}, ${directories}, ${suffix}) = fileparse($f,'\..*');
	$outfilename="${directories}${filename}_gt_${min_length}\.fasta";
	open my $long_fasta, '>', $outfilename  or die "Couldn't open $outfilename :$!";
	while(<OLD_FASTA>)
	{
    	unless ($count == 0)
        {
            chomp;
            my ($header, @seqLines) = split /\n/;
    		my $seqString = join '', @seqLines;
            #     		print "$seqString\n";
    		if ((length($seqString)) > "$min_length")
    		{
    			print $long_fasta '>';
    			print $long_fasta "$_";
    		}
    	}
    	$count++;
    }
    close (OLD_FASTA);
}
