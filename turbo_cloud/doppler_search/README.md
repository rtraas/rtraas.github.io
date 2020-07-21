# How to use the `FDoppSearch` bash scripts to run `turbo_seti` in bulk

## Overview

A bash script is any file with the extension ".sh".  Bash scripts, being a type of shell script, are typically used for executing programs and file manipulation.  In our case, they are used as a means to run `turbo_seti` in bulk.  This means that when you run these bash scripts, as soon as `turbo_seti` has finished execution on on file A, it will automatically begin execution on file B, then file C, and so on.  So instead of having to manually invoke `turbo_seti` on file A, waiting for the program to run its course, and then manually invoking `turbo_seti` on file B,etc., you can do something else while `turbo_seti` runs in the background.  This will be essential should you need to run `turbo_seti` on a large number of files (hundreds, thousands, whatever power of 10 it may be) as the thought of manually invoking `turbo_seti` for every file on Breakthrough Listen's 1,000,000 star survey makes me gag.

## Prerequisites

So my talk of running `turbo_seti` using bash scripts has intrigued you, has it?  Well, before you can start using the ones provided in this directory, there are some lines of code that need to be edited.  We're going to use C_BandFDoppSearch.sh as the example through which we'll walk through together.

Here's the template script found in this directory:
```
#!/bin/bash													#1
#This is copy-pasted from the file `template_script.txt`							#2
### Based off of /datax/scratch/karenp/turbo_event at the Breakthrough Listen Data Center at UC-Berkeley	#3
#example command: for file in /tess_container/seti_tess/c_band/*0000.h5; do	       		    	   	#4
for file in ABSOLUTE_OR_RELATIVE_PATH_TO_FILES_TO_RUN_TURBO_SETI_ON; do						#5
  if [[ "$file" == *"IDENTIFIER"* ]] || [[ "$file" == *"ANOTHER_OPTIONAL_IDENTIFIER"* ]]; then			#6
    echo "$file"   		     	   	      			     	 				#7
														#8
   time turboSETI "$file" -s 10 -M 4 -o ABSOLUTE_OR_RELATIVE_PATH_TO_DESIRED_OUTPUT_DIRECTORY_FOR_.DAT_FILES	#9
														#10
    echo "complete"												#11
  else														#12
    echo "invalid"												#13
  fi														#14
done														#15
```


The first thing that you might recognize is that I've provided line numbers so that it will be easier to spot certain lines of code when I reference them later on.  For those of you who may not know, all characters and text that follow the pound symbol (#) are ignored when the script is run.  So you are free to leave the line numbers in, but it won't make any difference if you don't, as they are merely included in here for this guide.  Now, let's get on with it.

## Customizing your scripts

There are only 3 lines that need to be changed to repurpose this script to fit your needs.

`Line 5`:	What line 5 is saying is "find every file contained in the specified path and do what I say in the lines after this".  Simply switch `ABSOLUTE_OR_RELATIVE_PATH_TO_FILES_TO_RUN_TURBO_SETI_ON` with the path to the directory where your `.h5` and/or `.fil` filterbank files are located.  You can specify an additional option to filter out files that you don't want the script to include by using an asterisk (`*`) followed by perhaps a certain file extension or a substring of a particular file name.  This works just like it does when searching for files in a terminal session.  I've included an example on line 4 demonstrating one of the many ways to limit which files will be selected.  Other examples include using "`*HIP*`" to select files whose targets come from the HIPPARCOS catalog, `*.fil` to only select files with the `.fil` extension.  You can even use `**` to search through all subdirectories, examples being `/parent_directory/\**` to search through all subdirectories of `parent_directory` or, better yet, use `/parent_directory/\**/*.h5` to specify that you want to include all files in all subdirectories of `parent_directory` if the files have the `.h5` extension.

`Line 6`:	Similar to what you can do in line 5, this is simply another way to select for certain files that meet a given criteria.  For example, if you wanted to only run `turbo_seti` on files with the `.h5` extension, but didn't specify that in line 5, you could specify it here by saying `if [[ "$file" == *".h5"* ]]; then` instead of what you see in the version listed here.  If you're confused about why the asterisks (`*`) are outside of the double quotes (`"`), it's because this is the syntax that shell scripts are written with.  The "double bar" symbol `||` denotes that this I've added an `or` statement to the current boolean `if` statement.  You can use anything after the double bars, and the use of it here in this example is trivial and mostly just for demonstrating that the option exists.  Of course I could have just as well used a different conditional operator and it would've worked all the same.  **Just don't replace `$file` because this is referencing to the variable named `file` that we defined on line 5!**

`Line 9`:	  The last thing is to replace `ABSOLUTE_OR_RELATIVE_PATH_TO_DESIRED_OUTPUT_DIRECTORY_FOR_.DAT_FILES` with the name of the directory you wish to save the output files produced by turbo_seti.  If you instead delete this piece of code along with the flag `-o` that specifies that an alternative output directory, in which the resulting line would read `time turboSETI "$file" -s 10 -M 4`, then the output directory would be the current working directory.  Additionally, if you did not change the numeric values specified after the flags `-s` and `-M`, then you would telling turbo_seti to complete a search for signals clearing an SNR threshold of 10 and are drifting at 4 Hz/s.
