#!/bin/bash

TEST_TIME_SECONDS=$1
TEST_NAME=$2

STAT_INTERVAL_5S=$(($TEST_TIME_SECONDS/5))

rm -f *_$TEST_NAME
top -b -n $STAT_INTERVAL_5S -d 5 >top_$TEST_NAME &
timeout $TEST_TIME_SECONDS mongostat >ms_$TEST_NAME &
timeout $TEST_TIME_SECONDS iostat -x 5 | grep sda >iostat_$TEST_NAME &
sar 5 $STAT_INTERVAL_5S -o sar_$TEST_NAME > /dev/null 2>&1 &
timeout $TEST_TIME_SECONDS tail -f /var/log/voss-deviceapi/db.log | grep -vi schedul >db_queries_$TEST_NAME &

sleep $TEST_TIME_SECONDS
sleep 5
./report_stats.py -t $TEST_NAME
