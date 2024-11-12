def pass1(input_file):
    mnt = []  # Macro Name Table
    mdt = []  # Macro Definition Table
    ala = []  # Argument List Array
    mnt_index = 1  # Start index for MNT
    mdt_index = 1  # Start index for MDT
    ala_index = 1  # Start index for ALA
    in_macro = False
    macro_name = None
    macro_start_mdt = None
    parameter_map = {}  # Maps each & parameter to #1, #2, etc.

    with open(input_file, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Handle the start of a macro definition
            if line.startswith('MACRO'):
                parts = line.split()
                if len(parts) > 1:
                    macro_name = parts[1]  # Get macro name (e.g., M1, M2)
                    macro_start_mdt = mdt_index  # Start MDT pointer for this macro
                    mnt.append((mnt_index, macro_name, macro_start_mdt))  # Add to MNT
                    mnt_index += 1

                    # Map each parameter with an `&` prefix to `#1`, `#2`, etc.
                    parameter_map = {param: f"#{i + 1}" for i, param in enumerate(parts[2:])}
                    in_macro = True
                    continue
                else:
                    print(f"Warning: Malformed MACRO definition on line: {line}")
                    continue

            # Handle end of a macro definition
            if line.startswith('MEND'):
                mdt.append((mdt_index, "MEND"))  # Add MEND to MDT
                mdt_index += 1
                in_macro = False
                continue

            # Collect macro body and replace parameters with #1, #2, etc.
            if in_macro:
                # Replace & parameters in line with respective # identifiers
                line_with_placeholders = line
                for param, placeholder in parameter_map.items():
                    line_with_placeholders = line_with_placeholders.replace(param, placeholder)

                # Add processed line to MDT
                mdt.append((mdt_index, line_with_placeholders))
                mdt_index += 1

            # Handle macro invocation to store arguments in ALA
            if not in_macro and any(line.startswith(macro) for macro in ["INCR", "DECR"]):
                parts = line.split()
                invoked_macro_name = parts[0]
                params = parts[1:]

                # Now process the parameters for the macro invocation
                # Here we add parameters as a list to the ALA
                ala.append((ala_index, invoked_macro_name, params))
                ala_index += 1

    # Output MNT, MDT, and ALA to files
    with open('mnt2.txt', 'w') as mnt_file:
        for entry in mnt:
            mnt_file.write(f"{entry[0]} {entry[1]} {entry[2]}\n")

    with open('mdt2.txt', 'w') as mdt_file:
        for entry in mdt:
            mdt_file.write(f"{entry[0]} {entry[1]}\n")

    with open('ala2.txt', 'w') as ala_file:
        for entry in ala:
            # Write the ALA content; each entry should be in the form: [Index, Macro Name, [Param1, Param2, ...]]
            ala_file.write(f"{entry[0]} {entry[1]} {' '.join(entry[2])}\n")

    print("Pass 1 complete! MNT, MDT, and ALA saved to mnt.txt, mdt.txt, and ala.txt.")

# Example input file path
input_file = "m2input.txt"

# Call pass1 with the input file
pass1(input_file)
