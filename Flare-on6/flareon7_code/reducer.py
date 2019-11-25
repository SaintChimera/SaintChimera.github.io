#!/usr/bin/python3
b_better = []
b_better.append([2,3,4,8,11,14]) # 0
b_better.append([0,1,8,11,13,14]) # 1
b_better.append([0,1,2,4,5,8,9,10,13,14,15]) # 2
b_better.append([5,6,8,9,10,12,15]) # 3
b_better.append([1,6,7,8,12,13,14,15]) # 4
b_better.append([0,4,7,8,9,10,12,13,14,15]) # 5
b_better.append([1,3,7,9,10,11,12,13,15]) # 6
b_better.append([0,1,2,3,4,8,10,11,14]) # 7
b_better.append([1,2,3,5,9,10,11,12]) # 8
b_better.append([6,7,8,10,11,12,15]) # 9
b_better.append([0,3,4,7,8,10,11,12,13,14,15]) # 10
b_better.append([0,2,4,6,13]) # 11
b_better.append([0,3,6,7,10,12,15]) # 12
b_better.append([2,3,4,5,6,7,11,12,13,14]) # 13
b_better.append([1,2,3,5,7,11,13,14,15]) # 14
b_better.append([1,3,5,9,10,11,13,15]) # 15

#h = [126, 24, 139, 90, 75, 233, 109, 223, 204, 203, 163, 13, 0, 40, 75, 114] # wrong h
h = [115, 29, 32, 68, 106, 108, 89, 76, 21, 71, 78, 51, 75, 1, 55, 102] 
answer = [0] * 16

def compare(compare_lists): # compare_lists is a list of lists
    new_list = []
    flip_flag_list = [0] * 16
    for a in compare_lists:
        for c in a:
            new_list.append(c)
    for d in new_list: # maybe a flip flag list, where everytime we find a certain number, we flip the flag for that number
        flip_flag_list[d] = (flip_flag_list[d] + 1) % 2
    return flip_flag_list

def flip_flag_fixer(flip_flag_list,solved_master_list): # the point here is that, when an extra flag in flip_flag_list is flipped, it means it will impede the solving. the below logic changes the list to remove ones that we've solved for, and returns a list of the changed ones.
    flip_flag_list_fixed = flip_flag_list
    fflf_changed = []
    for i in range(0,16):
        if ( flip_flag_list[i] == 1 and solved_master_list[i] == 1 ):
            flip_flag_list_fixed[i] = 0
            fflf_changed.append(i)
    return flip_flag_list_fixed,fflf_changed


def main(): # this needs to iterate through b and create a list of lists to be passed to compare. the caveat is that it has to be able to generate lists of up to the full size of b, iterating through every possible combination.
    counter = 0
    solved_master_list = [0] * 16 # gets compared flip_flag_list to keep track of whats already been solved, and what can be solved because of that.
    while counter <= 0xffff: # this only needs to run for 16 bits, since we use each bit as a flag.
        send_list = []
        send_list_positions = []
        for add in range(0,16):
            if ( counter >> add & 1 == 1 ):
                send_list.append(b_better[add])
                send_list_positions.append(add)
        counter += 1
        flip_flag_list = compare(send_list)
        flip_counter = 0
        flip_flag_list_fixed,fflf_changed = flip_flag_fixer(flip_flag_list,solved_master_list) #and the unknowns and the knows to discover the unknowns with the knowns. we only use this for testing if a variable can be solved for.
#        print("counter: ",counter," fflf: ",flip_flag_list_fixed," ffl: ",flip_flag_list," sml: ",solved_master_list," fflf_changed: ",fflf_changed)
        for number in flip_flag_list_fixed: # iterate through the flags and increment a number indicating how many are flipped
            if ( number == 1 ):
                flip_counter += 1
        if flip_counter == 1: # a single flag flipped indicates a solvable combination
            final_char = 0
            for i in send_list_positions:
                final_char = final_char ^ h[i]
            if fflf_changed:
                for i in fflf_changed:
                    final_char = final_char ^ answer[i]
            for i in range(0,16):   # set the final character at the position that it exists at
                if (flip_flag_list_fixed[i] == 1):
                    solved_master_list[i] = 1
                    answer[i] = final_char
                    counter = 0 # if we discovered a letter, then there may be solvable operations that we have already skipped.

    print(''.join(chr(x) for x in answer))

main()

