import subprocess
import os
import argparse
import json

def compute_cosine_similarity(mash_sketch1, mash_sketch2):
    # no abundance info is here
    # cos theta = |A.B| / ( |A|.|B| )
    # |A.B| = number of commons in A and B
    # |A| and |B| are: sqrt( len(A, or B) )
    num_common = len(set(mash_sketch1).intersection(set(mash_sketch2)))
    len1 = (len(mash_sketch1))**(0.5)
    len2 = (len(mash_sketch2))**(0.5)
    return num_common/(len1*len2)

filename_order = ['GCF_000163235.1_ASM16323v1_genomic.fna','GCF_000164555.1_ASM16455v1_genomic.fna','GCF_000208545.1_ASM20854v2_genomic.fna','GCF_000233875.1_ASM23387v1_genomic.fna','GCF_000249735.1_ASM24973v2_genomic.fna','GCF_000261145.1_Esch_coli_M919_V2_genomic.fna','GCF_000267705.2_ASM26770v2_genomic.fna','GCF_000350665.1_Esch_coli_KTE5_V1_genomic.fna','GCF_000351625.1_Esch_coli_KTE66_V1_genomic.fna','GCF_000352285.1_Esch_coli_KTE46_V1_genomic.fna','GCF_000358895.1_ASM35889v1_genomic.fna','GCF_000456385.1_Esch_coli_HVH_26_4-5703913_V1_genomic.fna','GCF_000458195.1_Esch_coli_HVH_147_4-5893887_V1_genomic.fna','GCF_000459755.1_Esch_coli_KOEGE_58_171a_V1_genomic.fna','GCF_000460055.1_Esch_coli_UMEA_3053-1_V1_genomic.fna','GCF_000462165.2_ASM46216v2_genomic.fna','GCF_000601135.1_ASM60113v1_genomic.fna','GCF_000614595.1_Ec2010EL1058_genomic.fna','GCF_000617745.1_Ec2010C-4529_genomic.fna','GCF_000618265.2_EcF6751_genomic.fna','GCF_000619005.2_Ec2009C-4052_genomic.fna','GCF_000619105.1_Ec2009C-4780_genomic.fna','GCF_000619765.2_Ec2009C-3279_genomic.fna','GCF_000687005.1_ASM68700v1_genomic.fna','GCF_000687025.1_ASM68702v1_genomic.fna','GCF_000700125.1_ASM70012v1_genomic.fna','GCF_000753315.1_FHI35_genomic.fna','GCF_000776375.1_ASM77637v1_genomic.fna','GCF_000779395.1_ASM77939v1_genomic.fna','GCF_000780315.1_ASM78031v1_genomic.fna','GCF_000781995.1_ASM78199v1_genomic.fna','GCF_000986765.1_ASM98676v1_genomic.fna','GCF_001041375.1_ViralProj287958_genomic.fna','GCF_001265335.1_302014_genomic.fna','GCF_001265625.1_100854_genomic.fna','GCF_001267345.1_303289_genomic.fna','GCF_001309985.1_ASM130998v1_genomic.fna','GCF_001521695.1_ASM152169v1_genomic.fna','GCF_001592595.1_ASM159259v1_genomic.fna','GCF_001614975.1_ASM161497v1_genomic.fna','GCF_001692775.1_ASM169277v1_genomic.fna','GCF_001748915.1_ASM174891v1_genomic.fna','GCF_001749235.1_ASM174923v1_genomic.fna','GCF_001881155.1_ASM188115v1_genomic.fna','GCF_001881345.1_ASM188134v1_genomic.fna','GCF_001892405.1_ASM189240v1_genomic.fna','GCF_001892585.1_ASM189258v1_genomic.fna','GCF_001893985.1_ASM189398v1_genomic.fna','GCF_002001595.1_ASM200159v1_genomic.fna','GCF_002002145.1_ASM200214v1_genomic.fna']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create mash sketches from a list of fna.gz files.")
    parser.add_argument('--genome_dir', '-g', type=str, help="Directory where the genomes are")
    parser.add_argument('--ksize', '-k', type=int, help="k-mer size")
    parser.add_argument('--seed', '-s', type=int, help="seed to compute sketxhes")
    parser.add_argument('--output_filename', '-o', type=str, help="output filename, where the matrix will be written")
    args = parser.parse_args()

    genomes_directory = args.genome_dir
    ksize = args.ksize
    seed = args.seed
    output_filename = args.output_filename

    file_list = os.listdir(genomes_directory)
    filename_to_sketch = {}
    for filename in file_list:
        complete_file_path = os.path.join(genomes_directory, filename)
        mash_sketch_filename = filename+'.msh'
        mash_readable_sketch_filename = mash_sketch_filename+'.json'

        cmd = f'mash sketch -k {ksize} {complete_file_path} -o {mash_sketch_filename} -S {seed}'
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
    f_out = open(output_filename, 'w')
    f_out.write(','.join(filename_order)+'\n')
    for filename1 in filename_order:
        cosine_similarities = []
        for filename2 in filename_order:
            sketch1 = filename_to_sketch[filename1+'.gz']
            sketch2 = filename_to_sketch[filename2+'.gz']
            cosine_sim = compute_cosine_similarity(sketch1, sketch2)
            cosine_similarities.append(cosine_sim)
        f_out.write(','.join( [str(cos_sim) for cos_sim in cosine_similarities] ) + '\n')
