# Symbol table, literal table, and intermediate code
symbol_table = {
    "A": 100,
    "L1": 103,
    "D": 101,
    "L2": 107,
    "C": 100,
    "B": 109
}

literal_table = {
    "='12'": 106,
    "='5'": 110
}

intermediate_code = [
    ("IS", "05", "1", "B"),   # MOVEM AREG, B
    ("IS", "01", "1", "C"),   # ADD AREG, C
    ("IS", "04", "1", "='12'"), # MOVER AREG, ='12'
    ("AD", "04"),             # Address Directive (no machine code)
    ("AD", "05"),             # Address Directive (no machine code)
    ("IS", "10", "", "D"),   # PRINT D
    ("AD", "03"),             # Address Directive (no machine code)
    ("IS", "04", "1", "='5'"), # MOVER AREG, ='5'
    ("DL", "01", "C", "5"),   # Data Literal
    ("AD", "03"),             # Address Directive (no machine code)
    ("IS", "00", "", ""),    # STOP
    ("DL", "01", "C", "19"),  # Data Literal
    ("AD", "02")              # Address Directive (no machine code)
]

def assembler_pass2(intermediate_code, symbol_table, literal_table):
    machine_code = []
    
    for line in intermediate_code:
        instruction_type = line[0]

        if instruction_type == "IS":
            mnemonic = line[1]   # Mnemonic (opcode)
            address_type = line[2]  # Address type (either '1' or 'S')
            operand = line[3] if len(line) > 3 else ""
            
            # Check if the operand is a symbol or literal
            if operand in symbol_table:
                # It's a symbol, get its address from the symbol table
                address = symbol_table[operand]
            elif operand in literal_table:
                # It's a literal, get its address from the literal table
                address = literal_table[operand]
            else:
                address = operand  # If it's already a number or address

            # Add machine code line
            machine_code.append(f"{mnemonic} {address_type} {address}")

        elif instruction_type == "IS" and line[1] in ["10", "00"]:
            # For PRINT (10) and STOP (00), address is 0 (since they don't use registers)
            mnemonic = line[1]
            address_type = "" if line[1] == "10" else "00"  # Both PRINT and STOP use no operand
            machine_code.append(f"{mnemonic} {address_type} 000")
    
        elif instruction_type == "AD" or instruction_type == "DL":
            # For AD and DL, we just ignore them in the machine code generation process.
            continue
    
    return machine_code

# Generate machine code
generated_code = assembler_pass2(intermediate_code, symbol_table, literal_table)

# Print machine code in the desired format
for line in generated_code:
    print(line)
