SimHP: A patients phenotype simulation tool

I. Introduction
    SimHP is a tool to generate patient cases with their phenotypes mapping to Human Phenotype Ontology(HPO). Users can set parameters by their own. The generated data can applicate on disease-assisted diagnosis algorithm. The latest version of SimHP can be downloaded here. Please download the file "SimHP.tar.gz".

II. System requirements
    Python 2.7 or 3.6
    Linux operation system

III. Files
    simulator.py			main script
    hp.obo				HPO obo file
    phenotype_annotation.tab	        phenotype annotation table file
    example_input.txt			input file

IV. Install SimHP
    tar zxvf SimHP.tar.gz

V. Run patient simulation
     Mandatory parameter:

	-o	Output file.

     Options:
				
	-i	One OMIM number or an input file (a list of OMIM numbers, separated by "\n").
	-b	HPO OBO file downloaded from HPO website. 
                Default: hp.obo
	-t	Phenotype_annotation.tab file downloaded from HPO website.
                Default: phenotype_annotation.tab
	-r	The numbers of random diseases.
                Default: 5
	-c	Patient numbers per disease. 
                Default: 20
	-l	The number range of patients HPs. You can also set a specific number such us 10.
                Default: [4,20]
	-m	Percent of query HP terms replaced by one of its ancestor, greater than or equal to 0 and less than 1. 
                Default: 0.2
	-n	Percent of unrelated terms randomly added to query HP terms, greater than or equal to 0 and less than 1. 
		Default: 0.15
	-a	Annotations of HP in output file. Set this parameter if you want to annotate.
	-f	Using frequency information. Set this parameter if you want to use frequency.
	-v  cuf-off frequency value to filter HP term and you need to set -f before use it.
	-h	Help.

    1. Generate a simulated dataset on random disease

      1.1. All default (5 diseases with 20 patients each):
        python simulator.py -o output.txt

      1.2. 100 random diseases with 10 patients each and annotations on output file:
        python simulator.py -o output.txt -r 100 -c 10 -a


    2. Generate a simulated dataset on one disease

      2.1. Prader-Willi syndrome, OMIM:176270:
        python simulator.py -l [2,15] -m 0.2 -n 0.1 -o out.txt -i OMIM:176270 -a
        python simulator.py -l [2,15] -m 0.2 -n 0.1 -o out.txt -i omim:176270 -a
        python simulator.py -l [2,15] -m 0.2 -n 0.1 -o out.txt -i 176270 -a


    3. Generate a simulated dataset on some specific diseases

      3.1. The diseases are written in the file example_input.txt
        python simulator.py -o output.txt -i example_input.txt

VI. Contact:
    If you have any questions, please contact:
    peixuanwang@alumni.sjtu.edu.cn

