import time

def maximal_near_sidon_set_recursive(nums_so_far, sum_counts, exception_count, N):
    """recursively extend a near-sidon set
    nums_so_far: partially built set
    sum_counts: number of times each possible number could have been expressed as the sum of two members of the set
    exception_count: number of sums expressible more than one way in nums_so_far
    N: largest allowed set member"""
    
    biggest_found_size = len(nums_so_far)
    biggest_found = nums_so_far
    lowest = 1 if nums_so_far == [] else nums_so_far[-1] + 1
    for candidate_next in range(lowest, N + 1):
        #we want to check whether it's valid to add candidate_next.
        exception_count_delta = 0
        for val in nums_so_far:
            #if there was previously exactly one way to express val + candidate_next as a sum of two set members,
            #there is now a second way; we need to use the exception to the Sidon condition
            #note we don't need to check candidate_next*2 because all members of nums_so_far are less than candidate_next
            if sum_counts[val + candidate_next] == 1:
                exception_count_delta += 1
        #if there is more than one violation of the Sidon condition, this is an invalid extension
        if exception_count_delta + exception_count > 1:
            continue
        #maintain sum_counts
        for val in nums_so_far:
            sum_counts[val + candidate_next] += 1
        sum_counts[candidate_next*2] += 1
        
        #recurse
        child_biggest_found_size, child_biggest_found = maximal_near_sidon_set_recursive(nums_so_far + [candidate_next], sum_counts,
                                                                                         exception_count + exception_count_delta, N)
        if child_biggest_found_size > biggest_found_size:
            biggest_found_size = child_biggest_found_size
            biggest_found = child_biggest_found
            
        #undo the changes to sum_counts
        for val in nums_so_far:
            sum_counts[val + candidate_next] -= 1
        sum_counts[candidate_next*2] -= 1
        
    return biggest_found_size, biggest_found

def maximal_near_sidon_set(N):
    return maximal_near_sidon_set_recursive([], [0 for i in range(2*N + 1)], 0, N)


start_time = time.perf_counter()

for N in range(1, 50):
    size, max_set = maximal_near_sidon_set(N)
    elapsed = time.perf_counter() - start_time
    print(f"N={N:2d}: size={size:2d}, classes={max_set}")
    print(f"  elapsed: {elapsed:.3f}s")