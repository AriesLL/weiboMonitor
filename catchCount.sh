folder="FillMe"
#name
input=$1
pythonTool="FillMe/bin/python"
$pythonTool ${folder}/listCount_new.py ${folder}/${input}/${input}.txt ${folder}/counter/log_${input}.txt
