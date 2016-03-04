from Operations.BioNano.files import XmapFile
with open('partial_matches.xmap', 'w') as o_file:
	xfile=XmapFile('EXP_REFINEFINAL1.xmap')
	count=0
	for align in xfile.parse():
		proportion=abs(align.query_start-align.query_end)/float(align.query_len)
		print(proportion)
	for align in xfile.parse():
		proportion=abs(align.query_start-align.query_end)/float(align.query_len)
		if proportion < 0.9:
			xfile.write(align, o_file)
			print("\t".join([str(align.query_id),str(proportion),str(align.anchor_id),str(align.anchor_start/1000000)]))
			count+=1
