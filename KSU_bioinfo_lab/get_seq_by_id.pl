#!/usr/bin/perl
##################################################################################
#   
#	USAGE: perl get_seq_by_id.pl [header or headers separated by spaces]
#
#  Created by jennifer shelton
#	Script creates new fasta files including all sequences corresponding to the headers given as input
#  perl get_seq_by_id.pl tcas_3770
##################################################################################
use strict;
use warnings;
use Bio::Seq;
use Bio::SeqIO;
use Bio::DB::Fasta; #makes a searchable db from my fasta file
# use List::Util qw(max);
# use List::Util qw(sum);
###############################################################################
##############                      notes                    ##################
###############################################################################

my $infile_fasta = "sample.fasta"; # give the name of your file
my $out = "seq_got_by_id.fasta";

my $db = Bio::DB::Fasta->new("$infile_fasta");
my $seq_out = Bio::SeqIO->new('-file' => ">$out",'-format' => 'fasta');		#Create new fasta outfile object.

for my $header (@ARGV)
{
	my $seq_obj = $db->get_Seq_by_id($header); #get fasta file
	$seq_out->write_seq($seq_obj);
}
