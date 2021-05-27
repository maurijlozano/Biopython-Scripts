#!/usr/bin/env python3
'''
NCBI_Assembly_downloader is a program designed to download genome sequences from NCBI Assembly database using Entrez Biopython module.
Written by Mauricio J. Lozano
UNLP - CONICET - Instituto de Biotecnología y Biología Molecular (IBBM)
'''
VERSION="1.0"
GITHUB="https://github.com/maurijlozano/ISCompare"

#Modules
import urllib, gzip, os, sys, re
import argparse
from Bio import Entrez

#************************************
#************************************
#************************************

def printSoftName():
	print("\n\n\n")
	print("   ********************************************")
	print("   *****   NCBI_Assembly_downloader")
	print("   *****   Version: "+str(VERSION))
	print("   *****   Developed by Mauricio J. Lozano")
	print("   *****   github.com/maurijlozano")
	print("   ********************************************")
	print("   Downloaded from: "+GITHUB)
	print("\n\n\n")

def parseArgs():
	'''
	Argument parser.
	'''
	parser = argparse.ArgumentParser(description='NCBI_Assembly_downloader is a program designed to download genome sequences from NCBI Assembly database using Entrez Biopython module..')
	parser.add_argument("-a", "--Assemblies",help="Accession numbers for the assemblies to download from NCBI.", dest="assemblies", action='append', nargs='+', required=True)
	parser.add_argument("-o", "--OutputDir",help="Output folder.",action="store", dest="path", required=False)
	parser.add_argument("-e", "--email",help="User email. Required for accession number download mode.",action="store", dest="yourEmail", required=True)
	#
	args = parser.parse_args()
	return args


def get_assemblies(AssemblyId, path=''):
	"""Download genbank assemblies for a given ID.
		Args:
		ID: search term, usually organism name
		download: whether to download the results
		path: folder to save to
    """
	handle = Entrez.esearch(db="assembly", term=AssemblyId, retmax='200')
	record = Entrez.read(handle)
	print (f'Downloading {AssemblyId}.')
	ids = record['IdList']
	print (f'found {len(ids)} ids')
	links = []
	for id in ids:
		#get summary
		esummary_handle = Entrez.esummary(db="assembly", id=id, report="full")
		summary = Entrez.read(esummary_handle, validate=False)
		#get ftp link
		url = summary['DocumentSummarySet']['DocumentSummary'][0]['FtpPath_RefSeq']
		if url == '':
			continue
		label = os.path.basename(url)
		link = os.path.join(url,label+'_genomic.gbff.gz')
		links.append(link)
		#download link
		fileName = f'{label}.gbff.gz'
		fileGBpath = f'./{path}'
		fileGBname = f'./{path}/{label}.gb'
		fileGB = open(fileGBname,"w+")
		urllib.request.urlretrieve(link, fileName)
		with gzip.open(fileName) as gzipfile:
			fileGB.write(gzipfile.read().decode("utf-8"))
		fileGB.close()
		os.remove(fileName)



#************************************
#************************************
#************************************


if __name__ == "__main__":
	#Presentation
	printSoftName()
	#Argument parsing
	args = parseArgs()
	#email verification
	if not args.yourEmail:
		sys.stdout.write("You must supply an email address for accession number mode.\n")
		sys.exit()
	elif not re.match('[^@]+@[^@]+\..*$',args.yourEmail):
		sys.stdout.write("Wrong email format.\n")
		sys.exit()
	else:
		Entrez.email = args.yourEmail
	#Path verification
	if args.path:
		path=args.path
		if not os.path.exists(path):
			os.mkdir(path)
			print("Directory " , path ,  " created.")
		else:
			print("Directory " , path ,  " already exists.")
	else:
		path='Assemblies'
		if not os.path.exists(path):
			os.mkdir(path)
			print("Using default folder, 'Assemblies'.")
		else:
			print("Directory " , path ,  " already exists.")	
	if not args.assemblies:
		sys.stdout.write("You must supply an email address for accession number mode.\n")
		sys.exit()
	else:
		assemblies = args.assemblies[0]
	for assembly in assemblies:
		get_assemblies(assembly, path=path)
#END
