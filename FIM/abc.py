import hashlib
import os
import time

def calculate_file_hash(filepath):
	h = hashlib.sha512()
	with open(filepath,'rb') as file:
		chunk = 0
		while chunk != b'':
			chunk = file.read(1024)
			h.update(chunk)
	return h.hexdigest()


def findabsolutepath(directory):
	for dirpath,_,filenames in os.walk(directory):
		for f in filenames:
			yield os.path.abspath(os.path.join(dirpath,f))


def homepage():
	print("\n***What would you like to do?***")
	print("Enter 'A' to Collect a new Baseline.")
	print("Enter 'B' to Begin monitoring files wiht saved Baseline.\n")
	print("Enter any other key to exit.")
	return input("Please enter:")


def main():
	decision = homepage()
	# Calculate Hash from the target files and store in baseline.txt
	if decision.upper() == 'A':

		# Collect all files in the target folder
		filepaths = findabsolutepath("files")

		# For each file, calculate the hash, and write to baseline.txt
		with open("baseline.txt", "w") as file:
			for f in filepaths:
				file.write(f"{f}|{calculate_file_hash(f)}\n")
		print("New Baseline collected!\n")
		main()

	elif decision.upper() == 'B':

		# Load file and hash from baseline.txt and store them in a dictionary
		hashpathdictionary = {}
		with open("baseline.txt", "r") as file:
			lines = file.readlines()
			for i in lines:
				line = i.split("|", 1)
				hashpathdictionary[line[0]] = line[1][:-1]

		# Begin monitoring files with saved Baseline 
		print("Checking files...")
		while True:
			filepaths = findabsolutepath("files")
			time.sleep(1)				
			for i in filepaths:
				file_hash = calculate_file_hash(i)
				# Notify if new file created
				if i not in hashpathdictionary.keys():
					print(f"{i} created!")	
				# Notify if a file changed
				elif hashpathdictionary[i] != file_hash:
					print(f"{i} has changed!")
	
			filepaths = findabsolutepath("files")
			for key in hashpathdictionary.keys():
				if key not in filepaths:
					print(f"{key} has been deleted!") 	

	else: 
		print("\nExitting...")
		exit()


if __name__ == '__main__':
	main()