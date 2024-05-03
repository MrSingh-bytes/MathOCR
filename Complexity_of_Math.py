import xml.etree.ElementTree as ET
import argparse

# 1. Calculate the Length of the MathML tree

def calculate_mathml_length(mathml):
    """
    Input: MathML string
    Returns: Length of the MathML tree considering only <mi> elements
    """
    tree = ET.fromstring(mathml)  # Parse the MathML string into an ElementTree object
    length = calculate_tree_length(tree)  # Calculate the length of the MathML tree
    return length

def calculate_tree_length(tree):
    """
    Input: Node of the MathML tree
    Returns: Length of the tree considering only <mi> elements
    """
    length = 0  # Initialize the length to 0

    if tree.tag == "mi":  # If the current node is an <mi> element, count it
        length += 1

    for child in tree:
        length += calculate_tree_length(child)  # Recursively calculate length of each child

    return length


# 2. Calculate the Depth(Complexity) of the MathML tree

def calculate_mathml_complexity(mathml):
    tree = ET.fromstring(mathml)  # Parse the MathML string into an ElementTree object
    complexity = calculate_tree_depth(tree) - 1  # Calculate the depth of the MathML tree
    return complexity

def calculate_tree_depth(tree):
    if len(tree) == 0:
        return 1  # Depth of a single node is 1
    
    max_child_depth = 0
    for child in tree:
        child_depth = calculate_tree_depth(child)
        max_child_depth = max(max_child_depth, child_depth)
    
    return max_child_depth + 1  # Depth of the current node is maximum child depth + 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate MathML length and depth.')
    parser.add_argument('mathml', type=str, nargs='?', help='MathML string')
    parser.add_argument('--file', type=str, help='Path to file containing the MathML strings')
    parser.add_argument('--length', action='store_true', help='Calculate the length of the MathML tree(s)')
    parser.add_argument('--depth', action='store_true', help='Calculate the depth of the MathML tree(s)')
    parser.add_argument('--both', action='store_true', help='Calculate both length and depth of the MathML tree(s)')

    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r') as f:
            lines = f.readlines()

        mathml_block = ""
        reading_block = False

        for line in lines:
            line = line.strip()
            
            if "<math>" in line:
                reading_block = True
                mathml_block = ""
            
            if reading_block:
                mathml_block += line
            
            if "</math>" in line:
                reading_block = False

                # Process the completed MathML block
                print(f"Processing MathML block: {mathml_block[:30]}...")
                
                # Process the completed MathML block
                if args.length or args.both:
                    length = calculate_mathml_length(mathml_block)
                    print(f"MathML length: {length}")

                if args.depth or args.both:
                    depth = calculate_mathml_complexity(mathml_block)
                    print(f"MathML depth: {depth}")

    elif args.mathml:
        mathml = args.mathml
        if args.length or args.both:
            length = calculate_mathml_length(mathml)
            print(f"MathML length: {length}")
        
        if args.depth or args.both:
            depth = calculate_mathml_complexity(mathml)
            print(f"MathML depth: {depth}")

    else:
        print("Please provide either a MathML string or a file path.")
        exit(1)

