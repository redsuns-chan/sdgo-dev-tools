# hex to float convertor
# author: RedSuns Chan

from os import path, stat
import struct
import sys

print(sys.argv[0])

def main(file_path: str, big_endian: bool):
	f = open(file_path, "r")
	file_size = stat(file_path).st_size
	content = f.read(file_size)
	content = content.replace(" ", "")
	converted = []
	i = 0
	while (i <= file_size):
		n = content[i:i + 8]
		if len(n) == 8:
			le_bytes = bytearray.fromhex(n)
			if big_endian == False:
				le_bytes.reverse()
			converted.append(struct.unpack('!f', le_bytes)[0])
		i += 8
	f.close()
	print(converted)
	outf = open("./float.txt", "w")
	outf.write(str(converted))
	outf.close()
	


if len(sys.argv) > 1:
	main(sys.argv[1], sys.argv[2].lower() == "b")
else:
	main("./hex.txt", False)
