# SD Gundam Online Texture File Extractor
# author: RedSuns Chan
import os
import pathlib

sdgo_data_path = "G:/Games/SDGO_DEV/data_dev/"
target_path = sdgo_data_path + "txrs/decoded/"

def extract_texture(file_name):
	f = open(sdgo_data_path + "txrs/" + file_name, "rb")
	file_size = os.path.getsize(sdgo_data_path + "txrs/" + file_name)
	found_type = ""
	fhex = f.read(file_size).hex().upper()
	
	# remove zoa header
	if fhex.startswith("5A4F415445583100"):
		fhex = fhex[24:]
	
	# detect type
	if fhex.startswith("424D"):
		found_type = "bmp"
	elif fhex.startswith("89504E47"):
		found_type = "png"
	elif fhex.endswith("54525545564953494F4E2D5846494C452E00"):
		found_type = "tga"
	elif fhex.startswith("44445320"): # if cannot find any recognized header, assume the file is dds, may need to improve this logic
		found_type = "dds"
	else:
		found_type = "tga"
	new_file = open(target_path + file_name.replace(".txr", "." + found_type), "wb")
	new_file.write(bytes.fromhex(fhex))
	f.close()
	new_file.close()
	return found_type

def main():
	print("sdgo texture extractor")
	os.chdir(sdgo_data_path)
	pathlib.Path(target_path).mkdir(parents=True, exist_ok=True)
	file_list = os.listdir(sdgo_data_path + "txrs")
	txr_count = 0
	tga_count = 0
	png_count = 0
	bmp_count = 0
	dds_count = 0
	unknown_count = 0
	file_list.sort()
	for file_name in file_list:
		if (file_name.endswith(".txr")):
			txr_count += 1
			print("processing " + file_name)
			file_type = extract_texture(file_name)
			if file_type == "tga":
				tga_count += 1
			elif file_type == "png":
				png_count += 1
			elif file_type == "bmp":
				bmp_count += 1
			elif file_type == "dds":
				dds_count += 1
			else:
				unknown_count += 1
	print("converted textures: " + str(txr_count))
	print("converted tga: " + str(tga_count))
	print("converted png: " + str(png_count))
	print("converted bmp: " + str(bmp_count))
	print("converted dds: " + str(dds_count))
	print("unknown files: " + str(unknown_count))

main()
