#!/fslhome/jtpage/bin/python

from Operations.BioNano.Compare.AssessReferenceAlignment import AssessReferenceAlignment

af=AssessReferenceAlignment('./EXP_REFINEFINAL1.xmap')
af.extractFalsePositives()
af.extractFalseNegatives()
af.extractTruePositives()

nearest_to_fp=af.findNearestNeighbors(af.false_positive_locations, [af.false_negative_locations, af.true_positive_locations])
nearest_to_fn=af.findNearestNeighbors(af.false_negative_locations, [af.false_positive_locations, af.true_positive_locations])

fp_count=0
for chr in nearest_to_fp:
	for distance in nearest_to_fp[chr]:
		if distance < 301:
			fp_count+=1
fn_count=0
for chr in nearest_to_fn:
	for distance in nearest_to_fn[chr]:
		if distance < 301:
			fn_count+=1

print("fp < 301 bp away: " + str(fp_count))
print("fn < 301 bp away: " + str(fn_count))
