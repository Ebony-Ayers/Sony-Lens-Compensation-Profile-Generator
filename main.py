import struct

def int8ToBytes(ints, n):
	if n == 1:
		return struct.pack("B", ints)
	else:
		return struct.pack("B"*n, *ints)

def bytesToint8(bytes, n):
	if n == 1:
		return struct.unpack("B", bytes)
	else:
		return struct.unpack("B"*n, bytes)

def int16ToBytes(ints, n):
	if n == 1:
		return struct.pack(">h", ints)
	else:
		return struct.pack(">h"*n, *ints)

def bytesToint16(bytes, n):
	if n == 1:
		return struct.unpack(">h", bytes)
	else:
		return struct.unpack(">h"*n, bytes)

def main():
	#the first 8 bytes are the same ever time
	initialBytes = [0x01, 0x00, 0x01, 0x00, 0x01, 0xEA, 0x00]

	while True:
		#input validation
		while True:
			while True:
				lenseName = str(input("Please enter a name for the lense: "))
				if lenseName == "":
					print("Please provide a name for the lense")
					continue
				if len(lenseName) > 64:
					print("Lense name cannot be longer than 64 letters. Please enter it again")
				else:
					break

			while True:
				focalLength = 0
				
				try:
					focalLength = input("Please enter the focal length of the lense: ")
					if focalLength == "":
						focalLength = 0
					else:
						focalLength = int(focalLength)
				except:
					print("Invalid input. Please enter an integer between 1 and 9999")
					continue
				
				if focalLength > 9999 or focalLength < 1:
					print("Invalid input. Please enter an integer between 1 and 9999")
				else:
					break
				
			print()
			print("The following will be created")
			print("name:", lenseName)
			print("focal length:", focalLength)
			userConfirmation = input("Do you wish to save them [Y/n]: ")
			print()
			if userConfirmation == "" or userConfirmation == "Y" or userConfirmation == "y":
				break
			
		while True:
			fileName = input("Enter the name of the file you wish to create: ")
			if fileName == "":
				print("File name most contain at least one letter")
			else:
				break

		with open(fileName, 'wb') as outputFile:
			#write out the first 8 bytes which are constant
			outputFile.write(int8ToBytes(initialBytes, len(initialBytes)))
			#the ninth byte is the length of the name as a 8bit integer
			outputFile.write(int8ToBytes(len(lenseName), 1))
			#write out the string with out a null terminating character
			outputFile.write(lenseName.encode('utf-8'))
			
			#the next important peice of data is at byte 392 so write the required amount of zeros to fill the gap
			numBlankBytes = 392 - (len(initialBytes) + 1) - len(lenseName)
			for i in range(numBlankBytes):
				outputFile.write(int8ToBytes(0x00, 1))
			
			#the focal length is always preceded by a one
			outputFile.write(int8ToBytes(0x01, 1))
			#write the focal length as a big endian two byte integer
			outputFile.write(int16ToBytes(focalLength, 1))
			
			#the file must be 496 bytes long so fill in the remaining data with zeros
			numBlankBytes = 496 - (len(initialBytes) + 1) - len(lenseName) - numBlankBytes - 3
			for i in range(numBlankBytes):
				outputFile.write(int8ToBytes(0x00, 1))
		
		print()
		userAction = input("Press enter to finish of \'r\' followed by enter to create another lense file: ")
		if userAction == "": break
		else:
			print()
			print("================================================")
			print()

if __name__ == "__main__":
	main()
