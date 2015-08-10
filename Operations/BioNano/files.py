# Module: Operations.BioNano.files
# Version: 0.1
# Author: Aaron Sharp
# Date: 05/26/2015
# 
# The purpose of this module is to manipulate optical maps
# as they appear in a variety of BNG file formats

class File(object):
	def __init__(self, input_file):
		i_file=open(input_file, "r")
		i_file.close()
		self.input_file=input_file
	def __eq__(self, other):
		if other is None:
			return False
		return self.input_file==other.input_file
	def __ne__(self, other):
		return self.input_file!=other.input_file

	@staticmethod
	def getExtension():
		raise Exception("Abstract method called")

	def getHeaders(self):
		headers=[]
		with open(self.input_file, "r") as i_file:
			for line in i_file:
				if line[0]=="#":
					headers.append(line)
				else:
					break
		return headers

	def parse(self):
		raise Exception("Abstract method called")
	def write(self, entity, o_file):
		raise Exception("Abstract method called")
		

class BnxFile(File):
	@staticmethod
	def getExtension():
		return "bnx"

	def parse(self):
		return BnxFile_iter(self.input_file)

	def write(self, molecule, o_file):

		o_file.write("	".join(["0", str(molecule.id), str(molecule.length), str(molecule.average_intensity), str(molecule.snr), str(molecule.num_labels), str(molecule.original_id), str(molecule.scan_id), str(molecule.scan_direction), str(molecule.chip_id), str(molecule.flowcell), str(molecule.run_id), str(molecule.global_scan_id)]) + "\n")

		label_data=["1", "0.0"]
		label_data.extend([str(i) for i in molecule.labels])
		o_file.write("	".join(label_data) + "\n")

		quality_one_data=["QX11"]
		quality_one_data.extend(molecule.qualities_one)
		o_file.write("	".join(quality_one_data) + "\n")

		quality_two_data=["QX12"]
		quality_two_data.extend(molecule.qualities_two)
		o_file.write("	".join(quality_two_data) + "\n")

class BnxFile_iter:
	def __init__(self, input_file):
		self.i_file=open(input_file, "r")
	def __iter__(self):
		return self
	def next(self):
		while True:
			try:
				line=self.i_file.readline()
				if line=='':
					self.i_file.close()
					raise StopIteration

				if line[0]=="#":
					continue

				if line [0] != "0":
					raise Exception("this file is incorrectly formatted")
				molecule_data=line.split()
				new_molecule=Molecule(molecule_data[1], float(molecule_data[2]))

				new_molecule.average_intensity=molecule_data[3]
				new_molecule.snr=molecule_data[4]
				new_molecule.num_labels=molecule_data[5]
				new_molecule.original_id=molecule_data[6]
				new_molecule.scan_id=molecule_data[7]
				new_molecule.scan_direction=molecule_data[8]
				new_molecule.chip_id=molecule_data[9]
				new_molecule.flowcell=molecule_data[10]
				new_molecule.run_id=molecule_data[11]
				new_molecule.global_scan_id=molecule_data[12]

				label_line=self.i_file.readline()
				if label_line[0] != "1":
					raise Exception("this file is incorrectly formatted")
				new_molecule.labels=label_line.split()[2:]
				
				quality_line_one=self.i_file.readline()
				if quality_line_one[0:4] != "QX11":
					raise Exception("this file is incorrectly formatted")
				new_molecule.qualities_one=quality_line_one.split()[1:]
				
				quality_line_two=self.i_file.readline()
				if quality_line_two[0:4] != "QX12":
					raise Exception("this file is incorrectly formatted")
				new_molecule.qualities_two=quality_line_two.split()[1:]

				return new_molecule
			except StopIteration:
				raise
			except IndexError:
				raise Exception("this file is incorrectly formatted")
			except:
				raise


class Molecule:
	def __init__(self, id, length):
		self.id=id
		self.length=length

	def shrink(self, new_length):
		self.length=new_length

		num_labels=len(self.labels)
		last_label_index=-1
		for i in xrange(num_labels-1, -1, -1):
			if float(self.labels[i]) <= float(self.length):
				last_label_index=i
				break
			if i==0:
				last_label_index=0

		quality_one_of_molecule_end=self.qualities_one[num_labels-1]
		quality_two_of_molecule_end=self.qualities_two[num_labels-1]

		self.labels=self.labels[0:last_label_index]
		self.qualities_one=self.qualities_one[0:last_label_index]
		self.qualities_two=self.qualities_two[0:last_label_index]

		self.labels.append(self.length)
		self.qualities_one.append(quality_one_of_molecule_end)
		self.qualities_two.append(quality_two_of_molecule_end)

		self.num_labels=last_label_index+1

class CmapFile(File):
	@staticmethod
	def getExtension():
		return "cmap"
	def parse(self):
		return CmapFile_iter(self.input_file)
	def write(self, label, o_file):
		fields=[str(label.contig_id),
			str(label.contig_len),
			str(label.contig_site_count),
			str(label.label_id),
			label.channel,
			str(label.position),
			str(label.stdev),
			str(label.coverage),
			str(label.occurrences),
			str(label.snr_mean),
			str(label.snr_stdev),
			str(label.snr_count)]
		o_file.write("\t".join(fields) + "\n")

class CmapFile_iter:
	def __init__(self, input_file):
		self.i_file=open(input_file)
	def __iter__(self):
		return self
	def __eq__(self, other):
		if other is None:
			return False
		return self.i_file.name==other.i_file.name
	def __ne__(self, other):
		return self != other
	def next(self):
		while True:
			try:
				line=self.i_file.readline()
				if line=='':
					self.i_file.close()
					raise StopIteration
				if line[0]=="#":
					continue
				label_data=line.split("\t")
				# The cmap file format may have 11 fields, or 12, depending on if it is unmerged, or merged respectively
				if len(label_data)<11:
					raise Exception("this file is incorrectly formatted")

				label_id=int(label_data[3])
				contig_id=int(label_data[0])
				new_label=Label(contig_id, label_id)

				new_label.contig_len=float(label_data[1])
				new_label.contig_site_count=int(label_data[2])

				new_label.channel=label_data[4]
				new_label.position=float(label_data[5])
				new_label.stdev=float(label_data[6])
				new_label.coverage=float(label_data[7]) # I'm not sure why this is a float, not an int
				new_label.occurrences=float(label_data[8])
				new_label.snr_mean=float(label_data[9])
				new_label.snr_stdev=float(label_data[10])
				if len(label_data) > 11:
					new_label.snr_count=float(label_data[11])
				
				return new_label

			except StopIteration:
				raise
			except IndexError:
				raise Exception("this file is incorrectly formatted")
			except:
				raise
				


class Label:
	def __eq__(self, other):
		if other is None:
			return False
		return self.__dict__ == other.__dict__
	def __init__(self, contig_id, label_id):
		self.contig_id=contig_id
		self.label_id=label_id
