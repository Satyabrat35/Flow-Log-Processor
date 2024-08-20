# Overview
The Flow Log Processor is a tool to analyze and process network flow logs. It
uses protocol and lookup tables to categorize and count different types of network 
traffic based on their tags and port/protocol combinations.

## Requirements 
1. Input file as well as the file containing tag mappings are plain text (ascii) files  
2. The flow log file size can be up to 10 MB 
3. The lookup file can have up to 10000 mappings 
4. The tags can map to more than one port, protocol combinations.  for e.g. sv_P1 and sv_P2 in the sample above. 
5. The matches should be case insensitive 

# Handle Large Files
Instead of loading the entire file content into memory and reading
line by line, I am reading the file in smaller chunks using a buffer size, which
can process the data incrementally without overwhelming the system's memory.
This is beneficial for files `>1GB`. This is an efficient way of reading and processing files.

## How to run
