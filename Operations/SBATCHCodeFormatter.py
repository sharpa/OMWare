# Module: Operations.SBATCHCodeFormatter
# Version: 0.1
# Author: Aaron Sharp
# Date: 06/03/2015
# 
# The purpose of this module is take as input "code" for a code generator (step)
# class, and format it for a specific platform, namely SBATCH
import Operations.CodeFormatter

class CodeFormatter (Operations.CodeFormatter.CodeFormatter):
	def __init__(self):
		pass
	def formatCode(self, step):
		batch_step_parts=[]
		for part in step.writeCode():
			batch_step_part="#!/bin/bash\n"
			batch_step_part+="#SBATCH --mem " + str(1024*step.getMem()) + "M\n"
			batch_step_part+="#SBATCH --time " + str(step.getTime()) + ":00:00\n"
			batch_step_part+="#SBATCH --ntasks 1\n"
			batch_step_part+="#SBATCH --cpus-per-task " + str(step.getThreads()) + "\n"

			errorNotificationEmail=step.getErrorNotificationEmail()
			if errorNotificationEmail is not None:
				batch_step_part+="#SBATCH --mail-user=" + errorNotificationEmail + "\n"
				batch_step_part+="#SBATCH --mail-type=FAIL\n"

			batch_step_part+=part + "\n"
			batch_step_parts.append(batch_step_part)
		return batch_step_parts

	def runOneStep(self, step):
		steps_retroorder=[]
		
		prereq=step
		while prereq is not None:
			if not prereq.isComplete():
				steps_retroorder.append(prereq)
			prereq=prereq.getPrereq()
		steps=steps_retroorder[::-1]
		
		steps_and_parts=[]
		for step in steps:
			parts=self.formatCode(step)
			if len(parts)>0:
				steps_and_parts.append(parts)

		print("#!/bin/bash\n")

		for step_num, step in enumerate(steps_and_parts):
			step_part_files=[]
			for part_num, part in enumerate(step):
				o_file_name="step" + str(step_num+1) + "_part" + str(part_num+1) + ".sh"
				o_file=open(o_file_name, "w")
				o_file.write(part)
				o_file.close()
				step_part_files.append(o_file_name)
				
			step_name="step" + str(step_num+1)
			dependency_clause="" if step_num==0 else "$step" + str(step_num)
			self.runStepInContext(step_part_files, step_name, dependency_clause)

	def runSeveralSteps(self, levels):
		print("#!/bin/bash\n")

		step_names={}
		for level_num, level in enumerate(levels):
			for step_num, step in enumerate(level):
				if step.isComplete():
					continue
				step_name="level" + str(level_num+1) + "_step" + str(step_num+1)
				step_names[step]=step_name
				step_parts=self.formatCode(step)

				step_part_files=[]
				for part_num, part in enumerate(step_parts):
					o_file_name=step_name + "_part" + str(part_num+1) + ".sh"
					o_file=open(o_file_name, "w")
					o_file.write(part)
					o_file.close()
					step_part_files.append(o_file_name)

				prereq=step.getPrereq()

                                dependency_clause=""
                                if prereq is not None:
                                        if prereq in step_names:
                                                dependency_clause= "$" + step_names[prereq]
				self.runStepInContext(step_part_files, step_name, dependency_clause)
				

	def runStepInContext(self, step_part_files, step_name, dependency_clause):
		print("")
		print(step_name + "=\"-d afterok\"")
		for step_part_file in step_part_files:
			print("sresult=`sbatch " + dependency_clause + " " + step_part_file + "`")
			print("echo $sresult")
			print("sid=`echo $sresult | awk '{print $NF}'`")
			print(step_name + "=$" + step_name + ":$sid")
