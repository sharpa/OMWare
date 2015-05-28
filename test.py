#!/usr/bin/python

from Assemble.BioNano.BNGAssembly import Assembly
obj=Assembly()
obj.writeCode()

obj.pairwise_alignment.writeCode()
obj.split.writeCode()
obj.sort.writeCode()
