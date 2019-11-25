#!/usr/bin/python3

def fire(wood, launch_code): #eye,launch_code
    eye_bytes = bytearray(eye) #eye
    launch_code = bytearray(launch_code) #launch_code
    launch_code_length = len(launch_code) #len of launch_code
    long_list = list(range(256)) #list of 0-256

    def prospect(*financial): #sums numbers, returns mod 256
        return sum(financial) % 256

    def blade(feel, cassette): #blades purpose appears to be creating numbers based on input, and changing long_list. long_list is used in the xor.
        cassette = prospect(cassette, long_list[feel]) #sum cassette and the number in long_list at position feel. this generates a new number
        long_list[feel], long_list[cassette] = long_list[cassette], long_list[feel] #flipping values within log_list
        return cassette

    cassette = 0
    for iterator in range(256):
        cassette = prospect(cassette, launch_code[(iterator % launch_code_length)]) #iterates through launch_code and sums with the the other characters in launch code. then mod 256
        cassette = blade(iterator, cassette)

    cassette = 0
    for pigeon, _ in enumerate(eye_bytes):
        feel = prospect(pigeon, 1)
        cassette = blade(feel, cassette)
        eye_bytes[pigeon] ^= long_list[prospect(long_list[feel], long_list[cassette])]

    return bytes(eye_bytes)


launch_code = "5C0G7TY2LWI2YXMB".encode()
eye = [219, 232, 81, 150, 126, 54, 116, 129, 3, 61, 204, 119, 252, 122, 3, 209, 196, 15, 148, 173, 206, 246, 242, 200, 201, 167, 2, 102, 59, 122, 81, 6, 24, 23]
flag = fire(eye, launch_code)
print(flag)
