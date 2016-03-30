#!/usr/bin/python

from argparse import ArgumentParser
parser=ArgumentParser(description='Use physical map evidence to break inaccurate joins in a reference (perhaps sequnence) genome')
parser.add_argument('xmap_file', help='.xmap alignment file where the physical map evidence is the query, and the reference to be broken is the anchor')
args=parser.parse_args()

from Operations.BioNano.files import XmapFile
import Operations.BioNano.exceptions
from Operations.BioNano.Compare.Comparison import Comparison
try:
	comparison=Comparison(XmapFile(args.xmap_file))
	for bp in comparison.findBreakPoints():
		print("\t".join([str(x) for x in bp]))
except IOError:
	print("The .xmap alignment file you specified, "+args.xmap_file+", could not be found")
	exit(1)
except Operations.BioNano.exceptions.FileArrangementException as e:
	print("Some of the .cmap contig files associated with your .xmap alignment file could not be found. More specifically, "+e.message)
	exit(1)
except Operations.BioNano.exceptions.FileMismatchException as e:
	print("The .xmap alignment ("+str(e.containing_file)+") file contains a contig id ("+str(e.mismatched_entity)+") that was not found in one of the .cmap contig files ("+str(e.missing_file)+")")
	exit(1)
except:
	raise
