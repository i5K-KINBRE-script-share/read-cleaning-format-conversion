#!/usr/bin/perl

#  pre_post_cleaning_metrics.pl
#  
#
#  Created by jennifer shelton on 7/25/13.
#
# 
#  USAGE: perl pre_post_cleaning_metrics.pl [.log filename/s]
# This script takes output log files from prinseq (v prinseq-lite-0.20.3) and outputs summary cleaning metrics to either pre_post_clean_reads.csv.
##################  define variables #################################################

use strict;
use warnings;
use IO::File;
my $outfile="pre_post_clean_reads.csv";
open (METRICS, ">$outfile");
my ($input_sequences,$input_bases,$input_mean_length,$good_sequences,$good_bases,$good_mean_length,$bad_sequences,$bad_bases,$bad_mean_length);
foreach my $f (@ARGV)
{
	my $file = IO::File->new($f);
#    my ($i,$temp_input_mean_length);
	while (<$file>)
    {
        chomp;
        s/[,]//g;
        if (/(Good sequences \(pairs\))(: )(.*)/)
        {
            $good_sequences+=$3*2;
        }
        if (/(Good bases \(pairs\))(: )(.*)/)
        {
            $good_bases+=$3;
        }
        elsif (/(Input sequences).*(: )(.*)/)
        {
            $input_sequences+=$3;
        }
        elsif (/(Input bases).*(: )(.*)/)
        {
            $input_bases+=$3;
        }
        elsif (/(Good sequences).*(: )(.*)( \()/)
        {
            $good_sequences+=$3;
        }
        elsif (/(Good bases).*(: )(.*)/)
        {
            $good_bases+=$3;
        }
        elsif (/(Bad sequences).*(: )(.*)( \()/)
        {
            $bad_sequences+=$3;
        }
        elsif (/(Bad bases).*(: )(.*)/)
        {
            $bad_bases+=$3;
        }
    }
    $input_mean_length=($input_bases/$input_sequences);
    $good_mean_length=($good_bases/$good_sequences);
    $bad_mean_length=($bad_bases/$bad_sequences);
}
print METRICS " ,Number of reads,Number of bases,Mean read length\nRaw reads,$input_sequences,$input_bases,$input_mean_length\nGood reads,$good_sequences,$good_bases,$good_mean_length\nBad reads,$bad_sequences,$bad_bases,$bad_mean_length\n";


