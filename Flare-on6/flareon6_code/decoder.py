#!/usr/bin/python3

import argparse
from PIL import Image

class Decoder:

    def __init__(self,args): 
        self._im = Image.open(args.inf,'r')
        self._pix = self._im.load()
        self._size = self._im.size
        self._outfile = args.outf

    def _b(self,b,r):
        for i in range(0,r):
            b2 = (b & 128) / 128
            b = ((b * 2) & 255) + b2
        return int(b)

    def _e(self,b,k):
        b = ((b << 24) - ((b >> 8) << 32)) >> 24 # we have to cut off everything but the last byte
        k = ((k << 24) - ((k >> 8) << 32)) >> 24 # we have to cut off everything but the last byte
        return b ^ k

    def f(self,idx):
        num = 0
        num2 = 0
        result = 0
        array = [121,255,214,60,106,216,149,89,96,29,81,123,182,24,167,252,88,212,43,85,181,86,108,213,50,78,247,83,193,35,135,217,0,64,45,236,134,102,76,74,153,34,39,10,192,202,71,183,185,175,84,118,9,158,66,128,116,117,4,13,46,227,132,240,122,11,18,186,30,157,1,154,144,124,152,187,32,87,141,103,189,12,53,222,206,91,20,174,49,223,155,250,95,31,98,151,179,101,47,17,207,142,199,3,205,163,146,48,165,225,62,33,119,52,241,228,162,90,140,232,129,114,75,82,190,65,2,21,14,111,115,36,107,67,126,80,110,23,44,226,56,7,172,221,239,161,61,93,94,99,171,97,38,40,28,166,209,229,136,130,164,194,243,220,25,169,105,238,245,215,195,203,170,16,109,176,27,184,148,131,210,231,125,177,26,246,127,198,254,6,69,237,197,54,59,137,79,178,139,235,249,230,233,204,196,113,120,173,224,55,92,211,112,219,208,77,191,242,133,244,168,188,138,251,70,150,145,248,180,218,42,15,159,104,22,37,72,63,234,147,200,253,100,19,73,5,57,201,51,156,41,143,68,8,160,58]
        for i in range(0,idx+1):
            num += 1
            num %= 256
            num2 += array[num]
            num2 %= 256
            num3 = array[num]
            array[num] = array[num2]
            array[num2] = num3
            result = array[(array[num] + array[num2]) % 256]
        return result

    def _g(self,idx):
        b = (idx+1) * 309030853
        k = (idx+2) * 209897853
        return self._e(b,k)

    def _j(self,z):
        num = 0xc7c55664
        value = 34199
        num += value
        num += 4
        num += self._f(6)
        z = self._b(z,1)
        return self._e(z,num)
    
    def _a_reverser(self,b,r=7):
        return (b ^ r) - r

    def _d_reverser(self,b,r=3):  # r is hardcoded 3 since this is only run once. b is the encoded byte char. the original algorithm first set a variable equal to 128 if b was odd and 0 if it was even. then b was divided by 2, anded against 256(to truncate it), then the odd variable described above is added to it.
        for i in range(0,r):
            if (b >= 128):
                b -= 128
                b = b * 2
                b += 1
            else:
                b = b * 2
        return b

#    def _c_reverser(self,b,r=r):


    def _b_reverser(self,b,r=7): # r is hardcoded 7 since it is only called once. b is the encoded byte char. this first ands with 128(which simplifies the value into over 128 or 0) then divides it by 128. this act simplifies b2 into over 128 or under 128 (1 or 0). 
        for i in range(0,r):
            if ((b % 2) == 1):
                b -= 1
                b += 256
            b = b / 2
        return b

    def _e_reverser(self,b,k): # k is a return from f(), b is the input byte char. the simplest explanation of this logic is to check each bit at each position. if the bits are the same between b and k, set the bit at that position equal to 0. if they are different, set it equal to 1. this is a logical xor by definition so this whole function is an overly complex xor implementation.
        return b ^ k

    def _h_reverser(self,data): # since num=0, the input array will have to be decoded from the first byte to the last rather than reversed.
        decoded_array = []
        num = 0
        for i in range(0,len(data)):
            num2 = self._g(num)
            num += 1
            num4 = self._g(num)
            num += 1
            num3 = self._d_reverser(data[i],3)
            num3 = self._e_reverser(num3,num4)
            num3 = int(self._b_reverser(num3,7))
            num3 = self._e_reverser(num3,num2)
            decoded_array.append(num3)
        return(decoded_array)

    def _pixel_decoder(self,pixel):
        red = pixel[0]
        green = pixel[1]
        blue = pixel[2]

        first_three_bits = red & 0b00000111
        second_three_bits = (green << 3) & 0b00111000
        third_two_bits = (blue << 6) & 0b11000000

        return (first_three_bits + second_three_bits + third_two_bits)

    def run(self):
        decoded_pixel_array = []
        for x in range(0,self._size[0]):
            for y in range(0,self._size[1]):
                decoded_pixel_array.append(self._pixel_decoder(self._pix[x,y]))
        with open(self._outfile,"wb") as fd:
            answer = self._h_reverser(decoded_pixel_array)
            for value in answer:
                answer_bytes = bytes([value])
                fd.write(answer_bytes)




if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Process data.')
    parser.add_argument('-inf', help='input encoded bitmap')
    parser.add_argument('-outf', help='output file')
    args = parser.parse_args()
    
    if ( args.inf == None ):
        print("give file with -inf")
    else:
        decoder = Decoder(args)
        decoder.run()
