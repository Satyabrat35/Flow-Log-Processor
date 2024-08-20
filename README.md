# Overview
The Flow Log Processor is a tool to analyze and process network flow logs. It
uses protocol and lookup tables to categorize and count different types of network 
traffic based on their tags and port/protocol combinations.

# Handle Large Files
Instead of loading the entire file content into memory and reading
line by line, I am reading the file in smaller chunks using a buffer size, which
can process the data incrementally without overwhelming the system's memory.
This is beneficial for files `>1GB`. This is an efficient way of reading and processing files.
Reference - https://medium.com/@anuragv.1020/chunk-by-chunk-tackling-big-data-with-efficient-file-reading-in-chunks-c6f7cf153ccd

## Requirements 
1. The flow log data file follows the format:

`<version> <account-id> <interface-id> <srcaddr> <dstaddr> <srcport> <dstport> <protocol> <packets> <bytes> <start> <end> <action> <log-status>`

2. The flow log data is in the version 2 default format, which includes 14 fields:

`VERSION_2_FIELDS_COUNT = 14`

`DSTPORT_FIELD_INDEX = 6`

`PROTOCOL_FIELD_INDEX = 7`

3. Input file as well as the file containing tag mappings are plain text (ascii) files  
4. The flow log file size can be up to 10 MB 
5. The lookup file can have up to 10000 mappings 
6. The tags can map to more than one port, protocol combinations.  for e.g. sv_P1 and sv_P2 in the sample example
7. The matches should be case insensitive 

## How to run
1. Download repository (zip) - https://github.com/Satyabrat35/Flow-Log-Processor
2. Go to project directory - `cd Flow-Log-Processor-main`
3. Run program - `python main.py`
4. Run tests - `python tests.py`

## Directory
1. `FlowLogRecords.py`: Contains functions for loading lookup tables, processing flow logs
2. `files`: Contains sample and large flow log and look up tables
3. `main.py`: The main script to execute the flow log processing
4. `tests.py`: Unit Test cases

## Error Handling
The script raises exceptions if input files are not found or if there are issues processing the files.
It ensures that the input files are correctly formatted and exist at the specified paths.

## Output
main.py

```
(base) satya@Kynes-Peace illumio % gtime -v python main.py
[INFO] Loading protocol assignments from files/protocol_assignment.csv...
[INFO] Generating lookup table from files/lookup_large.csv...
[INFO] Analyzing and processing flow logs from files/flow_log_large.txt...
Final Results written to -> output_large.csv
        Command being timed: "python main.py"
        User time (seconds): 0.14
        System time (seconds): 0.02
        Percent of CPU this job got: 66%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.25
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 15444
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 453
        Minor (reclaiming a frame) page faults: 3645
        Voluntary context switches: 305
        Involuntary context switches: 401
        Swaps: 0
        File system inputs: 0
        File system outputs: 0
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 16384
        Exit status: 0
```

tests.py

```
(base) satya@Kynes-Peace illumio % gtime -v python tests.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.004s

OK
        Command being timed: "python tests.py"
        User time (seconds): 0.04
        System time (seconds): 0.06
        Percent of CPU this job got: 40%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.26
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 15008
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 1024
        Minor (reclaiming a frame) page faults: 3760
        Voluntary context switches: 869
        Involuntary context switches: 458
        Swaps: 0
        File system inputs: 0
        File system outputs: 0
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 16384
        Exit status: 0

```