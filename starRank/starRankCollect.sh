# source tool and working dir
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
echo "$SCRIPT_DIR"
source ${SCRIPT_DIR}/global.sh

#echo "============= starRankData is $starRankData ========="
declare -A players
declare -A playersName

# http://chart.weibo.com/?rank_type=6  
# copy link address, can give you weibo id
players=( ["wxy"]="5796662600" ["mmq"]="5813256522" ["ycy"]="5644764907" ["daj"]="5542384916" ["yamy"]="5957839152" ["lmy"]="5541182601" ["lzt"]="6502204514" ["zn"]="2335410541" ["fj"]="5473085545" ["xmj"]="5873220619" ["sunnee"]="2485664410"  )
playersName=( ["wxy"]="吴宣仪" ["mmq"]="孟美岐" ["ycy"]="杨超越" ["daj"]="段奥娟" ["yamy"]="yamy" ["lmy"]="赖美云" ["lzt"]="李紫婷" ["zn"]="紫宁" ["fj"]="傅菁" ["xmj"]="徐梦洁" ["lry"]="刘人语" ["lzx"]="李子璇" ["gqz"]="高秋梓" ["sunnee"]="sunnee" ["wj"]="王菊" ["qyd"]="戚砚笛" ["gyx"]="高颖浠" ["xjy"]="许靖韵" ["lxy"]="吕小>雨" ["cyh"]="陈意涵" ["qdy"]="强东玥" ["wyx"]="吴映香" )

cur_month=`TZ=Asia/Shanghai date +%m`
cur_date=`TZ=Asia/Shanghai date +%d`
cur_year=`TZ=Asia/Shanghai date +%y`

mergeFile0="20${cur_year}_${cur_month}_${cur_date}_简版.txt"
mergeFile1="20${cur_year}_${cur_month}_${cur_date}_全版.txt"

if [ ! -d $starRankDir  ]; then
	mkdir -p $starRankDir;
fi
echo "昵称,粉丝数,总分,总排行,阅读（30分）,互动（30分）,社会影响力（20分）,爱慕值（20分）" > ${starRankDir}/${mergeFile0}

echo "昵称,日期,粉丝数,总分,总排行,分（阅读）,排名（阅读）,阅读数,30天微博数,7天微博数,昨日微博数,分（互动）,排名（互动）,互动数,微博互动,评论互动,故事互动,分（社会影响力）,排名（社会影响力）,提及微博阅读数,搜索量,分（爱慕）,排名（爱慕）,爱慕值,送花人数,送花次数" > ${starRankDir}/${mergeFile1}


for i in "${!players[@]}"; do
player=$i
weiboID=${players[$player]}
playerChineseName=${playersName[$i]}
outputArgu="${starRankData}/weibo/${player}/csv/${playerChineseName}_20${cur_year}_${cur_month}_${cur_date}" 
#echo ${outputArgu}
mode0File="${outputArgu}_mode_0_utf8.csv"
mode1File="${outputArgu}_mode_1_utf8.csv"
#echo $mode0File
#echo $mode1File
echo `tail -1 $mode0File` >> ${starRankDir}/${mergeFile0}
echo `tail -1 $mode1File` >> ${starRankDir}/${mergeFile1}
done
