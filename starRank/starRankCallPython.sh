# source tool and working dir
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
echo "$SCRIPT_DIR"
source ${SCRIPT_DIR}/global.sh

declare -A players
declare -A playersName

# http://chart.weibo.com/?rank_type=6  
# copy link address, can give you weibo id
players=( ["wxy"]="5796662600" ["mmq"]="5813256522" ["ycy"]="5644764907" ["daj"]="5542384916" ["yamy"]="5957839152" ["lmy"]="5541182601" ["lzt"]="6502204514" ["zn"]="2335410541" ["fj"]="5473085545" ["xmj"]="5873220619" ["sunnee"]="2485664410"  )
playersName=( ["wxy"]="吴宣仪" ["mmq"]="孟美岐" ["ycy"]="杨超越" ["daj"]="段奥娟" ["yamy"]="yamy" ["lmy"]="赖美云" ["lzt"]="李紫婷" ["zn"]="紫宁" ["fj"]="傅菁" ["xmj"]="徐梦洁" ["lry"]="刘人语" ["lzx"]="李子璇" ["gqz"]="高秋梓" ["sunnee"]="sunnee" ["wj"]="王菊" ["qyd"]="戚砚笛" ["gyx"]="高颖浠" ["xjy"]="许靖韵" ["lxy"]="吕小>雨" ["cyh"]="陈意涵" ["qdy"]="强东玥" ["wyx"]="吴映香" )


cur_month=`TZ=Asia/Shanghai date +%m`
cur_date=`TZ=Asia/Shanghai date +%d`
cur_year=`TZ=Asia/Shanghai date +%y`



for i in "${!players[@]}"; do
player=$i
weiboID=${players[$player]}
playerChineseName=${playersName[$i]}
#studyEpoch=`TZ=Asia/Shanghai date -d "2018${studyMonth}${studyDate} 0005" +%s`
#studyEpochMill=$((studyEpoch*1000))
#pageNum="0"
#url="https://m.weibo.cn/p/index?containerid=231343_${weiboID}_6"
#url=`echo "\"$4\""`
#echo $url
#enforce="1"

if [ ! -d "${starRankData}/weibo/${player}/csv/" ]; then
	mkdir -p "${starRankData}/weibo/${player}/csv/";
fi

inputArgu="${starRankData}/weibo/${player}/raw/${playerChineseName}_20${cur_year}_${cur_month}_${cur_date}" 
outputArgu="${starRankData}/weibo/${player}/csv/${playerChineseName}_20${cur_year}_${cur_month}_${cur_date}" 
$pythonTool ${curDir}/starRank.py $inputArgu $outputArgu
	#echo $((pageNum+1))
	#echo "should download!"


done

