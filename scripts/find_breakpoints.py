#!/usr/bin/python

from argparse import ArgumentParser
parser=ArgumentParser(description='Use physical map evidence to break inaccurate joins in a reference (perhaps sequnence) genome')
parser.add_argument('xmap_file', help='.xmap alignment file where the physical map evidence is the query, and the reference to be broken is the anchor')
args=parser.parse_args()

from Operations.BioNano.files import XmapFile
from Operations.BioNano.Compare.Comparison import Comparison
comparison=Comparison(XmapFile(args.xmap_file))
for bp in comparison.findBreakPoints():
	print("\t".join([str(x) for x in bp]))
