from Operations.BioNano.Compare.AssessReferenceAlignment import AssessReferenceAlignment
af=AssessReferenceAlignment('./EXP_REFINEFINAL1.xmap')
af.extractFalsePositives()

bspqi_site="GCTCTTC"
snvs=set()
for i in xrange(0,len(bspqi_site)):
	for base in ['A', 'T', 'C', 'G']:
		if base==bspqi_site[i]:
			continue
		snv=bspqi_site[0:i]+base+bspqi_site[i+1:len(bspqi_site)]
		print(snv)
		snvs.add(snv)

from Bio import SeqIO
for record in SeqIO.parse('false_positive_regions.fasta', 'fasta'):
	output=""
	if "NNNNNNN" in record.seq:
		output="1"
	contains_snv=False
	for snv in snvs:
		if snv in record.seq:
			contains_snv=True
	if contains_snv:
		output+="\t1"
	else:
		output+="\t0"
	print(output)

