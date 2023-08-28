import subprocess
import os
import argparse
import json

def compute_cosine_similarity(mash_sketch1, mash_sketch2):
    # no abundance info is here
    # cos theta = |A.B| / ( |A|.|B| )
    # |A.B| = number of commons in A and B
    # |A| and |B| are: sqrt( len(A, or B) )
    num_common = set(mash_sketch1).intersection(set(mash_sketch2))
    len1 = (len(mash_sketch1))**(0.5)
    len2 = (len(mash_sketch2))**(0.5)
    return num_common/(len1*len2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create mash sketches from a list of fna.gz files.")
    parser.add_argument('--genome_dir', '-g', type=str, help="Directory where the genomes are")
    args = parser.parse_args()
    genomes_directory = args.genome_dir

    file_list = os.listdir(genomes_directory)
    filename_to_sketch = {}
    for filename in file_list:
        complete_file_path = os.path.join(genomes_directory, filename)
        mash_sketch_filename = filename+'.msh'
        mash_readable_sketch_filename = mash_sketch_filename+'.json'

        cmd = f'mash sketch -k 21 {complete_file_path} -o {mash_sketch_filename}'
        subprocess.call(cmd.split(' '))

        cmd = f'mash info {mash_sketch_filename} -d'
        f = open(mash_readable_sketch_filename, 'w')
        subprocess.call(cmd.split(' '), stdout=f)
        f.close()

        f = open(mash_readable_sketch_filename, 'r')
        sketch_data = json.load(f)['sketches'][0]['hashes']
        f.close()
        filename_to_sketch[filename] = sketch_data

    # these sketches are all 0-1 (no abundance info is kept by mash)
    for filename1 in file_list:
        for filename2 in file_list:
            print(filename1, filename2, compute_cosine_similarity( filename_to_sketch[filename1], filename_to_sketch[filename2] ))
