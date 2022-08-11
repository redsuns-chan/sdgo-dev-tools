# sdgo-sfx-extractor
# author: RedSuns Chan
# rename file extension to .wav

import os
from pathlib import Path
import shutil
from toolconfig import sdgo_data_path

target_path = sdgo_data_path + "sdrs/decoded/"

def main():
	print("sdgo sfx extractor")
	Path(target_path).mkdir(parents=True, exist_ok=True)
	file_list = os.listdir(sdgo_data_path + "sdrs")
	for file_name in file_list:
		if file_name.endswith(".zsd"):
			file_name = file_name.replace(".zsd", "")
			print("converting " + file_name + ".zsd >>>>> " + file_name + ".wav")
			shutil.copyfile(sdgo_data_path + "sdrs/" + file_name + ".zsd", target_path + file_name + ".wav")

main()
