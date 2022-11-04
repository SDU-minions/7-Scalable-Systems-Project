from pyspark import SparkConf, SparkContext
import locale
locale.getdefaultlocale()
locale.getpreferredencoding()

conf = SparkConf().set('spark.executor.cores', 1).set('spark.cores.max',1).set('spark.executor.memory', '1g').set('spark.driver.host', '127.0.0.1')
sc = SparkContext(master='local', appName='pyspark-local', conf=conf)

# Lecture 04 - ClusterPySpark
file = './app/alice-in-wonderland.txt'
txtFile = sc.textFile(file)
all_word = txtFile.flatMap(lambda line: line.split())
word_map = all_word.map(lambda word: (word, 1))
word_reduce = word_map.reduceByKey(lambda s, t: s+t)
select_words = lambda s : s[1] > 400
top_words = word_reduce.filter(select_words).sortBy(lambda s: s[1])
print(top_words.collect())