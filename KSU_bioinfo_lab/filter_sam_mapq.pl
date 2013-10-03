#!/usr/bin/perl
use strict;
use warnings;
use IO::File;
use File::Basename; # enable maipulating of the full path
#  filter_sam_mapq.pl
#  USAGE: perl filter_sam_mapq.pl [filename/s]
# This script takes sam files from Bowtie2 paired end alignments and outputs filtered sam files (only reporting alignments above the minimum MAPQ filter)
# Filters are based on MAPQ and pair relationships (e.g. if mates were aligned separately only one mate can pass the filter in order that mate to be printed) for Bowtie2 sam files 
# Change the default MAPping Quality (MAPQ) in line 23.
#
#
#  Created by jennifer shelton on 10/1/13.
##################  define variables #################################################
my (@temp);
my (%pass_hash);
my ($contig,$k);
my $i=0;
my $outfile;
################################ Set filters ###############################
my $mapq=10;

################################ make a pass_hash of raw counts ################################
print "Summary of fragments counted by this script:\n"; # header for output summary
foreach my $f (@ARGV)
{
	my $concordant_pair_mapped_read=0;
	my $discordant_pair_mapped_read=0;
	my $unpaired_mate_mapped_reads=0; # only one end maps relatively unambiguously (above MAPQ cutoff) 
	my $fragment=0; # counts one for each pair or singleton (UU in Bowtie2 syntax) regardless of whether or not they map
	my %read_hash;
	my $file = IO::File->new();
    	if ($file->open("< $f")) {print "$f opened for first pass\n";}
    	else {print "could not open $f for second pass\n";}
	while (<$file>)
	{
		unless (/^\@/)
 	   {
	        @temp=split(/\t/);
	        unless ($pass_hash{$temp[0]}) ## if we haven't seen the read before add it to pass_hash and initialize as 0 (i.e. we have no evidence this fragment passes our ambiguity filter)
	        {
	        	$pass_hash{$temp[0]}=0;
	        }
################################ require pairs map to same contig ################################
	        if ($temp[6] eq '=')
	        {
################################ filter concordant pairs ################################
	        	if ($_ =~ /YT:Z:CP/)
	        	{
	        		unless ($read_hash{$temp[0]})
	        		{
	        			$fragment++;
	        			if (($temp[4]>$mapq)&&($temp[4]!=255))
	        			{
	        				$read_hash{$temp[0]}=1;
	        			}
	        			else
	        			{
	        				$read_hash{$temp[0]}=0;
	        			}
	        		}
	        		else
	        		{ 
	        			if ((($temp[4]>$mapq)&&($temp[4]!=255)) || ($read_hash{$temp[0]}==1))
	        			{
	        				$pass_hash{$temp[0]}=1; ## pair passes when one or both ends map relatively unambiguously (above MAPQ cutoff)
	        				$concordant_pair_mapped_read++;
	        			}
	        		}
	        	}	        				        		
################################ filter discordant pairs ################################	        		
	        	if ($_ =~ /YT:Z:DP/)
	        	{
	        		unless ($read_hash{$temp[0]})
	        		{
	        			$fragment++;
	        			if (($temp[4]>$mapq)&&($temp[4]!=255))
	        			{
	        				$read_hash{$temp[0]}=1;
	        			}
	        			else
	        			{
	        				$read_hash{$temp[0]}=0;
	        			}
	        		}
	        		else
	        		{ 
	        			if ((($temp[4]>$mapq)&&($temp[4]!=255)) || ($read_hash{$temp[0]}==1))
	        			{
	        				$pass_hash{$temp[0]}=1; ## count one for a paired read where one or both ends map relatively unambiguously (above MAPQ cutoff)
	        				$discordant_pair_mapped_read++;
	        			}
	        		}
	        	}
	        }
	        elsif (($read_hash{$temp[0]}) && ($temp[6] ne '=') && (($_ =~ /YT:Z:CP/) || ($_ =~ /YT:Z:DP/)))
	        {
	        	$fragment++;
	        	$read_hash{$temp[0]}=0;
	        }
################# if one pair fails and one passes use the broken pairs (UP) ################################	        		
	        if ($_ =~ /YT:Z:UP/)
	        	{
	        		unless ($read_hash{$temp[0]})
	        		{
	        			$fragment++;
	        			if (($temp[4]>$mapq)&&($temp[4]!=255))
	        			{
	        				$read_hash{$temp[0]}=1;
	        			}
	        			else
	        			{
	        				$read_hash{$temp[0]}=0;
	        			}
	        		}
	        		else
	        		{ 
	        			if ((($temp[4]>$mapq)&&($temp[4]!=255)) && ($read_hash{$temp[0]}==0))
	        			{
	        				$pass_hash{$temp[0]}=$_; ## pass where only one end maps relatively unambiguously (above MAPQ cutoff)
	        				$unpaired_mate_mapped_reads++;
	        			}
	        			elsif ((($temp[4]<=$mapq)||($temp[4]==255)) && ($read_hash{$temp[0]}==1))
	        			{
	        				$pass_hash{$temp[0]}=$_; ## pass where only one end maps relatively unambiguously (above MAPQ cutoff)
	        				$unpaired_mate_mapped_reads++;
	        			}	        			
	        		}
	        	}	

		}
	    
    	}
    	print "$f concordant_pairs that were added to unambigous sam file= $concordant_pair_mapped_read\n";
	print "$f discordant_pairs that were added to unambigous sam file= $discordant_pair_mapped_read\n";
	print "$f unpaired_mates that were added to unambigous sam file= $unpaired_mate_mapped_reads\n";
	print "$f fragments were found in total= $fragment\n";
    	$i++;
	$file->close;
}
	
foreach my $f (@ARGV)
{
################################ create output files #########################################
	my (${filename}, ${directories}, ${suffix}) = fileparse($f,'\..*');
	my $outfilename="${directories}${filename}_unambig\.sam";
	open my $outfile, '>', $outfilename  or die "Couldn't open $outfilename :$!";
################################ open one sam file at a time #########################################
	my $file = IO::File->new();
    if ($file->open("< $f")) {print "$f opened for second pass\n";}
    else {print "could not open $f for second pass\n";}
	while (<$file>)
	{
		if  (/^\@/)
		{
			print $outfile "$_"; ## if this line is a header line print current line of sam file 
		}
		else
		{
			@temp=split(/\t/);
			unless($pass_hash{$temp[0]} eq '0')
			{ 
	    		if ($pass_hash{$temp[0]} eq '1') 
	    		{
	    	    	print $outfile "$_"; ## if this pair passed the MAPQ filters print current line of sam file
	    		}
	    		else 
	    		{
	    			print $outfile "$pass_hash{$temp[0]}"; ## if only one member of a pair passed the MAPQ filters print the member that passed and set the pass_hash value to 0 (e.g. skip printing this alignment twice)
	    			$pass_hash{$temp[0]}=0;
	    		}
	    	}
		}
	}
	$file->close;
}
	
