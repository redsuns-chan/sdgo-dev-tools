
import os
from pathlib import Path
import shutil

sdgo_data_path = "D:/Project/SDGO/data/"
target_path = sdgo_data_path + "scp/decoded/"

command = "java -jar ./unlua.jar \"" + sdgo_data_path + "scp/{{filename}}.scp" + "\" > \"" + target_path + "{{filename}}.scp\""

def main():
	print("sdgo script extractor")
	Path(target_path).mkdir(parents=True, exist_ok=True)
	file_list = os.listdir(sdgo_data_path + "scp")
	for file_name in file_list:
		if file_name.endswith(".scp"):
			print("decompiling script " + file_name)
			file_name = file_name.replace(".scp", "")
			os.system("cmd /c " + command.replace("{{filename}}", file_name))
			if os.stat(target_path + file_name + ".scp").st_size == 0:
				os.remove(target_path + file_name + ".scp")
				shutil.copyfile(sdgo_data_path + "scp/" + file_name + ".scp", target_path + file_name + ".lua")

main()
