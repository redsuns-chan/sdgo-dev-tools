# SD Gundam Online Mod File Data Extractor
# author: RedSuns Chan

import sys
import codecs
import json

def extract_header(f):
    read_zoa = 0
    header_pointer = 0
    max_header_length = 24
    while read_zoa == 0 or header_pointer >= max_header_length:
        try:
            byte = f.read(4)
            byte = byte.hex()
            if (byte == "5a4f4100"): # 'ZOA'
                read_zoa = 1
            header_pointer += 4
        except UnicodeDecodeError:
            print("Error while reading file bytes")
    section1 = f.read(1)
    texture_count = int(f.read(1).hex(), 16)
    f.read(2)
    f.read(1)
    object_count = int(f.read(1).hex(), 16)
    f.read(2)
    section3 = f.read(4)
    section4 = f.read(4)
    return {
        "texture_count": texture_count,
        "bone_count": object_count
    }

def extract_bone_names(f, bone_count):
    section_length = 256 // 2
    byte = ""
    bones = []
    for i in range(bone_count):
        bone_str = ""
        for x in range(section_length):
            byte_hex = f.read(2).hex()
            try:
                if byte_hex == "0000":
                    bone_str += " "
                else:
                    letter = byte_hex[2:4]
                    letter_bytes = bytes(letter, encoding="utf-8")
                    bone_str += str(codecs.decode(letter_bytes, "hex"), "utf-8")
            except UnicodeDecodeError:
                bone_str += ""
            
        bones.append(bone_str.strip())
        bone_str = ""
    return bones

def main(index):
    try:
        f = open('./mdrs/' + index + '.mod', 'rb')
        try:
            file_info = extract_header(f)
            file_info["bone_names"] = extract_bone_names(f, file_info["bone_count"])
            
            f.close()
            #print(json.dumps(file_info))
        except FileExistsError:
            print("unable to close file")
    except FileNotFoundError:
        print('model file not exists')

main(sys.argv[1])
