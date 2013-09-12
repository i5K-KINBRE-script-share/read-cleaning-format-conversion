#!/usr/bin/perl
# use strict;
use warnings;
use File::Basename; # enable maipulating of the full path
#
#
#
##### Script converts older paired sanger reads (with an ANC, FASTA, and QUAL file) to FASTQ format. The headers and files will be similar to Illumina mate pair output (i.e. RF orientation). You will need to customize line 14 to 64 to import your data because the sanger ANC files seem to have a variable order to the columns. The conversion from FASTA to FASTQ is a modification of a script posted to SeqAnwsers http://seqanswers.com/forums/showthread.php?t=2775 
##### Usage: sanger2fasta_qual.pl 
#
#
#

my (%header_hash,%template_id_hash,%seq_hash,%key_hash,%fastq,@timeData,@row);
my ($key,$value,$index,$file_out,$insert_size,$insert_sd,$template_id,$ti,$trace_end,$trace_name,$filehandle,$path);

################# create %header_hash %template_id_hash ####################

######## list all files I am interested in #########
###my @files=`ls /homes/bioinfo/Tcas/sanger_reads/tribolium_castaneum_R*_bp_*.fastq`;
my @ancfiles=`ls /homes/bioinfo/Tcas/sanger_reads/anc.tribolium_castaneum.00*`; # default directory
foreach(@ancfiles)
{
    chomp;
    unless ($_ eq '/homes/bioinfo/Tcas/sanger_reads/anc.tribolium_castaneum.004')
    {
	    open(IN_ANC,"<$_") or die $!; 	# request a warning
	    while(<IN_ANC>)
	    {
    		unless (/TEMPLATE_ID/)
    		{
        		@row= split("\cI");
        		($insert_size,$insert_sd,$template_id,$ti,$trace_end,$trace_name)=($row[29],$row[30],$row[53],$row[54],$row[56],$row[58]); #file 1-3
        		if ($template_id_hash{$template_id}){$template_id_hash{$template_id}=$template_id_hash{$template_id}+1;}
        		else {$template_id_hash{$template_id}=1;}
        		if (($trace_end eq "F")||($trace_end eq "FORWARD"))
        		{
           	 		$header_hash{$ti}="\@Template_id=${template_id}_Insert_size=${insert_size}_Insert_sd=${insert_sd}#/2\n";
        		}
        		elsif (($trace_end eq "R")||($trace_end eq "REVERSE"))
        		{
            		$header_hash{$ti}="\@Template_id=${template_id}_Insert_size=${insert_size}_Insert_sd=${insert_sd}#/1\n";
        		}
        	}
    	}
        
    }
}

print "stage 1: header hash for first 3 files done\n";
open(IN_ANC,"</homes/bioinfo/Tcas/sanger_reads/anc.tribolium_castaneum.004") or die $!; 	# request a warning
while(<IN_ANC>)
{
	unless (/TEMPLATE_ID/)
	{
	    @row= split("\cI");
	    ($insert_size,$insert_sd,$template_id,$ti,$trace_end,$trace_name)=($row[26],$row[27],$row[56],$row[57],$row[59],$row[61]); #file 4
	    if ($template_id_hash{$template_id}){$template_id_hash{$template_id}=$template_id_hash{$template_id}+1;}
    	else {$template_id_hash{$template_id}=1;}
    	if (($trace_end eq "F")||($trace_end eq "FORWARD"))
    	{
        	$header_hash{$ti}="\@Template_id=${template_id}_Insert_size=${insert_size}_Insert_sd=${insert_sd}#/2\n";
    	}
    	elsif (($trace_end eq "R")||($trace_end eq "REVERSE"))
    	{
        	$header_hash{$ti}="\@Template_id=${template_id}_Insert_size=${insert_size}_Insert_sd=${insert_sd}#/1\n";
    	}
    }
}
@timeData = localtime(time);
print "stage 2: header hash for 4th file done @timeData\n";
$/ = ">";
################# list all files I am interested in ########################
my $fastafiles=`ls /homes/bioinfo/Tcas/sanger_reads/fasta.tribolium_castaneum.00*`;
my @fastafiles=split(/\n/,$fastafiles);
foreach (@fastafiles) #loop through list of files
{
    chomp;
    open (IN_FASTA,"<$_");
    ########## write fasta and qual split by F and R ####################
    my $count = 0;
    while (<IN_FASTA>)
    {
        unless ($count == 0)
        {
            chomp;
            /\|ti\|(\S+)/;
            $seq_hash{$1}=$_;
        }
        $count++;
        
    }
    @timeData = localtime(time);
    print "stage 2: loop though fastas partially done @timeData\n"
}
@timeData = localtime(time);
print "stage 3: loop though fastas done @timeData\n";
$/ = ">";
################# list all files I am interested in ########################
my $qualfiles=`ls /homes/bioinfo/Tcas/sanger_reads/qual.tribolium_castaneum.00*`;
my @qualfiles=split(/\n/,$qualfiles);
foreach (@qualfiles) #loop through list of files
{
    chomp;
    open (IN_QUAL,"<$_");
    my (${filename}, ${directories}, ${suffix}) = fileparse($_);
    my $qual0 =33;
    my $count = 0;
    while (<IN_QUAL>)
    {
        unless ($count == 0)
        {
            chomp;
            my ($qdef, @qualLines) = split /\n/;
            $qdef =~ /\|ti\|(\S+)/;
            my $temp_ti=$1;
            my $qualString = join ' ', @qualLines;
            $qualString =~ s/\s+/ /g;
            my @quals = split / /, $qualString;
            ######## create or designate filehandle ########
            if ($header_hash{$temp_ti} =~ /^@\S+_Insert_size=(\S+)_Insert_sd=\S+\#\/([12])\n/)# match the header
            {
                unless (($fastq{"len$1pair$2"}))# start the first file
                {
                    $fastq{"len$1pair$2"}=1;
                    $path=${directories}."Trib_cast_R".$2."_".$1;
                    $filehandle="FASTQ".$2."_".$1;
                    open($filehandle, ">$path");
                }
                else
                {
                    $filehandle="FASTQ".$2."_".$1;
                }
                print {$filehandle} "$header_hash{$temp_ti}";
                my ($fdef, @seqLines) = split (/\n/,$seq_hash{$temp_ti});
                my $seq = join '', @seqLines;
                print {$filehandle} "$seq\n";
                print {$filehandle} "+\n";
                foreach (@quals)
                {
                    unless ($_ eq ''){print {$filehandle} chr($_ + 33);}
                }
                print {$filehandle} "\n";
            }
        }
        $count++;
    }
    @timeData = localtime(time);
    print "stage 3: loop though qual partially done @timeData\n"
}
print "stage 4: loop though quals done\n";
