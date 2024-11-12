# Macro definitions for your provided input
macros = {
    "INCR": [
        ("MOVER", "&REG", "&X"),
        ("ADD", "&REG", "&Y"),
        ("MOVEM", "&REG", "&X")
    ],
    "DECR": [
        ("MOVER", "&REG", "&A"),
        ("SUB", "&REG", "&B"),
        ("MOVEM", "&REG", "&A")
    ]
}

# Define the macro calls
macro_calls = [
    ("INCR", "N1", "N2", "&REG=CREG"),
    ("DECR", "N1", "N2")
]

# Macro Name Table (MNT)
mnt = []
mnt_location = 1  # Starting location for MNT entries
for idx, macro_name in enumerate(macros.keys()):
    mnt.append([idx + 1, macro_name, mnt_location])
    mnt_location += len(macros[macro_name])  # Increment by number of statements

# Macro Definition Table (MDT)
mdt = []
stmt_counter = 1
for macro_name, statements in macros.items():
    for stmt in statements:
        formatted_stmt = f"{stmt[0]} #{stmt[1].replace('&', '')}, " \
                         f"#{stmt[2].replace('&', '')}"
        mdt.append([stmt_counter, formatted_stmt])
        stmt_counter += 1

# Argument List Array (ALA)
ala = []
ala_counter = 1
for macro_call in macro_calls:
    macro_name = macro_call[0]
    args = macro_call[1:]
    ala_entry = [f"{ala_counter} {macro_name}"]
    for arg in args:
        if "=" in arg:
            param, reg = arg.split("=")
            ala_entry.append(f"{param} (Value: None, Register: {reg})")
        else:
            ala_entry.append(f"{arg} (Value: {arg}, Register: None)")
    ala.append(" ".join(ala_entry))
    ala_counter += 1

# Writing to mnt.txt
with open("mnt.txt", "w") as mnt_file:
    for entry in mnt:
        mnt_file.write(f"{entry[0]} {entry[1]} {entry[2]}\n")

# Writing to mdt.txt
with open("mdt.txt", "w") as mdt_file:
    for entry in mdt:
        mdt_file.write(f"{entry[0]} {entry[1]}\n")

# Writing to ala.txt
with open("ala.txt", "w") as ala_file:
    for entry in ala:
        ala_file.write(f"{entry}\n")

# Output files have been generated
print("Files mnt.txt, mdt.txt, and ala.txt have been created successfully.")
