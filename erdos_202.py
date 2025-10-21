import math
import time
from typing import List, Tuple, Set

def dfs(N, classes_so_far, sieve, gcd_cache, best_cardinality=0):
    """
    N: problem size, maximum modulus
    classes_so_far: current DFS state. list of tuples (modulus, residue)
    sieve: bitmask tracking which moduli are still candidates to be appended
    gcd_cache: precomputation of all gcds we might need
    best_so_far: tracking optimal result we've seen for pruning
    """
    current_depth = len(classes_so_far)
    best_cardinality = max(best_cardinality, current_depth)
    best_set = classes_so_far
    
    lower = 1 if not classes_so_far else classes_so_far[-1][0] + 1

    # Loop over possible new residue classes
    for new_n in range(lower, N + 1):

        # Prune congruence classes that are coprime with a congruence class in classes_so_far
        if not (sieve >> new_n) & 1:
            continue
        
        # Simple pruning: are there enough moduli left that we could beat the current best?
        remaining = (sieve >> (new_n + 1)).bit_count()
        if remaining + current_depth + 1 <= best_cardinality:
            continue
        
        for new_a in range(new_n):
            # Check disjointness of a mod n with previously included congruence classes
            disjoint = True
            for ni, ai in classes_so_far:
                if (ai - new_a) % gcd_cache[min(ni, new_n)][max(ni, new_n)] == 0:
                    disjoint = False
                    break
            
            if not disjoint:
                continue
            
            # Update sieve: keep only moduli that are not coprime to new_n
            new_sieve = sieve & ~(1 << new_n)
            for m in range(new_n + 1, N + 1):
                if gcd_cache[new_n][m] == 1:
                    new_sieve &= ~(1 << m)
            
            # Recurse
            child_best_cardinality, child_best_set = dfs(
                N, classes_so_far + [(new_n, new_a)], new_sieve, gcd_cache,
                best_cardinality
            )
            
            if child_best_cardinality > best_cardinality:
                best_set = child_best_set
                best_cardinality = child_best_cardinality
    
    return best_cardinality, best_set

def largest_congruence_class_set(N):
    # Precompute all GCDs
    gcd_cache = [[0] * (N + 1) for _ in range(N + 1)]
    for i in range(1, N + 1):
        for j in range(i, N + 1):
            gcd_cache[i][j] = math.gcd(i, j)

    #maintain a sieve of potentially valid new moduli
    full_sieve = (1 << (N + 1)) - 1
    size, solution = dfs(N, [], full_sieve, gcd_cache)
    return size, solution
    
start_time = time.perf_counter()

for N in range(1, 50):
    size, classes = largest_congruence_class_set(N)
    elapsed = time.perf_counter() - start_time
    print(f"N={N:2d}: size={size:2d}, classes={classes}")
    print(f"  elapsed: {elapsed:.3f}s")