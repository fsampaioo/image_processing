# IMAGE PROCESSING

- Frederico Sampaio				8922100
- Julia Minetto Macias			8937329

**README**

1. Generating index
Considering all the files extracted in a folder, the first step is generate indexes vectors of all the images of the database through some method. Follow the steps:
 - Create a folder inside this workspace folder which will contain all the images (the database). In this case, we already have this folder with the images, called database. 
 - To execute, follow the command:
 
	python index.py --images <image database directory path> --method <fourier or gch or lch> --mask <3 or 7>.
	
	- The flag --images specifies the directory of the images database.
	- The flag --method specifies the method to be used to compare.
	- The flag --mask is optional, used in case of Fourier. The default is 7.
	 
Exemple: python index.py --images images/ --method lch --mask 3

 - Now there is a .csv file inside the indexes folder.

2. Specifying query

Once generated the indexes, we will execute the desired query, that is, compare an input image to all images of the database. Follow the steps:
 -To execute, follow the command: 
 
	python main.py --images <image database directory path> -q <query image path> -n <number of similar images> --method <fourier or gch or lch> --mask <3 or 7> -d <chi2 or manhattan or euclidian>
 
	-The flag --images specifies the directory of the images database.
	-The flag -q or --query specifies the image to be compared.
	-The flag -n or --limit specifies how many output images you want.
	-The flag --method or -m specifies the method to be used to compare.
	-The flag --mask is optional, used in case of Fourier. The default is 7.
	-The flag -d or --distance specifies the distance metric comparison.
	
Ps: The arguments information can be found using the help command, for example:
		python main.py -h

