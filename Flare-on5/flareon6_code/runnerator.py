#!/usr/bin/python3


# our dictionary to compare values against
# python cuts off leading zeros on hex digits. so we have to do the same.
answer_dict = {
    "c5389090762f612" : ["d","s"," "],
    "f7846960fbcc7a93" : ["i","n"],
    "225b8f234851b1f5" : ["h","o","t"],
    "88f824561ea6e145" : ["e"," "],
    "e2c73500000" : ["Z"],
    "9b99d615f3c62a" : ["o","w"],
    "42e2d4e0000" : ["."],
    "ad2d8400000" : ["n","g"," "],
    "af26000000" : ["l","l"],
    "532a000000" : [" "],
    "81757200000" : ["t","h","e"],
    "6b42600000" : ["A","h",","],
    "740000000" : ["g"],
    "7f0000000" : ["r"],
    "4fa000000" : ["e"," "],
    "4f0000000" : ["e"],
    "b6d55cc50000" : ["a","c","e"],
    "532376300000" : [" ","y","o"],
    "767b000000" : ["i","n"],
    "a484600000" : [" ","b","l"],
    "4445000000" : ["n","o"],
    "a62000000" : [" ","H"],
    "827f000000" : ["u","r"],
    "4359000000" : ["i","s"],
    "5e424300000" : ["t","h","i"],
    "200000000" : [" "],
    "6c696b00000" : ["l","i","k"],
    "6f66000000" : ["o","f"],
    "660000000" : ["f"],
    "20696e00000" : [" ","i","n"]
}



# run for all of our files named {}_run.txt where {} is a number
for a in range(1,667):

    # generate empty list of the size of our answer so that we can write to index's instead of appending to the list.
    answer_list = []
    for i in range(0,0x45):
        answer_list.append("Z")
    
    
    with open('python_hex_dump/{}_run.txt'.format(a),'rb') as f:
        file_content = f.read()
        
    # loop through each answer in the answer block.
    for b in range(0,33):
        
        # generate offsets
        offset = b << 3
        offset = offset + b
        offset = offset << 5
        string_location = 0x0c
        length_location = 0x10
        answer_location = 0x20
        start_pos = file_content[offset+string_location]
        length = file_content[offset+length_location]
        
        # grab answer from offset in answer block.
        # since we are only checking the first 16 bytes, we have a duplicate key in the
        # dictionary. so we get around that by filling it with a trigger character and
        # checking the answer block for more information on what string it is.
        answer = ''.join(format(file_content[offset+answer_location+x],'x') for x in range(0,8))
        compare_answer = answer_dict[answer]
        if compare_answer[0] == "Z":
            if file_content[offset+answer_location+8] == 160:
                compare_answer = [" ","w"]
            else:
                compare_answer = [" "]
        
        # build our answer
        for c in range(0,len(compare_answer)):
            answer_list[start_pos+c] = compare_answer[c]

    print(''.join(answer_list))

