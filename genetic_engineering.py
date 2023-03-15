import os
from dna_tools.sequencing import generate_complementary_strand, determine_plasmid_strand_cut_by_side, \
    determine_gfp_strand_with_sticky_ends, generate_final_strand

file_name = input("File to parse:\n")

if not os.path.exists(file_name):
    raise Exception(f"File {file_name} not found.")

plasmid_original = ""
plasmid_restriction_site = ""

gfp_original = ""
gfp_restriction_sites = ""

with open(file_name, 'r') as filehandler:
    line_number = 1
    for line in filehandler.readlines():
        match line_number:
            case 1:
                plasmid_original = line.strip()
            case 2:
                plasmid_restriction_site = line.strip()
            case 3:
                gfp_original = line.strip()
            case 4:
                gfp_restriction_sites = line.strip()
            case _:
                print(f"Line {line_number} is out of bound")
        line_number += 1

plasmid_complementary = generate_complementary_strand(plasmid_original)
gfp_complementary = generate_complementary_strand(gfp_original)

restriction_sites_cuts = {
    'plasmid': {
        'original': {
            'left': plasmid_restriction_site,
            'right': plasmid_restriction_site,
            'cut_position': 1
        },
        'complementary': {
            'left': generate_complementary_strand(plasmid_restriction_site),
            'right': generate_complementary_strand(plasmid_restriction_site),
            'cut_position': 5
        }
    },
    'gfp': {
        'original': {
            'left': gfp_restriction_sites.split()[0],
            'right': gfp_restriction_sites.split()[1],
            'cut_position': 1
        },
        'complementary': {
            'left': generate_complementary_strand(gfp_restriction_sites.split()[0]),
            'right': generate_complementary_strand(gfp_restriction_sites.split()[1]),
            'cut_position': 5
        }
    }
}

cut_plasmid = {
    'original': {
        'left': determine_plasmid_strand_cut_by_side(strand=plasmid_original, sequence_type='original',
                                                     side='left', restrictions=restriction_sites_cuts['plasmid']),
        'right': determine_plasmid_strand_cut_by_side(strand=plasmid_original, sequence_type='original',
                                                      side='right', restrictions=restriction_sites_cuts['plasmid'])
    },
    'complementary': {
        'left': determine_plasmid_strand_cut_by_side(strand=plasmid_complementary, sequence_type='complementary',
                                                     side='left', restrictions=restriction_sites_cuts['plasmid']),
        'right': determine_plasmid_strand_cut_by_side(strand=plasmid_complementary, sequence_type='complementary',
                                                      side='right', restrictions=restriction_sites_cuts['plasmid'])
    }
}

cut_gfp = {
    'original': determine_gfp_strand_with_sticky_ends(strand=gfp_original, sequence_type='original',
                                                      restrictions=restriction_sites_cuts['gfp']),
    'complementary': determine_gfp_strand_with_sticky_ends(strand=gfp_complementary, sequence_type='complementary',
                                                           restrictions=restriction_sites_cuts['gfp'])
}


def display_final_strands():
    print(generate_final_strand(cut_plasmid, cut_gfp, 'original'))
    print((generate_final_strand(cut_plasmid, cut_gfp, 'complementary')))


if __name__ == '__main__':
    display_final_strands()
