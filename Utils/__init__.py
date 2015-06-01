# Common, miscellaneous scripts for optical map manipulation

# CodeWriter
# This module provides [will provide] encapsulation for platform specific code writing
# For example, I may want to run my assembly in serial on my Windows laptop (not a great idea),
# or I may want to run it in serial on a specific flavor of linux based cluster (more likely).
# It's not the job of the optical map assembly to keep track of OS specifications

# Resources
# Similar to code writer above, many assembly algorithms are sensitive to hardware availabilities,
# such as maximum memory or threads

# Wizard
# I'm envisioning a sort of question and answer command line interface experience that will allow
# new users to choose input parameter values with confidence.  It will include helpful hints.

# Rarefactor
# A question that has been a big deal in my lab is this: what amount of coverage is necessary?
# As part of the answer to that question, we reduced a single input dataset by random molecule removal

# CD
# Every "step" has a working directory that is separate from the code directory.  This class
# encapsulates the process of changing directories, and is very careful to change back once complete

# Workspace
# Encapsulates information that every code-generator needs to know, and can only get from the outside
# For example, executables, work dirs, and input datasets
