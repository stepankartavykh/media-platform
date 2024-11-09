#!/bin/bash

echo "$PWD"

#export SPARK_HOME=/home/skartavykh/spark-3.5.2-bin-hadoop3

#$SPARK_HOME/bin/spark-submit ./server_count.py \
#	--num_output_partitions 1 --log_level WARN \
#	./input/test_warc.txt servernames

#./cc-pyspark/get-data.sh


"$SPARK_HOME"/bin/spark-submit --packages org.apache.hadoop:hadoop-aws:3.3.2 ./cc_index_word_count.py --input_base_url s3://commoncrawl/
    --query "SELECT url, warc_filename, warc_record_offset, warc_record_length, content_charset FROM ccindex WHERE crawl = 'CC-MAIN-2020-24' AND subset = 'warc' AND url_host_tld = 'is' LIMIT 10" s3a://commoncrawl/cc-index/table/cc-main/warc/ myccindexwordcountoutput --num_output_partitions 1 --output_format json