# WARNING PIPELINE UNDER DEVELOPMENT!!

![alttext](https://raw.githubusercontent.com/i5K-KINBRE-script-share/transcriptome-and-genome-assembly/master/images/ngs_pipelines_on_beocat.png)
##Illumina read cleaning with Trimmomatic
All of the scripts you will need to complete this lab as well as the sample dataset will be copied to your Beocat directory as you follow the instructions below. You should type or paste the text in the beige code block into your terminal as you follow along with the instructions below. If you are not used to commandline, practice with real data is one of the best ways to learn.

If you would like a quick primer on basic linux commands try these 10 minute lessons from Software Carpentry http://swcarpentry.github.io/shell-novice/. To learn to start using Beocat and begin using the terminal go to https://github.com/i5K-KINBRE-script-share/FAQ/blob/master/UsingBeocat.md. Learn how to download files from Beocat at https://github.com/i5K-KINBRE-script-share/FAQ/blob/master/BeocatEditingTransferingFiles.md.

We will be using the script "clean_illumina.py" to organize our working directory and write scripts to clean our adapters from our reads and to remove low quality bases.

To begin this lab your should read about the software we will be using. Trimmomatic will be used to clean raw reads. Trimmomatic cleaning is highly customizable. You can see a detailed parameter list by visiting their manual at http://www.usadellab.org/cms/?page=trimmomatic. We will be using Trimmomatic's custom palindrome adapter cleaning and their max information adaptive quality trimmer. These features along with the ability to efficiently handle paired end data make Trimmomatic a useful tool on Illumina datasets. Read more about Trimmomatic's unique features in their paper http://bioinformatics.oxfordjournals.org/content/30/15/2114.

To find out more about the parameters for "clean_illumina.py" run "python ~/read-cleaning-format-conversion/KSU_bioinfo_lab/clean_illumina/clean_illumina.py -h" or visit its manual at https://github.com/i5K-KINBRE-script-share/read-cleaning-format-conversion/blob/master/KSU_bioinfo_lab/clean_illumina/clean_illumina_MANUAL.md.

###Step 1: Clone the Git repositories 

git clone https://github.com/i5K-KINBRE-script-share/read-cleaning-format-conversion
