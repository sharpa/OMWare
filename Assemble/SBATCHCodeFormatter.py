# Module: Assemble.BioNano.BNGAssembly
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/03/2015
# 
# The purpose of this module is take as input "code" for a code generator (step)
# class, and format it for a specific platform, namely SBATCH
import Assemble.CodeFormatter

class CodeFormatter (Assemble.CodeFormatter.CodeFormatter):
	def __init__(self):
		pass
	def formatCode(self, step):
		batch_steps=[]
		
		prereqs=step.getPrereqs()
		for prereq in prereqs:
			batch_steps.extend(self.formatCode(prereq))
		
		batch_step_parts=[]
		for part in step.writeCode():
			batch_step_part="#!/bin/bash\n"
			batch_step_part+="#SBATCH --mem " + str(1024*step.getMem()) + "M\n"
			batch_step_part+="#SBATCH --time " + str(step.getTime()) + ":00:00\n"
			batch_step_part+="#SBATCH --ntasks " + str(step.getThreads()) + "\n"
			batch_step_part+=part + "\n"
			batch_step_parts.append(batch_step_part)
		batch_steps.append(batch_step_parts)

		return batch_steps

	def serializeCode(self, step):
		steps_and_parts=self.formatCode(step)

		print("#!/bin/bash\n")

		print("afterok_done=\"\"")
		print("afterok_build=\"\"\n")
		for step_num, step in enumerate(steps_and_parts):
			for part_num, part in enumerate(step):
				o_file_name="step" + str(step_num+1) + "_part" + str(part_num+1) + ".sh"
				o_file=open(o_file_name, "w")
				o_file.write(part)
				print("sresult=`sbatch $afterok_done " + o_file_name + "`")
				print("echo $sresult")
				print("sid=`echo $sresult | awk '{print $NF}'`")
				print("afterok_build=$afterok_build:$sid\n")

			print("afterok_done=\"-d afterok\"$afterok_build")
			print("afterok_build=\"\"\n")
				
