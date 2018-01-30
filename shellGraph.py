#!/usr/bin/python
import sys
from graphviz import Digraph

# Parsing based on Bash Grammar provided in link : http://wiki.bash-hackers.org/syntax/basicgrammar

class BashParser:
	shellbuiltInWords="alias,bg,bind,break,builtin,caller,cd,command,compgen,complete,compopt,continue,declare,dirs,disown,echo,enable,eval,exec,exit,export,false,fc,fg,getopts,hash,help,history,jobs,kill,let,local,logout,mapfile,popd,printf,pushd,pwd,read,readarray,readonly,return,set,shift,shopt,source,suspend,test,times,trap,true,type,typeset,ulimit,umask,unalias,unset,wait"
	usualCommands="mkdir,rmdir,rm -rf,ls,ps,tree,find,grep,egrep,sed,awk,ifconfig,ping,rm,du,df,less,more,test"
	complexWords="for,if,fi,do,done,while,{,},((,)),[[,]],case,esac,until,select"
	def __init__(self):
		self.line=""
	def parse(self, cmdString):
		cmdString=cmdString.strip()
		cmd=None
		
		if ( ("||" not in cmdString) and ("|" in cmdString)):
			cmd=PipelineCommand(cmdString)
			return cmd	
		elif (("&&" in cmdString) or ("&" in cmdString )or ("||" in cmdString) ):
			cmd=ListCommand(cmdString)
			return cmd
		#elif ("{" in cmdString or "}" in cmdString)):
			#cmd=BlockCommand(cmdString)
		elif ( "()" in cmdString or "function " in cmdString): 
			cmd=BashFunction(cmdString.replace("function","").replace("(","").replace(")",""))
			return cmd
		else:
			for x in self.complexWords:
				if x in cmdString:
					cmd=CompoundCommand(cmdString)
					return cmd
			for x in self.usualCommands:
				if cmdString.startswith(x) :
					cmd=UsualCommand(cmdString)
					return cmd
			for x in self.shellbuiltInWords:
				if cmdString.startswith(x) :
					cmd=BuiltinCommand(cmdString)
					return cmd
			if (cmd is None):
				cmd=BashCommand(cmdString)
				return cmd
			
		
				
				
	
class BashCommand:
	def __init__(self, cmdString):
		self.cmd=cmdString
		self.shape="box"
		self.cmdType="Other"
	def printGraph(self, dot):
		if ("FUNCTION" in self.cmdType):
			return dot.node(self.cmdType,self.cmd,shape=self.shape)
		else:
			return None
			
class BlockCommand:
	def __init__(self, cmdString):
		self.cmds=[]
		self.shape="box3d"
		self.cmdType="block"
	def printGraph(self, dot):
		if ("FUNCTION" in self.cmdType):
			return dot.node(self.cmdType,self.cmds[0],shape=self.shape)
		else:
			return None	

		
class BuiltinCommand (BashCommand):
	#builtInWords=self.shellbuiltInWords.split(",")
	def __init__(self, cmdString):
		super(BuiltinCommand, self).__init__(cmdString)
		self.shape="box"
		self.cmdType="BUILTIN"
	def isBuiltin():
		return True;

class UsualCommand (BashCommand):
	#builtInWords=self.usualCommands.split(",")
	def __init__(self, cmdString):
		super(UsualCommand, self).__init__(cmdString)
		self.cmdType="USUAL"
		self.shape="box"
	def isBuiltin():
		return false
		
class PipelineCommand (BashCommand):
	def __init__(self, cmdString):
		super(PipelineCommand, self).__init__(cmdString)
		self.cmdType="PIPELINE"
		self.shape="cds"
		self.leftCmd=cmdString
		self.rightCmd=cmdString
		
class ListCommand (BashCommand):
	def __init__(self, cmdString):
		super(ListCommand, self).__init__(cmdString)
		self.cmdType="LIST"
		#self.cmdList.add(cmdString.split("&&,&,;,||,"))
		self.shape="hexagon"
		if ( ("&&" in cmdString) or ("&" in cmdString)): 
			self.cmd="AND"
		elif ("||" in cmdString):
			self.cmd="OR"
		
class CompoundCommand (BlockCommand):
	def __init__(self, cmdString):
		super(CompoundCommand, self).__init__(cmdString)
		self.cmdType="COMPOUND"
		if ("if" in cmdString or "then" in cmdString or "fi" in cmdString or "else" in cmdString ):
			self.cmds.append("IF-ELSE")
			self.shape="diamond"
		else:
			self.cmds.append("LOOP")
			self.shape="box3d"
	def findCmdType(self):
		''' 
		 for command
		 while, do while loop commands
		 if then elif command
		 do done command
		 sub-shell or execute commands
		 {} - run a s group command
		 (()) and [[]] expressions		
		'''

class BashFunction (BlockCommand):
	def __init__(self, cmdString):
		super(BashFunction, self).__init__(cmdString)
		self.cmds.append(cmdString)
		self.cmdType="FUNCTION"
		self.shape="ellipse"
		if "}" in cmdString :
			self.cmdType="FUNCTION - END"
		else:
			self.cmdType="FUNCTION - START"
		self.commandsInBlock=[]
	


#for x in builtInWords:
	#print(x)
	
if __name__ == "__main__":
	lines = list(open(sys.argv[1])) 
	dot=Digraph(comment="Shell script analysis")
	precmd=None
	for line in lines:
			bparser = BashParser()
			if ((line.strip() is not None) and (line.strip().startswith("#")==False) and line.strip() !=''):
				cmd=bparser.parse(line)
				dotNode=cmd.printGraph(dot)
				if ((precmd is not None) and (dotNode is not None)):	
					if (isinstance(cmd,BlockCommand)):
						dot.edge(precmd.cmds[0],cmd.cmds[0],"Next")
						precmd=cmd
						print("[*] " + line.strip() + "=>" + cmd.cmds[0])
				#else:
				#	dot.edge(precmd.cmd,cmd.cmds[0],"Next")
				#	precmd=cmd
				#	print("[*] " + line.strip() + "=>" + cmds.cmds[0])
	dot.render("siva.gv", view=True)
		
		#if not line.trim().startswith(pattern) for pattern in builtInWords
		


