f = open('script.sh', 'w')
for k in [11, 21, 31]:
    f.write( f'mkdir fmh_signatures_k_{k}_scaled_1\n' )
    f.write( f'sourmash compute ../ecoli_genomes/* --outdir fmh_signatures_k_{k}_scaled_1 -k {k} --scaled 1 --seed 0 --track-abundance\n' )
    f.write( f'sourmash compare fmh_signatures_k_{k}_scaled_1 --similarity-matrix --csv sourmash_cos_sim_mat_k_{k}_scaled_1.csv\n' )

for seed in range(20):
    for k in [11, 21, 31]:
        for scaled in [1000]:
            f.write( f'mkdir fmh_signatures_k_{k}_scaled_{scaled}_seed_{seed}\n' )
            f.write( f'sourmash compute ../ecoli_genomes/* --outdir fmh_signatures_k_{k}_scaled_{scaled}_seed_{seed}/ -k {k} --scaled {scaled} --seed {seed} --track-abundance\n' )
            f.write( f'sourmash compare fmh_signatures_k_{k}_scaled_{scaled}_seed_{seed} --similarity-matrix --csv sourmash_cos_sim_mat_k_{k}_scaled_{scaled}_seed_{seed}.csv\n' )
