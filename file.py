import os
foldername=raw_input("Give foldername: ")
for file in os.listdir("%s/"%(foldername)):
	print file