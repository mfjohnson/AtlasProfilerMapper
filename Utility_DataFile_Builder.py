from pyspark import HiveContext
from pyspark import SQLContext
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark import *
from faker import Factory
from collections import defaultdict
from random import random, randrange,randint
import uuid
import datetime


#----------------------------
sc = SparkContext(appName = "WriteRDD")
hc = HiveContext(sc)
sqlContext = SQLContext(sc)
#----------------------------
rowCountPerGroup = 10
fake = Factory.create()



#----------------------------
def random_date(start, end):
    secRange = randrange(0, (end - start).total_seconds(),1)
    d = start + datetime.timedelta(secRange)
    return(unicode(d))



def buildCustomerRDD(i) :
    d1 = datetime.date(randrange(2008,2016,1),randrange(1,12,1),1)
    d2 = datetime.date(2016,12,31)


    r = (i, str(uuid.uuid4()), fake.company(), fake.name(), fake.email(), fake.address(),randrange(1990,2016,1), randrange(1000,10000,1000),unicode(d1))

    return(r);

#---------------- Begin Main Processing
a = sc.parallelize(range(1,100))
colNames = ["transgroup","CustomerId","CompanyName","contactname","EMAIL","Address","CustomerSince","AnnualSales","LastOrderDate"]
rows = a.map(lambda i: buildCustomerRDD(i) )
b = hc.inferSchema(rows)
b = reduce(lambda b, idx: b.withColumnRenamed(b.schema.names[idx],colNames[idx]),xrange(len(b.schema.names)), b)


b.printSchema()
b.show()

b.write.format("orc").mode("overwrite").saveAsTable("CustomerInfo")
#z = b.write.saveAsTable("CustomerInfo")
#print z