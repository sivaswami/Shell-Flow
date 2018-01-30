#!/usr/bin/python
import sys
from graphviz import Digraph
#--------------------------------------
# Just started working on this. Any idea of parsersfor shell are welcome
#-----------------------------------------
shellbuiltInWords="alias,bg,bind,break,builtin,caller,cd,command,compgen,complete,compopt,continue,declare,dirs,disown,echo,enable,eval,exec,exit,export,false,fc,fg,getopts,hash,help,history,jobs,kill,let,local,logout,mapfile,popd,printf,pushd,pwd,read,readarray,readonly,return,set,shift,shopt,source,suspend,test,times,trap,true,type,typeset,ulimit,umask,unalias,unset,wait"
builtInWords=shellbuiltInWords.split(",")
#for x in builtInWords:
    #print(x)
lines = list(open(sys.argv[1]))
dot=Digraph(comment="Shell script analysis")
for line in lines:
    if "function" in line.strip():
    if line.contains("{"
        if not line.strip().startswith('#'):
            line=line.replace("function","")
            line=line.replace("(","")
            line=line.replace(")","")
            dot.node(line.strip(),"Function:"+line.strip())
dot.render("siva.gv", view=True)

    #if not line.trim().startswith(pattern) for pattern in builtInWords




