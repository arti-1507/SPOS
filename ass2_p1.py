# Define the predefined pseudo-ops, instructions, and their respective sizes
INSTRUCTIONS = {
    "LOAD": 1, "ADD": 1, "MULT": 1, "TRANS": 1, "PRINT": 1, "STOP": 1, "SUB": 1
}
DIRECTIVES = {
    "START": 0, "DS": 0, "DC": 0, "EQU": 0, "ORIGIN": 0, "END": 0, "LTORG": 0
}

# Sample assembly code
assembly_code = [
    ["", "START", "100"],
    ["A", "DS", "5"],
    ["", "LOAD", "A"],
    ["", "ADD", "AREG,=’5’"],
    ["", "MULT", "BREG,=’10’"],
    ["", "TRANS", "L"],
    ["L2", "PRINT", "L1"],
    ["", "LTORG", ""],
    ["L", "ADD", "AREG,=’5’"],
    ["", "SUB", "BREG,=’15’"],
    ["", "ADD", "B"],
    ["B", "EQU", "L+10"],
    ["", "ORIGIN", "L2+20"],
    ["L1", "DS", "5"],
    ["C", "DC", "10"],
    ["", "STOP", ""],
    ["", "END", ""]
]

# Initialize tables
symbol_table = {}
literal_table = []
pool_table = []
location_counter = 0
pool_index = 0

# Helper functions for symbols and literals
def add_symbol(symbol, address, length=1, type="Label"):
    if symbol and symbol not in symbol_table:
        symbol_table[symbol] = {"Address": address, "Length": length, "Type": type}

def add_literal(literal):
    if literal not in [lit["Literal"] for lit in literal_table]:
        literal_table.append({"Literal": literal, "Address": None})

# Main assembler pass 1 function
def assembler_pass1(assembly_code):
    global location_counter, pool_index
    
    for line in assembly_code:
        label, mnemonic, operand = line
        
        # START directive
        if mnemonic == "START":
            location_counter = int(operand)
        
        # DS and DC
        elif mnemonic in ["DS", "DC"]:
            size = int(operand)
            add_symbol(label, location_counter, size, mnemonic)
            location_counter += size
        
        # LTORG (handle literals)
        elif mnemonic == "LTORG":
            pool_table.append(pool_index)
            for lit in literal_table[pool_index:]:
                lit["Address"] = location_counter
                location_counter += 1
            pool_index = len(literal_table)
        
        # EQU directive
        elif mnemonic == "EQU":
            expression = operand.replace("+", "").replace("-", "")
            base_address = symbol_table.get(expression, {}).get("Address", 0)
            offset = int(operand.split("+")[-1]) if "+" in operand else 0
            add_symbol(label, base_address + offset, 0, "EQU")
        
        # ORIGIN directive
        elif mnemonic == "ORIGIN":
            expression, offset = operand.split("+")
            location_counter = symbol_table[expression]["Address"] + int(offset)
        
        # Instructions and literals in operands
        elif mnemonic in INSTRUCTIONS:
            add_symbol(label, location_counter, INSTRUCTIONS[mnemonic], "Instruction")
            if "=" in operand:
                literal = operand.split(",=")[-1].replace("’", "")
                add_literal(f"={literal}")
            location_counter += INSTRUCTIONS[mnemonic]
        
        # END directive
        elif mnemonic == "END":
            pool_table.append(pool_index)
            for lit in literal_table[pool_index:]:
                lit["Address"] = location_counter
                location_counter += 1

# Run pass 1
assembler_pass1(assembly_code)

# Display Symbol Table
print("Symbol Table")
print("Symbol\tAddress")
for symbol, info in symbol_table.items():
    print(f"{symbol}\t{info['Address']}")

# Display Literal Table
print("\nLiteral Table")
print("Index\tLiteral\tAddress")
for i, literal in enumerate(literal_table):
    print(f"{i}\t{literal['Literal']}\t{literal['Address']}")

# Display Pool Table
print("\nPool Table")
print("Pool Number\tStart Index")
for i, pool in enumerate(pool_table):
    print(f"{i}\t{pool}")
