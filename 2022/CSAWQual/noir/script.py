#!/usr/bin/env python

from PIL import Image
import os
from tqdm import tqdm 

#frame work tqdm dung de lam dep loop =))

coord = (418,637)

def get_pixel_val(filename):
	im = Image.open(filename)
	pix = im.load()
	ans = pix[coord]
	im.close()
	return ans

arr = []
for i in tqdm(range(1, 1830)):
	idx = str(i)
	#format filename
	if (len(idx) < 3):
		idx = "0"*(3-len(idx)) + idx #try to print(idx) after this line if you don't know what it do
	val = get_pixel_val(f"/home/cheese00/ctf/csawctf/frames/out-{idx}.jpg")[0]
	if (val > 200):
		arr.append(str(1))
	else:
		arr.append(str(0))

cipher = "".join(arr)
cipher = cipher.replace("1111","-")
cipher = cipher.replace("11",".")
cipher = cipher.replace("000000"," ")
cipher = cipher.replace("00","")
cipher = cipher.replace("0","")
print(cipher)

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-', '_':'..--.-'}

def decrypt(message):
 
    # extra space added at the end to access the
    # last morse code
    message += ' '
 
    decipher = ''
    citext = ''
    for letter in message:
 
        # checks for space
        if (letter != ' '):
 
            # counter to keep track of space
            i = 0
 
            # storing morse code of a single character
            citext += letter
 
        # in case of space
        else:
            # if i = 1 that indicates a new character
            i += 1
 
            # if i = 2 that indicates a new word
            if i == 2 :
 
                 # adding space to separate words
                decipher += ' '
            else:
 
                # accessing the keys using their values (reverse of encryption)
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT
                .values()).index(citext)]
                citext = ''
 
    return decipher

result = decrypt(cipher)
print(result)