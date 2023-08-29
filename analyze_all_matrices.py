import os
from scipy.stats.stats import pearsonr

ksizes = [11, 21, 31]
seed_list = range(20)

if __name__ == '__main__':
    for k in ksizes:
        ground_truth_mat_filename = f'fmh_signatures_and_matrices/sourmash_cos_sim_mat_k_{k}_scaled_1.csv'
        f = open(ground_truth_mat_filename, 'r')
        order = f.readlines()[0].strip()
        order = order.replace('../ecoli_genomes/', '')
        order_ground_truth = order.replace('.gz', '')
        f.close()

        for seed in seed_list:
            fmh_cos_sim_mat_filename = f'fmh_signatures_and_matrices/sourmash_cos_sim_mat_k_{k}_scaled_1000_seed_{seed}.csv'
            f = open(fmh_cos_sim_mat_filename, 'r')
            order = f.readlines()[0].strip()
            order = order.replace('../ecoli_genomes/', '')
            order_this_file = order.replace('.gz', '')
            f.close()

            if order_this_file != order_ground_truth:
                print('NOOO')

        for seed in seed_list:
            mash_cos_sim_mat_filename = f'mash_sketches/mash_cos_sim_mat_k_{k}_seed_{seed}'
            f = open(mash_cos_sim_mat_filename, 'r')
            order_this_file = f.readlines()[0].strip()
            f.close()

            if order_this_file != order_ground_truth:
                print('NOOO')

        # so, we know that the order in all files are the same
        # therefore, can now just concat all rows one after another
        ground_truth_mat_filename = f'fmh_signatures_and_matrices/sourmash_cos_sim_mat_k_{k}_scaled_1.csv'
        f = open(ground_truth_mat_filename, 'r')
        all_lines = f.readlines()
        ground_truth_vector = []
        for line in all_lines[1:]:
            line = line.strip()
            ground_truth_vector = ground_truth_vector + [ float(x) for x in line.split(',')]
        f.close()

        for seed in seed_list:
            fmh_cos_sim_mat_filename = f'fmh_signatures_and_matrices/sourmash_cos_sim_mat_k_{k}_scaled_1000_seed_{seed}.csv'
            f = open(fmh_cos_sim_mat_filename, 'r')
            all_lines = f.readlines()
            vector_this_file = []
            for line in all_lines[1:]:
                line = line.strip()
                vector_this_file = vector_this_file + [ float(x) for x in line.split(',')]
            f.close()

            print( pearsonr(ground_truth_vector, vector_this_file) )

        for seed in seed_list:
            mash_cos_sim_mat_filename = f'mash_sketches/mash_cos_sim_mat_k_{k}_seed_{seed}'
            f = open(mash_cos_sim_mat_filename, 'r')
            all_lines = f.readlines()
            vector_this_file = []
            for line in all_lines[1:]:
                line = line.strip()
                vector_this_file = vector_this_file + [ float(x) for x in line.split(',')]
            f.close()

            print( pearsonr(ground_truth_vector, vector_this_file) )
