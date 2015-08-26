# Module: UnitTests.tFiles
# Version: 0.1
# Author: Aaron Sharp
# Date: 08/10/2015
# 
# The purpose of this module is to provide unit tests for 
# all BioNano file objects

import unittest
import os
from StringIO import StringIO
from UnitTests.Helper import Mock
from Operations.BioNano.files import File
from Operations.BioNano.files import File_iter
from Operations.BioNano.files import CmapFile
from Operations.BioNano.files import CmapFile_iter
from Operations.BioNano.files import XmapFile
from Operations.BioNano.files import XmapFile_iter

class tFile_base(unittest.TestCase):
	input_file="file.cmap"
	def setUp(self):
		with open(self.input_file, "w"):
			self.obj=File(self.input_file)

	def tearDown(self):
		os.remove(self.input_file)

class tFile(tFile_base):
	def test_init_fileDoesNotExist(self):
		with self.assertRaises(Exception):
			File("bad_filename")
	def test_init_fileDoesExist(self):
		self.assertEqual(self.input_file, self.obj.input_file)
	def test_equal_otherIsNone(self):
		other=None
		self.assertFalse(self.obj==other)
	def test_equal_otherHasDiffFile(self):
		other_file="other_file.ext"
		with open(other_file, "w"):
			other=File(other_file)
		os.remove(other_file)
		self.assertFalse(self.obj==other)
	def test_equal_sameFile(self):
		other=Mock(input_file=self.input_file)
		self.assertTrue(self.obj==other)

	def test_getExtension(self):
		with self.assertRaises(Exception):
			File.getExtension()

	def test_getHeaders(self):
		expected=["#Header1\n",
			"#Header2\n",
			"#Header3\n",
			"#Header4\n"]
		with open(self.input_file, "w") as i_file:
			i_file.write("".join(expected))
			i_file.write("\n".join(["Non-header1", "#Comment but not header1"]) + "\n")

		actual=self.obj.getHeaders()

		self.assertEqual(expected, actual)

	def test_parse(self):
		with self.assertRaises(Exception):
			self.obj.parse()
	def test_write(self):
		with self.assertRaises(Exception):
			self.obj.write(None, None)

class tFile_iter(unittest.TestCase):
	input_file="file.cmap"
	def setUp(self):
		with open(self.input_file, "w"):
			self.obj=File_iter(self.input_file)
	def tearDown(self):
		os.remove(self.input_file)
	def test_init(self):
		self.assertEqual(open(self.input_file).name, self.obj.i_file.name)
	def test_iter(self):
		self.assertEqual(self.obj, self.obj.__iter__())
	def test_equal_none(self):
		other=None
		self.assertFalse(self.obj==other)
	def test_equal_diffClass(self):
		other=Mock(i_file=open(self.input_file))
		self.assertFalse(self.obj==other)

	def test_equal_diffFile(self):
		with open("other_file", "w") as other_file:
			other=File_iter("other_file")
		os.remove("other_file")

		self.assertFalse(self.obj==other)

	def test_equal_isEqual(self):
		other=File_iter(self.input_file)
		self.assertTrue(self.obj==other)


class tCmapFile(tFile_base):
	def setUp(self):
		with open(self.input_file, "w"):
			self.obj=CmapFile(self.input_file)
	def test_getExtension(self):
		self.assertEqual("cmap", CmapFile.getExtension())
	
	def test_parse(self):
		expected=CmapFile_iter(self.input_file)
		self.assertEqual(expected, self.obj.parse())

	def test_write(self):
		label=Mock(contig_id=1, contig_len=1.0, contig_site_count=1, label_id=1, channel="1", position=1.0, stdev=1.0, coverage=1.0, occurrences=1, snr_mean=1.0, snr_stdev=1.0, snr_count=1.0)
		expected="\t".join([str(label.contig_id), str(label.contig_len), str(label.contig_site_count), str(label.label_id), label.channel, str(label.position), str(label.stdev), str(label.coverage), str(label.occurrences), str(label.snr_mean), str(label.snr_stdev), str(label.snr_count)]) + "\n"
		o_file=StringIO()

		self.obj.write(label, o_file)

		self.assertEqual(expected, o_file.getvalue())

