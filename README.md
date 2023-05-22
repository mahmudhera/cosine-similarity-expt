These genomes were downloaded from RefSeq. These genomes are all bacterial. Single chromosome. They also reside in the KEGG database.

Commands:
-------------
sourmash sketch dna * -o ../signatures_scaled_1000/signatures_k_21_scaled_1000 -p k=21,scaled=1000
/usr/bin/time -v sourmash compare signatures_k_21_scaled_1 -o compare_results
sourmash plot compare_results
