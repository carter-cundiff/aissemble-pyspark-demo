# aiSSEMBLE PySpark Demo

## Environment Configuration

Please consult our [Configuring Your Environment guidance](https://boozallen.github.io/aissemble/aissemble/current/configurations.html).

## Running The Pipeline
This project was created from the [aiSSEMBLE archetype](https://boozallen.github.io/aissemble/aissemble/current/archetype.html) 
using the following command:
```
mvn archetype:generate -DarchetypeGroupId=com.boozallen.aissemble \
  -DarchetypeArtifactId=foundation-archetype \
  -DarchetypeVersion=1.10.0 \
  -DgroupId=org.demo \
  -DartifactId=pyspark-demo \
  -DprojectGitUrl=https://github.com/carter-cundiff/aissemble-pyspark-demo.git \
  -DprojectName=PysparkDemo
```

The following [pipeline was added](https://boozallen.github.io/aissemble/aissemble/current/add-pipelines-to-build.html) to generate out the desired functionality (ref: [Pipeline Metamodel](https://boozallen.github.io/aissemble/aissemble/current/pipeline-metamodel.html)):
```
pyspark-demo-pipeline-models/src/main/resources/pipelines/PysparkPipeline.json

{
  "name": "PysparkPipeline",
  "package": "org.demo",
  "type": {
    "name": "data-flow",
    "implementation": "data-delivery-pyspark"
  },
  "dataLineage": false,
  "steps": [
    {
      "name": "Ingest",
      "type": "synchronous",
      "persist" : {
        "type": "delta-lake"
      },
      "provenance": {
        "enabled": false
      }
    },
    {
      "name": "Transform",
      "type": "synchronous",
      "provenance": {
        "enabled": false
      }
    }
  ]
}
```

The project is built using Maven:
```
mvn clean install
```

The business logic for the pipeline lives in the following files:
- [pyspark-demo-docker/pyspark-demo-spark-worker-docker/src/main/resources/docker/Dockerfile](https://github.com/carter-cundiff/aissemble-pyspark-demo/blob/main/pyspark-demo-docker/pyspark-demo-spark-worker-docker/src/main/resources/docker/Dockerfile)
- [pyspark-demo-pipelines/pyspark-pipeline/src/pyspark_pipeline/step/ingest.py](https://github.com/carter-cundiff/aissemble-pyspark-demo/blob/main/pyspark-demo-pipelines/pyspark-pipeline/src/pyspark_pipeline/step/ingest.py)
- [pyspark-demo-pipelines/pyspark-pipeline/src/pyspark_pipeline/step/transform.py](https://github.com/carter-cundiff/aissemble-pyspark-demo/blob/main/pyspark-demo-pipelines/pyspark-pipeline/src/pyspark_pipeline/step/transform.py)


The project is deployed locally using Tilt:
```
tilt up
```

Select the `Trigger update` button for the `pyspark-pipeline` resource within the Tilt UI to run the pipeline
and view the logs.

After the pipeline has completed, the `.parquet` Delta Lake files saved to the local s3 resource can be viewed with the following:
```
awslocal s3 ls s3://spark-infrastructure/delta_images/
```

Additionally, any `.jpg` files created from the Delta Lake dataframe can be copied out of the pod with the following:
```
kubectl cp pyspark-pipeline-driver:/opt/spark/work-dir/output_images/{IMAGE_NAME}.jpg ./image.jpg
```

To tear down the project with Tilt, run the following:
```
tilt down
```

## Additional Resources
[aiSSEMBLE Github Repo](https://github.com/boozallen/aissemble)

[aiSSEMBLE User Manual](https://boozallen.github.io/aissemble/aissemble/current/index.html)