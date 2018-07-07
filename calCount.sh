folder="FillMe"
input=$1
pythonTool="FillMe/bin/python"
study=${folder}/counter/log_${input}.txt
pre=`cat $study| tail -2| head -1| cut -d',' -f2`
cur=`cat $study| tail -1| head -1| cut -d',' -f2`
timeTag=`cat $study| tail -1| head -1| cut -d',' -f1`
echo "$timeTag , $((cur-pre)) , $pre , $cur " >> ${folder}/counter/stat_${input}.txt
