# SD Gundam Online Mod File Data Extractor
# author: RedSuns Chan

import struct
import sys
import codecs

sdgo_data_path = "D:/Project/SDGO/data/"

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
	unknown_num_1 = f.read(1)
	texture_count = int(reverse_hex(f.read(4).hex()), 16)
	object_count = int(reverse_hex(f.read(4).hex()), 16)
	f.read(4)
	mesh_count = int(reverse_hex(f.read(4).hex()), 16)
	return {
		"texture_count": texture_count,
		"bone_count": object_count,
		"mesh_count": mesh_count
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
					letter = byte_hex[0:2]
					letter_bytes = bytes(letter, encoding="utf-8")
					bone_str += str(codecs.decode(letter_bytes, "hex"), "utf-8")
			except UnicodeDecodeError:
				bone_str += ""
			
		bones.append(bone_str.strip())
		bone_str = ""
	return bones

def extract_materials(f, texture_count):
	float_size = 68
	texture_path_size = 512
	materials = []
	for i in range(texture_count):
		floats_bytes = f.read(float_size).hex()
		texture_path = ""
		texture_path_bytes = f.read(texture_path_size).hex()
		reversed_texture_path_bytes = ""
		x = 0
		while x < 512:
			letter_byte = texture_path_bytes[0 + x : 2 + x]
			if (letter_byte != "00"):
				texture_path += str(codecs.decode(letter_byte, "hex"), "UTF-8")
			x += 2
		material = {}
		material["floats"] = floats_bytes
		material["texture"] = texture_path.replace('\\', "/")
		materials.append(material)

	return materials

def read_next_float(f):
	return struct.unpack('!f', reverse_hex(f.read(4).hex()))[0]

def reverse_hex(hex: str):
	output = ""
	i = len(hex) - 1
	while i - 1 >= 0:
		output += hex[i - 1] + hex[i]
		i -= 2
	return output

def main(index):
	try:
		f = open(sdgo_data_path + 'mdrs/' + index + '.mod', 'rb')
		try:
			file_info = extract_header(f)
			file_info["bone_names"] = extract_bone_names(f, file_info["bone_count"])
			file_info["materials"] = extract_materials(f, file_info["texture_count"])
			f.close()
			print(file_info)
		except FileExistsError:
			print("unable to close file")
	except FileNotFoundError:
		print('model file not exists')

main(sys.argv[1])
