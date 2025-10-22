import time

def maximal_near_sidon_set_recursive(bitfield, sums_once, exception_sums, N, last_added, best_size_ref, best_bitfield_ref):
    """
    bitfield: integer whose 1 bits represent the set members chosen so far
    sums_once: integer whose 1 bits represent numbers already expressible as a pair sum in exactly one way
    exception_sums: integer which is 0 if we have not yet used the exception sum and 2**k if k is the exception sum
    N: problem size
    last_added: start index for candidate_next loop
    best_size_ref: passing by reference the best size seen
    best_bitfield_ref: passing by reference a bitfield representing the best subset seen
    """
    current_size = bitfield.bit_count()

    # New best
    if current_size > best_size_ref[0]:
        best_size_ref[0] = current_size
        best_bitfield_ref[0] = bitfield

    # Prune if not enough potential numbers remain
    if current_size + (N - last_added) <= best_size_ref[0]:
        return current_size, []

    # Iterate over potential new numbers
    for candidate_next in range(last_added + 1, N + 1):
        # Prune if not enough potential numbers remain
        if current_size + (N - candidate_next + 1) <= best_size_ref[0]:
            break

        # Compute sums that candidate_next would add (including candidate_next*2)
        new_sums = bitfield << candidate_next
        new_sums |= (1 << (candidate_next * 2))

        # Detect Sidon condition violations and check validity
        collisions_with_once = sums_once & new_sums
        new_exceptions = collisions_with_once & ~exception_sums

        if new_exceptions != 0:
            exception_count_delta = new_exceptions.bit_count()
            if exception_count_delta > 1 or (exception_sums > 0 and exception_count_delta > 0):
                continue

        # Maintain fields and recurse
        new_sums_once = (sums_once | new_sums) & ~collisions_with_once
        new_exception_sums = exception_sums | collisions_with_once
        
        new_bitfield = bitfield | (1 << candidate_next)
        maximal_near_sidon_set_recursive(
            new_bitfield, new_sums_once, new_exception_sums,
            N, candidate_next, best_size_ref, best_bitfield_ref
        )
    
    return

def maximal_near_sidon_set(N):
    best_size_ref = [0]
    best_bitfield_ref = [0]
    
    maximal_near_sidon_set_recursive(0, 0, 0, N, 0, best_size_ref, best_bitfield_ref)
    best_size = best_size_ref[0]
    best_bitfield = best_bitfield_ref[0]
    best_seq = []
    for i in range(1, N + 1):
        if best_bitfield & (1 << i):
            best_seq.append(i)
    return (best_size, best_seq)

start_time = time.perf_counter()


for N in range(1, 70):
    size, max_set = maximal_near_sidon_set(N)
    elapsed = time.perf_counter() - start_time
    print(f"N={N:2d}: size={size:2d}, classes={max_set}")
    
    print(f"  elapsed: {elapsed:.3f}s")