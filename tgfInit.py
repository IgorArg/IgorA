#!/usr/bin/env python

# Import sys. Need this to get arguments to this script.
import sys

#
import subprocess

# Import method environ
from os import environ

# Import methods isdir
from os.path import isdir

#-----------------------------------------------------------------------------------------------------------------------

def reportError(message):
   print ""
   if len(message)>0:
      print "### ERROR: %s" % message
   else:
      print "### ERROR: Undefined error"
   print "" 

#-----------------------------------------------------------------------------------------------------------------------

def reportErrorAndExit(message):
   reportError(message)
   sys.exit(1)

#-----------------------------------------------------------------------------------------------------------------------

# Define fall-back path to TGF
TGF_PATH="/lib"

if "READCONFIG_ADDR" in environ:
   TGF_LIB_DIR=""
   TGF_MAIN_FILE=""
   #===========================================
   # Find path to TGF library directory
   #===========================================
   lastCmd="readConfig -query \"key='TEST_GENERATOR_FRAMEWORK_LIB_DIR'\" -f \"%path/%name\""
   try:
      TMP_DIR_PATH=subprocess.check_output(lastCmd, shell=True)
      TGF_LIB_DIR=TMP_DIR_PATH.strip()
      if not isdir(TGF_LIB_DIR):
         reportErrorAndExit("Test Generator Framework library path does not exist.")
   except subprocess.CalledProcessError, e:
      errMsg="The readConfig command (%s) failed.\n" % lastCmd
      if len(e.output)>0:
         errMsg+="\n"
         errMsg+="    The readConfig command output:\n"
         errMsg+="    ------------------------------\n"
         errMsg+=e.output
      else:
         errMsg+="\n"
         errMsg+="    No readConfig command output.\n"
      reportErrorAndExit(errMsg)
elif isdir(TGF_PATH):
   TGF_LIB_DIR=TGF_PATH
   environ["TGF_HOME"]=TGF_PATH
else:
   reportErrorAndExit("No active readConfig session.")

#===========================================
# Initiate TFG and set environment variable
#===========================================
environ["TGF_LIB_DIR"]=TGF_LIB_DIR
sys.path.append(TGF_LIB_DIR)
import GPmain as tgf
