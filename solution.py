assignments = []

def cross(A, B):
    return [a+b for a in A for b in B]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
boxes= ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
     'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9',
     'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
     'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9',
     'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9',
     'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
     'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9',
     'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9',
     'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9']
    
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
    
#grid setup
def display(values):
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def grid_values(grid):
    return dict(zip(boxes, grid))
    
def grid_values(grid):
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

#Eliminate
def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

#Only Choice
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

#Reduce
def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
    if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

#Search
def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False 
    if all(len(values[s]) == 1 for s in boxes): 
        return values 
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

#Identify Nake Twins
def naked_twins(self):
    for unit in self.all_units:
        candidates = [(box, self.values[box]) for box in unit if len(self.values[box]) == 2]
        if len(candidates) >= 2:
            sorted_candidates = sorted(candidates, key=itemgetter(1))
            paired_candidates = groupby(sorted_candidates, key=itemgetter(1))
            for digits, candidates in paired_candidates:
                boxes = [candidate[0] for candidate in candidates]
                if len(boxes) == 2:
                    for box in unit:
                        if box not in boxes:
                            for digit  in digits:
                                if digit in self.values[box] and len(self.values[box]) > 1:
                                    self.assign_value(box, self.values[box].replace(digit, ''))

# Eliminate the naked twins as possibilities for their peers
def reduce_puzzle(values):
    values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

#Diagonal
def __init__(self, is_diag_sudoku=False, from_string=None, from_dict=None):
    self.boxes = self.cross(rows, cols)
    self.values = self.grid_values(from_string, from_dict)
    self.row_units = [self.cross(rows, cols) for col in rows]
    self.col_units = [self.cross(rows, col) for col in cols]
    self.square_units = self.row_units + self.col_units + self.square_units
    if is_diag_sudoku==True:
        self.diag_units = [[y+x for y,x in zip(rows, cols)], [y+x for y,x in zip(rows, cols[::-1])]]
        self.all_units += self.diag_units
    self.units = dict((box, [unit for unit in self.all_units if box in unit]) for box in self.boxes)
    self.peers = dict((box, set(sum(self.units[box], [])) - set([box])) for box in self.boxes)


    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
