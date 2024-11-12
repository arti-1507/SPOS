# Direct input data for MNT, MDT, and ALA
mnt = [
    ["1", "M1", "1"],
    ["2", "M2", "5"]
]

mdt = [
    ["1", "MOVER #A, #X"],
    ["2", "ADD #A, ='1'"],
    ["3", "MOVER #B, #Y"],
    ["4", "ADD #B, ='5'"],
    ["5", "MOVER #U, #P"],
    ["6", "MOVER #V, #Q"],
    ["7", "ADD #U, ='15'"],
    ["8", "ADD #V, ='10'"]
]

ala = {
    "M1": {
        "&X": ("10", None),
        "&Y": ("20", None),
        "&A": (None, "AREG"),
        "&B": (None, "CREG")
    },
    "M2": {
        "&P": ("100", None),
        "&Q": ("200", None),
        "&U": (None, "BREG"),
        "&V": (None, "AREG")
    }
}


# Function to expand macros
def expand_macro(macro_call):
    parts = macro_call.split()
    macro_name = parts[0]
    args = parts[1].split(",") if len(parts) > 1 else []

    # Retrieve ALA for this macro
    arg_map = ala.get(macro_name, {}).copy()

    # Parse arguments and update the ALA mapping
    for arg in args:
        if "=" in arg:
            param, value = arg.split("=")
            if param in arg_map:
                arg_map[param] = (arg_map[param][0], value)  # Update register

    # Expand using MDT
    expanded_code = []
    mnt_entry = next((entry for entry in mnt if entry[1] == macro_name), None)
    if mnt_entry:
        start_index = int(mnt_entry[2]) - 1
        for i in range(start_index, start_index + 4):  # Expand exactly 4 lines for each macro
            stmt = mdt[i][1]
            for param, (value, register) in arg_map.items():
                if value:
                    stmt = stmt.replace(f"#{param.strip('&')}", value)
                if register:
                    stmt = stmt.replace(f"#{param.strip('&')}", register)
            expanded_code.append(stmt)
    return expanded_code


# Input code to process
input_code = [
    "START 100",
    "M1 10, 20, &B=CREG",
    "M2 100, 200, &V=AREG, &U=BREG",
    "END"
]


# Generate the expanded assembly code
expanded_code = []
for line in input_code:
    if line.startswith("START") or line.startswith("END"):
        expanded_code.append(line)
    else:
        expanded_code.extend(expand_macro(line))


# Output the expanded code
print("Expanded Code:")
for line in expanded_code:
    print(line)
