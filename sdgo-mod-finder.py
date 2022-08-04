# use texture number to find related .mod

import os
from pathlib import Path
import sys

sdgo_data_path = "G:\\Games\\SDGO_DEV\\data_dev\\"

def main(tex: str):
	os.chdir(sdgo_data_path)
	search = "Txrs\\" + tex + ".txr"
	print("searching related mod of '" + search + "'")
	search = search.encode("UTF-8").hex("|").replace("|", "00").upper() + "00"
	print("hex: '" + search + "'")
	file_list = os.listdir(sdgo_data_path + "mdrs")
	file_list.sort()
	related_mods = []
	for file_name in file_list:
		if (file_name.endswith(".mod")):
			f = open(sdgo_data_path + "mdrs/" + file_name, "rb")
			file_size = os.path.getsize(sdgo_data_path + "mdrs/" + file_name)
			fhex = f.read(file_size).hex().upper()
			found = fhex.find(search) > -1
			if found:
				related_mods.append(file_name)
	print(related_mods)
	return

main(sys.argv[1])
