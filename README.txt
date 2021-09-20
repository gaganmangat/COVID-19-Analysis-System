TECHNOLOGIES USED:
Python

PYTHON PACKAGES USED:
Pandas
Numpy
Tex

SETUP TO RUN:
1. Download zip file to your local machine
2. Extract the zip file
3. Open terminal/cmd promt
4. Goto that Path

Example-
	cd ~/Desktop/20111019-asign1

STEPS TO RUN:
1. Create a new virtual environment in that directory
	python3.6 -m pip install virtualenv
	virtualenv venv -p python3.6

2. Activate the virtual environment using the following command
	source venv/bin/activate

3. Install all dependencies using the following command
	pip install -r requirements.txt

4. Then navigate to /assign1
	cd assign1

5. Run the required scripts using the following command	
	./<name-of-the-script>.sh
Example-		
	./case-generator.sh

If permission is denied, run the following command before running the script.
	chmod +x <name-of-the-script>.sh


STEPS TO RUN TEX FILE:

1. The tex file report.tex can be run using the following command:
	pdflatex report.tex
It will produce the output file report.pdf in the same directory.
