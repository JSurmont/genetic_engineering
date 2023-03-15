import os.path


dna_elements_pairs = {'T': 'A', 'A': 'T', 'C': 'G', 'G': 'C'}


def generate_complementary_strand(strand: str) -> str:
    new_strand: str = ''
    for i in strand:
        if i not in dna_elements_pairs:
            raise Exception(f"Element {i} isn't constitutive of DNA (constitutive elements: T, A, C, G).")
        new_strand += dna_elements_pairs[i]
    return new_strand


def determine_sticky_end_cut_index_by_side(strand: str, sequence_type: str, side: str, restrictions: dict) -> int:
    if sequence_type not in ('original', 'complementary'):
        raise Exception(f"Sequence type is not properly defined.\n"
                        f"{sequence_type} does not exist in the restriction dictionary: {restrictions}")
    if side == 'left':
        return strand.index(restrictions[sequence_type][side]) + restrictions[sequence_type]['cut_position']
    elif side == 'right':
        return strand.rindex(restrictions[sequence_type][side]) + restrictions[sequence_type]['cut_position']
    else:
        raise Exception("Side is not properly defined.\n"
                        f"{side} does not exist in the restriction dictionary: {restrictions}")


def determine_plasmid_strand_cut_by_side(strand: str, sequence_type: str, side: str, restrictions: dict) -> str:
    cut_index = determine_sticky_end_cut_index_by_side(strand, sequence_type, side, restrictions)
    if side == 'left':
        return strand[:cut_index]
    elif side == 'right':
        return strand[cut_index:]
    else:
        raise Exception("Side is not properly defined.\n"
                        f"{side} does not exist in the restriction dictionary: {restrictions}")


def determine_gfp_strand_with_sticky_ends(strand: str, sequence_type: str, restrictions: dict) -> str:
    left_cut_index = determine_sticky_end_cut_index_by_side(strand, sequence_type, 'left', restrictions)
    right_cut_index = determine_sticky_end_cut_index_by_side(strand, sequence_type, 'right', restrictions)
    return strand[left_cut_index:right_cut_index]


def generate_final_strand(plasmid: dict, gfp: dict, strand_type: str) -> str:
    return plasmid[strand_type]['left'] + gfp[strand_type] + plasmid[strand_type]['right']
