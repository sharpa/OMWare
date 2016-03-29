# Module: UnitTests.tScripts
# Version: 0.1
# Author: Aaron Sharp
# Date: 03/22/16
#
# This module represents a sort of black-box
# test that will check certain script inputs
# for expected script outputs

import unittest
import os
import shutil
import subprocess
from StringIO import StringIO

class tScripts(unittest.TestCase):
	test_dir='script_test'
	saved_path=os.getcwd()
	@classmethod
	def setUpClass(cls):
		os.mkdir(cls.test_dir)
		os.chdir(cls.test_dir)
	@classmethod
	def tearDownClass(cls):
		os.chdir(cls.saved_path)
		shutil.rmtree(cls.test_dir)

class tFindBreakpoints(tScripts):
	maxDiff=None
	xmap_name='file.xmap'
	xmap_writer=None
	xmap=None
	query_cmap_name='file_r.cmap'
	query_cmap=None
	anchor_cmap_name='file_q.cmap'
	anchor_cmap=None
	cmap_writer=None
	def setUp(self):
		self.xmap=open(self.xmap_name, 'w')
		self.xmap_writer=XmapFile(self.xmap_name)
		self.query_cmap=open(self.query_cmap_name, 'w')
		self.anchor_cmap=open(self.anchor_cmap_name, 'w')
		self.cmap_writer=CmapFile(self.query_cmap_name)
	def tearDown(self):
		self.xmap.close()
		self.query_cmap.close()
		self.anchor_cmap.close()
		os.remove(self.xmap_name)
		os.remove(self.query_cmap_name)
		os.remove(self.anchor_cmap_name)

	### Bad input ###
	def test_badInput_none(self):
		expected_stdout="usage: find_breakpoints.py [-h] xmap_file\nfind_breakpoints.py: error: too few arguments\n"
		expected_returnCode=2
		expecteds=[expected_stdout, expected_returnCode]
		actual_stdout=None
		try:

			actual_stdout=subprocess.check_output("../scripts/find_breakpoints.py", stderr=subprocess.STDOUT)

			actual_returnCode=0
		except subprocess.CalledProcessError as error:
			actual_stdout=error.output
			actual_returnCode=error.returncode
		except:
			raise
		actuals=[actual_stdout, actual_returnCode]

		self.assertEquals(expecteds, actuals)

	def test_badInput_notAFile(self):
		expected_stdout="The .xmap alignment file you specified, file.xmap.bed.ext, could not be found\n"
		expected_returnCode=1
		expecteds=[expected_stdout, expected_returnCode]
		actual_stdout=None
		try:

			actual_stdout=subprocess.check_output(["../scripts/find_breakpoints.py",self.xmap_name+".bed.ext"], stderr=subprocess.STDOUT)

			actual_returnCode=0
		except subprocess.CalledProcessError as error:
			actual_stdout=error.output
			actual_returnCode=error.returncode
		except:
			raise
		actuals=[actual_stdout, actual_returnCode]

		self.assertEquals(expecteds, actuals)

	@unittest.skip('not_implemented')
	def test_badInput_notXmap(self):
		pass
	def test_badInput_contigInXmapNotInAnchorCmap(self):
		for label_position in xrange(1,1000):
			label=Mock(contig_id=1, contig_len=1000, contig_site_count=1000, label_id=label_position, channel="1", position=label_position, stdev=0, coverage=1, occurrences=1)
			self.cmap_writer.write(label, self.query_cmap)
		self.query_cmap.close()
		alignment=Mock(alignment_id=1, query_id=1, anchor_id=1, query_start=2, query_end=998, anchor_start=1, anchor_end=1000, orientation='+', confidence=250,hit_enum="*", query_len=1000, anchor_len=1000, label_channel="1", alignment="*")
		self.xmap_writer.write(alignment, self.xmap)
		self.xmap.close()
		expected_stdout="The .xmap alignment ("+self.xmap_name+") file contains a contig id (1) that was not found in one of the .cmap contig files ("+self.anchor_cmap_name+")\n"
		expected_returnCode=1
		expecteds=[expected_stdout, expected_returnCode]
		try:

			actual_stdout=subprocess.check_output(["../scripts/find_breakpoints.py",self.xmap_name], stderr=subprocess.STDOUT)

			actual_returnCode=0
		except subprocess.CalledProcessError as error:
			actual_stdout=error.output
			actual_returnCode=error.returncode
		except:
			raise
		actuals=[actual_stdout, actual_returnCode]

		self.assertEquals(expecteds, actuals)
	def test_badInput_contigInXmapNotInQueryCmap(self):
		for label_position in xrange(1,1000):
			label=Mock(contig_id=1, contig_len=1000, contig_site_count=1000, label_id=label_position, channel="1", position=label_position, stdev=0, coverage=1, occurrences=1)
			self.cmap_writer.write(label, self.anchor_cmap)
		self.anchor_cmap.close()
		alignment=Mock(alignment_id=1, query_id=1, anchor_id=1, query_start=2, query_end=998, anchor_start=1, anchor_end=1000, orientation='+', confidence=250,hit_enum="*", query_len=1000, anchor_len=1000, label_channel="1", alignment="*")
		self.xmap_writer.write(alignment, self.xmap)
		self.xmap.close()
		expected_stdout="The .xmap alignment ("+self.xmap_name+") file contains a contig id (1) that was not found in one of the .cmap contig files ("+self.query_cmap_name+")\n"
		expected_returnCode=1
		expecteds=[expected_stdout, expected_returnCode]
		try:

			actual_stdout=subprocess.check_output(["../scripts/find_breakpoints.py",self.xmap_name], stderr=subprocess.STDOUT)

			actual_returnCode=0
		except subprocess.CalledProcessError as error:
			actual_stdout=error.output
			actual_returnCode=error.returncode
		except:
			raise
		actuals=[actual_stdout, actual_returnCode]

		self.assertEquals(expecteds, actuals)
	def test_badInput_cantFindCmap(self):
		os.remove(self.query_cmap_name)
		os.remove(self.anchor_cmap_name)
		expected_stdout="Some of the .cmap contig files associated with your .xmap alignment file could not be found. More specifically, Unable to find query, anchor maps.\n"
		expected_returnCode=1
		expecteds=[expected_stdout, expected_returnCode]
		actual_stdout=None
		try:

			actual_stdout=subprocess.check_output(["../scripts/find_breakpoints.py",self.xmap_name], stderr=subprocess.STDOUT)

			actual_returnCode=0
		except subprocess.CalledProcessError as error:
			actual_stdout=error.output
			actual_returnCode=error.returncode
		except:
			raise
		actuals=[actual_stdout, actual_returnCode]
		with open(self.query_cmap_name, 'w'):
			pass
		with open(self.anchor_cmap_name, 'w'):
			pass

		self.assertEquals(expecteds, actuals)

	### One alignment only ###
	def test_oneAlignment_no5PercentOverhang(self):
		for label_position in xrange(1,1000):
			label=Mock(contig_id=1, contig_len=1000, contig_site_count=1000, label_id=label_position, channel="1", position=label_position, stdev=0, coverage=1, occurrences=1)
			self.cmap_writer.write(label, self.query_cmap)
			self.cmap_writer.write(label, self.anchor_cmap)
		self.query_cmap.close()
		self.anchor_cmap.close()
		alignment=Mock(alignment_id=1, query_id=1, anchor_id=1, query_start=2, query_end=998, anchor_start=1, anchor_end=1000, orientation='+', confidence=250,hit_enum="*", query_len=1000, anchor_len=1000, label_channel="1", alignment="*")
		self.xmap_writer.write(alignment, self.xmap)
		self.xmap.close()
		expected_stdout=""
		expected_returnCode=0
		expecteds=[expected_stdout, expected_returnCode]
		try:

			actual_stdout=subprocess.check_output(["../scripts/find_breakpoints.py",self.xmap_name], stderr=subprocess.STDOUT)

			actual_returnCode=0
		except subprocess.CalledProcessError as error:
			actual_stdout=error.output
			actual_returnCode=error.returncode
		except:
			raise
		actuals=[actual_stdout, actual_returnCode]

		self.assertEquals(expecteds, actuals)
	def test_oneAlignment_noLabeledOverhang(self):
		for label_position in xrange(1,500):
			label=Mock(contig_id=1, contig_len=1000, contig_site_count=1000, label_id=label_position, channel="1", position=label_position, stdev=0, coverage=1, occurrences=1)
			self.cmap_writer.write(label, self.query_cmap)
			self.cmap_writer.write(label, self.anchor_cmap)
		self.query_cmap.close()
		self.anchor_cmap.close()
		alignment=Mock(alignment_id=1, query_id=1, anchor_id=1, query_start=2, query_end=500, anchor_start=1, anchor_end=500, orientation='+', confidence=250,hit_enum="*", query_len=1000, anchor_len=1000, label_channel="1", alignment="*")
		self.xmap_writer.write(alignment, self.xmap)
		self.xmap.close()
		expected_stdout=""
		expected_returnCode=0
		expecteds=[expected_stdout, expected_returnCode]
		try:

			actual_stdout=subprocess.check_output(["../scripts/find_breakpoints.py",self.xmap_name], stderr=subprocess.STDOUT)

			actual_returnCode=0
		except subprocess.CalledProcessError as error:
			actual_stdout=error.output
			actual_returnCode=error.returncode
		except:
			raise
		actuals=[actual_stdout, actual_returnCode]

		self.assertEquals(expecteds, actuals)

	def test_oneAlignment_oneSingleLabelOverhang(self):
		for label_position in xrange(1,502):
			label=Mock(contig_id=1, contig_len=1000, contig_site_count=1000, label_id=label_position, channel="1", position=label_position, stdev=0, coverage=1, occurrences=1)
			self.cmap_writer.write(label, self.query_cmap)
			self.cmap_writer.write(label, self.anchor_cmap)
		self.query_cmap.close()
		self.anchor_cmap.close()
		alignment=Mock(alignment_id=1, query_id=1, anchor_id=1, query_start=2, query_end=500, anchor_start=1, anchor_end=500, orientation='+', confidence=250,hit_enum="*", query_len=1000, anchor_len=1000, label_channel="1", alignment="*")
		self.xmap_writer.write(alignment, self.xmap)
		self.xmap.close()
		expected_stdout="Chr01\t500\t501\t1\t250.0\t+\n"
		expected_returnCode=0
		expecteds=[expected_stdout, expected_returnCode]
		try:

			actual_stdout=subprocess.check_output(["../scripts/find_breakpoints.py",self.xmap_name], stderr=subprocess.STDOUT)

			actual_returnCode=0
		except subprocess.CalledProcessError as error:
			actual_stdout=error.output
			actual_returnCode=error.returncode
		except:
			raise
		actuals=[actual_stdout, actual_returnCode]

		self.assertEquals(expecteds, actuals)
	def test_oneAlignment_oneLabeledOverhang(self):
		for label_position in xrange(1,1000):
			label=Mock(contig_id=1, contig_len=1000, contig_site_count=1000, label_id=label_position, channel="1", position=label_position, stdev=0, coverage=1, occurrences=1)
			self.cmap_writer.write(label, self.query_cmap)
			self.cmap_writer.write(label, self.anchor_cmap)
		self.query_cmap.close()
		self.anchor_cmap.close()
		alignment=Mock(alignment_id=1, query_id=1, anchor_id=1, query_start=2, query_end=500, anchor_start=1, anchor_end=500, orientation='+', confidence=250,hit_enum="*", query_len=1000, anchor_len=1000, label_channel="1", alignment="*")
		self.xmap_writer.write(alignment, self.xmap)
		self.xmap.close()
		expected_stdout="Chr01\t500\t502\t1\t250.0\t+\n"
		expected_returnCode=0
		expecteds=[expected_stdout, expected_returnCode]
		try:

			actual_stdout=subprocess.check_output(["../scripts/find_breakpoints.py",self.xmap_name], stderr=subprocess.STDOUT)

			actual_returnCode=0
		except subprocess.CalledProcessError as error:
			actual_stdout=error.output
			actual_returnCode=error.returncode
		except:
			raise
		actuals=[actual_stdout, actual_returnCode]

		self.assertEquals(expecteds, actuals)

	### Multiple alignments ###
	@unittest.skip('not implmemented')
	def test_multipleAligns_noTwoLabelOverhang(self):
		pass

from UnitTests.Helper import Mock
from Operations.BioNano.files import XmapFile
from Operations.BioNano.files import CmapFile
