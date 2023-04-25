import time
import argparse 
from itertools import combinations
from collections import defaultdict, Counter

# TODO measure efficiency & improve
# TODO use hash table to improve
# TODO error for invalid CLI args

max_print = 600
answer = 'No solution available'
VERBOSE = False
TRY_COUNT = 0
ALL_COMBOS = defaultdict(list)


def conv(int_list: list[int]):
    return [(i, str(i)) for i in int_list]


def check(n, p):
    global ALL_COMBOS
    global TRY_COUNT
    global answer
    ALL_COMBOS[n].append(p) 
    TRY_COUNT = TRY_COUNT+1
    if n == TARGET:
        answer = p
        if GREEDY:
            summary()

            
def summary(max = max_print):

    elapsed_time = time.process_time() - TIME_ZERO

    if VERBOSE:
        global ALL_COMBOS
        all = {k:len(v) for k,v in ALL_COMBOS.items()}
        path_counts = sorted(all.items(), key=lambda x:x[0])
        for int, n in path_counts:
            if int>max:
                break
            print(f'{int:5}{n:6}')

    print(f'Solution for {TARGET} is {answer} found after {TRY_COUNT} tries and {elapsed_time:.4f} seconds')
    quit()


def explore (old, new):
    results = []
    old_n, old_path = old
    new_n, new_path = new
    # ADD
    comb_n = old_n+new_n
    comb_path = f'({old_path}+{new_path})'
    res_a = (comb_n, comb_path)
    check(comb_n,comb_path)
    results.append(res_a)
    # SUBTRACT
    if old_n > new_n:
        comb_n = old_n-new_n
        comb_path = f'({old_path}-{new_path})'
        res_s = (comb_n, comb_path)
        check(comb_n,comb_path) 
        results.append(res_s)
    elif new_n > old_n:
        comb_n = new_n-old_n
        comb_path = f'({new_path}-{old_path})'
        res_s = (comb_n, comb_path)
        check(comb_n,comb_path) 
        results.append(res_s)
    else:
        pass
    # MULTIPLY
    comb_n, comb_path = old_n*new_n, f'({old_path}*{new_path})'
    res_m = (comb_n, comb_path)
    check(comb_n,comb_path)
    results.append(res_m)
    # DIVIDE
    if old_n >= new_n and old_n % new_n == 0:
        comb_n, comb_path = old_n//new_n, f'({old_path}//{new_path})'
        res_d = (comb_n, comb_path)
        check(comb_n,comb_path)
        results.append(res_d)
    elif old_n < new_n and new_n % old_n == 0:
        comb_n, comb_path = new_n//old_n, f'({new_path}//{old_path})'
        res_d = (comb_n, comb_path)
        check(comb_n,comb_path)
        results.append(res_d)
    else:
        pass
    return results


def solve (path_list: list[tuple[int, str]]):
    size = len(path_list)
    results_this_level : list[list[tuple[int, str]]] = [] 
    if size == 2:
        return explore(path_list[0], path_list[1])
    # FOR >=3
    pair_index_options = combinations(range(size), 2)
    for p in pair_index_options:
        modified_list = path_list.copy()
        next = modified_list.pop(p[1])
        first = modified_list.pop(p[0])
        operation_results = explore(first, next)
        for r in operation_results:
            new_branch = modified_list.copy()
            new_branch.append(r)
            results_this_level.append(new_branch)
    #print(f'for level {size} there are {len(results_this_level)} possibilities to search')
    #print(results_this_level)
    # NEXT LEVEL DOWN
    for result_path_list in results_this_level:
        #print(f'trying {result_path_list}')
        solve(result_path_list)
    return


if __name__ == "__main__":
    TIME_ZERO = time.process_time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', '-t', type=int, default=None, help="The target integer")
    parser.add_argument('--operands', '-o', nargs='+', type=int, help='The set of numbers which may be used to solve the puzzle')
    parser.add_argument('--greedy', '-g', action="store_true", help='If selected, terminates on the first valid solution. Otherwise, all combinations are explored.')
    args = parser.parse_args()
    operands = args.operands 
    TARGET = args.target
    GREEDY = args.greedy
    initial = conv(operands)
    solve(initial)
    summary()


#start = [5,7,9,11,13,23]
#targ = 463

# start = [3,5,9,19,20,25] 
# targ = 462 #25139 tries 

#class pedigree_number

# class PedigreeInt:
#     def __init__(self, value: int):
#         self.value = value
#         self.pedigree = str(value)

# start_set = [3,13,19,20,23,25]
# [4,5,7,9,11,20] 218
# [3,5,9,20,23,25] 388 #1178064 tries 
#    #[3,5,9,19,20,25] 462
#   [5,7,9,11,13,23] 463