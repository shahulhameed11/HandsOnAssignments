# -*- coding: utf-8 -*-
"""Linear_Regression_Pysaprk.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SatiP1_8cBtWfnErRYxQVTHwTFqG5uzA

# Goal: To predict yearly amount spent by customers using Linear Regression in PySpark

## install pyspark
"""

!pip install pyspark

"""## importing necessary pyspark libraries"""

from pyspark.sql import SparkSession

spark =SparkSession.builder.appName('lr_ex').getOrCreate()

from pyspark.ml.regression import LinearRegression

"""## loading the dataset"""

from google.colab import files
import io
uploaded = files.upload()

df_customers=spark.read.csv('Ecommerce_Customers.csv',inferSchema=True,header=True)

df_customers.printSchema()

df_customers.show(5)

"""## Converting the necessary features into vectors accepted by the pyspark mlib"""

from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler

df_customers.columns

"""## Here email, address, avatar are categorical variables which infer nothing. So, selecting only the numerical columns for the prediction

## As said earlier converting the numerical columns into a single vector column
"""

assembler=VectorAssembler(inputCols=['Avg Session Length','Time on App','Time on Website','Length of Membership']
                          ,outputCol='features')

output=assembler.transform(df_customers)

output.show(2)

"""## Yearly Amount Spent column is the target column to predict"""

final_data = output.select('features','Yearly Amount Spent')

final_data.show(5)

"""## Splitting the dataset into 70:30 ratio"""

train_data, test_data = final_data.randomSplit([0.7,0.3])

train_data.describe().show()

test_data.describe().show()

"""## Specifying the target column for Linear Regression model"""

lr=LinearRegression(labelCol='Yearly Amount Spent')

lr_model=lr.fit(train_data)

test_results= lr_model.evaluate(test_data)

"""## residuals is the difference between the actual and predicted label from the test data"""

test_results.residuals.show()

test_results.rootMeanSquaredError

test_results.r2

"""## predicting the test data by selecting only the features"""

unlabeled_data=test_data.select('features')

predictions = lr_model.transform(unlabeled_data)

predictions.show()

test_data.show()

"""## combining the predictions and test_data dataframes on features column to compare the predictions done by the model with the actual values"""

df_result = test_data.join(predictions, ['features'])
df_result = df_result.withColumnRenamed("prediction", "prediction_by_model")\
.withColumnRenamed("Yearly Amount Spent", "actual_values")
df_result.show()

