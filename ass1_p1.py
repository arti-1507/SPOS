# Define Mnemonic Opcode Table (MOT) and Pseudo Opcode Table (POT)
MOT = {
    'START': 'AD', 'END': 'AD', 'DS': 'DL', 'DC': 'DL', 'EQU': 'AD',
    'ORIGIN': 'AD', 'LTORG': 'AD', 'STOP': 'IS', 'MOVER': 'IS',
    'MOVEM': 'IS', 'ADD': 'IS', 'PRINT': 'IS'
}
POT = ['START', 'END', 'LTORG', 'ORIGIN', 'EQU']

# Registers and their numeric codes
REGISTER_CODES = {'AREG': 1, 'BREG': 2, 'CREG': 3, 'DREG': 4}

# Symbol, Literal, Pool Tables, and other initializations
symbol_table = {}
literal_table = []
pool_table = [0]
LC = 0

def process_line(line):
    global LC, literal_table, pool_table
    tokens = line.split()
    label, opcode, operand1, operand2 = None, None, None, None

    # Split tokens based on whether there's a label
    if len(tokens) == 4:
        label, opcode, operand1, operand2 = tokens
    elif len(tokens) == 3:
        if tokens[0] in MOT:
            opcode, operand1, operand2 = tokens
        else:
            label, opcode, operand1 = tokens
    elif len(tokens) == 2:
        opcode, operand1 = tokens
    elif len(tokens) == 1:
        opcode = tokens[0]

    # Process label if it exists
    if label:
        symbol_table[label] = LC

    # Process each opcode
    if opcode == 'START':
        LC = int(operand1)
    elif opcode == 'DS':
        symbol_table[label] = LC
        LC += int(operand1)
    elif opcode == 'DC':
        symbol_table[label] = LC
        LC += 1
    elif opcode == 'EQU':
        if '+' in operand1:
            base, offset = operand1.split('+')
            symbol_table[label] = symbol_table[base] + int(offset)
        elif '-' in operand1:
            base, offset = operand1.split('-')
            symbol_table[label] = symbol_table[base] - int(offset)
    elif opcode == 'ORIGIN':
        if '+' in operand1:
            base, offset = operand1.split('+')
            LC = symbol_table[base] + int(offset)
        elif '-' in operand1:
            base, offset = operand1.split('-')
            LC = symbol_table[base] - int(offset)
    elif opcode == 'LTORG' or opcode == 'END':
        new_literals_added = False
        for lit in literal_table[pool_table[-1]:]:
            if lit['address'] is None:
                lit['address'] = LC
                LC += 1
                new_literals_added = True
        if new_literals_added:
            pool_table.append(len(literal_table))
    elif opcode in MOT and MOT[opcode] == 'IS':
        LC += 1
        if operand2 and operand2.startswith('='):
            literal_table.append({'literal': operand2, 'address': None})
    elif opcode == 'STOP':
        LC += 1

# Input Program (line by line)
input_program = [
    "START 100",
    "A DS 3",
    "L1 MOVEM AREG, B",
    "ADD AREG, C",
    "MOVER AREG, ='12'",
    "D EQU A+1",
    "LTORG",
    "L2 PRINT D",
    "ORIGIN A-1",
    "MOVER AREG, ='5'",
    "C DC '5'",
    "ORIGIN L2+1",
    "STOP",
    "B DC '19'",
    "END"
]

# Process each line of the program
for line in input_program:
    process_line(line)

# Function to display tables
def display_tables():
    print("\nSymbol Table")
    print("Symbol\tAddress")
    for symbol, address in symbol_table.items():
        print(f"{symbol}\t{address}")

    print("\nLiteral Table")
    print("Index\tLiteral\tAddress")
    for index, literal in enumerate(literal_table):
        lit_val = literal['literal']
        lit_addr = literal['address']
        print(f"{index}\t{lit_val}\t{lit_addr}")

    print("\nPool Table")
    print("Pool Number\tStart Index")
    for pool_number, start_index in enumerate(pool_table[:-1]):  # Exclude last entry if it's redundant
        print(f"{pool_number}\t\t{start_index}")

# Display the tables
display_tables()
