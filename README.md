These genomes were downloaded from RefSeq. These genomes are all bacterial. Single chromosome. They also reside in the KEGG database.

Commands:
-------------
sourmash sketch dna * -o ../signatures_scaled_1000/signatures_k_21_scaled_1000 -p k=21,scaled=1000
/usr/bin/time -v sourmash compare signatures_k_21_scaled_1 -o compare_results
sourmash plot compare_results


# Ecoli time and memory
k=21, saled=1000
------------------
Command being timed: "sourmash compare ecoli_signatures_k_21_scaled_1000.sig -o compare_results_k_21_scaled_1000"
User time (seconds): 2.97
System time (seconds): 12.83
Percent of CPU this job got: 2406%
Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.65
Average shared text size (kbytes): 0
Average unshared data size (kbytes): 0
Average stack size (kbytes): 0
Average total size (kbytes): 0
Maximum resident set size (kbytes): 92604
Average resident set size (kbytes): 0
Major (requiring I/O) page faults: 0
Minor (reclaiming a frame) page faults: 17425
Voluntary context switches: 305
Involuntary context switches: 116948
Swaps: 0
File system inputs: 0
File system outputs: 48
Socket messages sent: 0
Socket messages received: 0
Signals delivered: 0
Page size (bytes): 4096
Exit status: 0


Command being timed: "sourmash compare ecoli_signatures_k_21_scaled_1000.sig -o compare_results_k_21_scaled_1000"
User time (seconds): 2.70
System time (seconds): 13.19
Percent of CPU this job got: 2480%
Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.64
Average shared text size (kbytes): 0
Average unshared data size (kbytes): 0
Average stack size (kbytes): 0
Average total size (kbytes): 0
Maximum resident set size (kbytes): 92316
Average resident set size (kbytes): 0
Major (requiring I/O) page faults: 3
Minor (reclaiming a frame) page faults: 17439
Voluntary context switches: 369
Involuntary context switches: 154
Swaps: 0
File system inputs: 8
File system outputs: 48
Socket messages sent: 0
Socket messages received: 0
Signals delivered: 0
Page size (bytes): 4096
Exit status: 0


k=21, scaled=1
---------------------
Command being timed: "sourmash compare ecoli_signatures_k_21_scaled_1.sig -o compare_results_k_21_scaled_1"
User time (seconds): 184.52
System time (seconds): 67.76
Percent of CPU this job got: 106%
Elapsed (wall clock) time (h:mm:ss or m:ss): 3:57.07
Average shared text size (kbytes): 0
Average unshared data size (kbytes): 0
Average stack size (kbytes): 0
Average total size (kbytes): 0
Maximum resident set size (kbytes): 10017772
Average resident set size (kbytes): 0
Major (requiring I/O) page faults: 2
Minor (reclaiming a frame) page faults: 39261570
Voluntary context switches: 464
Involuntary context switches: 904
Swaps: 0
File system inputs: 0
File system outputs: 48
Socket messages sent: 0
Socket messages received: 0
Signals delivered: 0
Page size (bytes): 4096
Exit status: 0

Command being timed: "sourmash compare ecoli_signatures_k_21_scaled_1.sig -o compare_results_k_21_scaled_1"
User time (seconds): 184.03
System time (seconds): 65.75
Percent of CPU this job got: 106%
Elapsed (wall clock) time (h:mm:ss or m:ss): 3:54.59
Average shared text size (kbytes): 0
Average unshared data size (kbytes): 0
Average stack size (kbytes): 0
Average total size (kbytes): 0
Maximum resident set size (kbytes): 10017456
Average resident set size (kbytes): 0
Major (requiring I/O) page faults: 3
Minor (reclaiming a frame) page faults: 39300789
Voluntary context switches: 401
Involuntary context switches: 793
Swaps: 0
File system inputs: 8
File system outputs: 48
Socket messages sent: 0
Socket messages received: 0
Signals delivered: 0
Page size (bytes): 4096
Exit status: 0
