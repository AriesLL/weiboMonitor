## Crawl 微博 starRank 数据

#### 中国时间 每天早上10AM 更新，请设置crontab 在当地时区对应时间过5分钟 抓取数据


#### User Guide:

pick up a WORK_DIR on your computer, 
```console
# copy scripts
cp -rf ./starRank $WORK_DIR/scripts

#make them executable
chmod a+x $WORK_DIR/scripts/*.sh

#run starRankPipeline.sh, which call starRankGet.sh, starRankCallPython.sh and starRankCollect.sh
$WORK_DIR/scripts/starRankPipeline.sh
```

Then two new directories are generated:

$WORK_DIR/starRankRawCSV, here the raw data and parsed csv files for each rocket girl are.

$WORK_DIR/starRankCollect, here are the collected csv files, one for simplied version, one for full version





