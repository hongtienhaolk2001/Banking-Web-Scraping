# Bigdata_-Application_at_Scale

Tạo SparkSession

```python
from pyspark.sql import SparkSession
my_spark = SparkSession.builder.getOrCreate()
```
attribute `catalog` danh sách tất cả các dữ liêu bên trong cluster
method `listTables` trong `catalog` trả về tất cả các table như một list

```python
spark.catalog.listTables()
```