class tCmapFile_iter(unittest.TestCase):
	input_file="file.cmap"
	def setUp(self):
		with open(self.input_file, "w"):
			self.obj=CmapFile_iter(self.input_file)
	def tearDown(self):
		os.remove(self.input_file)

	def test_next_emptyFile(self):
		with self.assertRaises(StopIteration):
			self.assertEqual(None, self.obj.next())
	def test_next_badFileFormat(self):
		with open(self.input_file, "w") as o_file:
			o_file.write("1	2	3	4	5	6	7	8	9	10\n")
		with self.assertRaises(Exception):
			self.obj.next()

	def test_next_skipsHeaders(self):
		with open(self.input_file, "w") as o_file:
			o_file.write("# this is a comment")
		with self.assertRaises(StopIteration):
			self.obj.next()

	def test_next_twoLines(self):
		expected=Mock(contig_id=1, contig_len=2.0, contig_site_count=3, label_id=4, channel="5", position=6.0, stdev=7.0, coverage=8.0, occurrences=9.0, snr_mean=10.0, snr_stdev=11.0, snr_count=12.0)
		with open(self.input_file, "w") as o_file:
			o_file.write("1	2	3	4	5	6	7	8	9	10	11	12")

		self.assertEqual(expected, self.obj.next())

class tXmapFile(tFile_base):
	def setUp(self):
		with open(self.input_file, "w"):
			self.obj=XmapFile(self.input_file)
	def test_getExtension(self):
		self.assertEquals("xmap", XmapFile.getExtension())

	def test_parse(self):
		expected=XmapFile_iter(self.input_file)
		self.assertEqual(expected, self.obj.parse())

	def test_write(self):
		expected="1	2	3	1.0	2.0	1.0	2.0	+	999.9	1DM	1.0	1.0	1	(1,1)(1,2)\n"
		alignment=Mock(alignment_id=1, query_id=2, anchor_id=3, query_start=1.0, query_end=2.0, anchor_start=1.0, anchor_end=2.0, orientation="+", confidence=999.9, hit_enum="1DM", query_len=1.0, anchor_len=1.0, label_channel="1", alignment="(1,1)(1,2)")
		with open("test_file", "w") as o_file:

			self.obj.write(alignment, o_file)

		with open("test_file") as i_file:
			actual=i_file.readline()
		os.remove("test_file")

		self.assertEqual(expected, actual)

class tXmapFile_iter(unittest.TestCase):
	input_file="test.xmap"
	def setUp(self):
		with open(self.input_file, "w"):
			self.obj=XmapFile_iter(self.input_file)

	def tearDown(self):
		os.remove(self.input_file)

	def test_next_emptyFile(self):
		with self.assertRaises(StopIteration):
			self.obj.next()
		
	def test_next_badFileFormat(self):
		with open(self.input_file, "w") as i_file:
			i_file.write("1	2	3	4	5\n")

		with self.assertRaises(Exception):
			self.obj.next()

	def test_next_skipsHeaders(self):
		with open(self.input_file, "w") as o_file:
			o_file.write("# this is a comment")
		with self.assertRaises(StopIteration):
			self.obj.next()
		
	def test_next_goodFormat(self):
		expected=Mock(alignment_id=0, query_id=1, anchor_id=2, query_start=3.0, query_end=4.0, query_len=10.0, anchor_start=5.0, anchor_end=6.0, anchor_len=11.0, orientation="+", confidence=8.0, hit_enum="9D", label_channel="channel12", alignment="(1,3)")
		with open(self.input_file, "w") as i_file:
			i_file.write("#1	2	3	4	5\n0	1	2	3.0	4.0	5.0	6.0	+	8.0	9D	10.0	11.0	channel12	(1,3)")

		actual=self.obj.next()

		self.assertEqual(expected, actual)
