# Direct input data for MNT, MDT, and ALA
mnt = [
    ["1", "INCR", "1"],
    ["2", "DECR", "4"]
]

mdt = [
    ["1", "MOVER &REG, &X"],
    ["2", "ADD &REG, &Y"],
    ["3", "MOVEM &REG, &X"],
    ["4", "MOVER &REG, &A"],
    ["5", "SUB &REG, &B"],
    ["6", "MOVEM &REG, &A"]
]

ala = {
    "INCR": {"&X": None, "&Y": None, "&REG": "AREG"},
    "DECR": {"&A": None, "&B": None, "&REG": "BREG"}
}


# Function to expand macros
def expand_macro(macro_call):
    parts = macro_call.split()
    macro_name = parts[0]
    args = parts[1].split(",") if len(parts) > 1 else []

    # Retrieve and update ALA for this macro
    arg_map = ala.get(macro_name, {}).copy()
    for i, param in enumerate(arg_map):
        if i < len(args):  # Check if the index is within range
            if "=" in args[i]:
                param_name, reg = args[i].split("=")
                if param_name in arg_map:
                    arg_map[param_name] = reg  # Update register
            else:
                arg_map[param] = args[i]  # Update argument value

    # Expand using MDT
    expanded_code = []
    mnt_entry = next((entry for entry in mnt if entry[1] == macro_name), None)
    if mnt_entry:
        start_index = int(mnt_entry[2]) - 1
        end_index = start_index + 3 if macro_name == "INCR" else start_index + 2
        for i in range(start_index, end_index + 1):
            stmt = mdt[i][1]
            for param, value in arg_map.items():
                stmt = stmt.replace(param, value)
            expanded_code.append(stmt)
    return expanded_code


# Input code to process
input_code = [
    "START 100",
    "READ N1",
    "READ N2",
    "INCR N1,N2,REG=CREG",
    "DECR N1,N2",
    "STOP",
    "N1 DS 1",
    "N2 DS 1",
    "END"
]

# Generate the expanded assembly code
expanded_code = []
for line in input_code:
    # Strip any extra spaces and check conditions
    stripped_line = line.strip()
    if (stripped_line.startswith("START") or
        stripped_line.startswith("READ") or
        stripped_line.startswith("STOP") or
        stripped_line.startswith("END") or
        stripped_line.endswith("DS 1")):
        expanded_code.append(line)
    else:
        expanded_code.extend(expand_macro(line))


# Output the expanded code
print("Expanded Code:")
for line in expanded_code:
    print(line)
