from pyspark.sql import SparkSession

logFile = "/home/skartavykh/MyProjects/media-bot/storage/2024-06-14_18-47-55-687057_everything_feed.json"
spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
logData = spark.read.text(logFile).cache()

numAs = logData.filter(logData.value.contains('a')).count()
numBs = logData.filter(logData.value.contains('b')).count()

print("Lines with a: %i, lines with b: %i" % (numAs, numBs))

spark.stop()
