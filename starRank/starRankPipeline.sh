# source tool and working dir
SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
echo "$SCRIPT_DIR"
source ${SCRIPT_DIR}/global.sh

sh ${curDir}/starRankGet.sh;
sh ${curDir}/starRankCallPython.sh;
sh ${curDir}/starRankCollect.sh
