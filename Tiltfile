allow_k8s_contexts('local')
docker_prune_settings(num_builds=1, keep_recent=1)

aissemble_version = '1.10.0'

build_args = { 'DOCKER_BASELINE_REPO_ID': 'ghcr.io/',
               'VERSION_AISSEMBLE': aissemble_version}

# Add deployment resources here
# pyspark-pipeline-compiler
local_resource(
    name='compile-pyspark-pipeline',
    cmd='cd pyspark-demo-pipelines/pyspark-pipeline && poetry run behave tests/features && poetry build && cd - && \
    cp -r pyspark-demo-pipelines/pyspark-pipeline/dist/* pyspark-demo-docker/pyspark-demo-spark-worker-docker/target/dockerbuild/pyspark-pipeline && \
    cp pyspark-demo-pipelines/pyspark-pipeline/dist/requirements.txt pyspark-demo-docker/pyspark-demo-spark-worker-docker/target/dockerbuild/requirements/pyspark-pipeline',
    deps=['pyspark-demo-pipelines/pyspark-pipeline'],
    auto_init=False,
    ignore=['**/dist/']
)

k8s_kind('SparkApplication', image_json_path='{.spec.image}')


yaml = local('helm template oci://ghcr.io/boozallen/aissemble-spark-application-chart --version %s --values pyspark-demo-pipelines/pyspark-pipeline/src/pyspark_pipeline/resources/apps/pyspark-pipeline-base-values.yaml,pyspark-demo-pipelines/pyspark-pipeline/src/pyspark_pipeline/resources/apps/pyspark-pipeline-dev-values.yaml' % aissemble_version)
k8s_yaml(yaml)
k8s_resource('pyspark-pipeline', port_forwards=[port_forward(4747, 4747, 'debug')], auto_init=False, trigger_mode=TRIGGER_MODE_MANUAL)

# spark-worker-image
docker_build(
    ref='pyspark-demo-spark-worker-docker',
    context='pyspark-demo-docker/pyspark-demo-spark-worker-docker',
    build_args=build_args,
    extra_tag='pyspark-demo-spark-worker-docker:latest',
    dockerfile='pyspark-demo-docker/pyspark-demo-spark-worker-docker/src/main/resources/docker/Dockerfile'
)

k8s_yaml('pyspark-demo-deploy/src/main/resources/apps/spark-worker-image/spark-worker-image.yaml')


yaml = helm(
   'pyspark-demo-deploy/src/main/resources/apps/spark-operator',
   name='spark-operator',
   values=['pyspark-demo-deploy/src/main/resources/apps/spark-operator/values.yaml',
       'pyspark-demo-deploy/src/main/resources/apps/spark-operator/values-dev.yaml']
)
k8s_yaml(yaml)
yaml = helm(
   'pyspark-demo-deploy/src/main/resources/apps/spark-infrastructure',
   name='spark-infrastructure',
   values=['pyspark-demo-deploy/src/main/resources/apps/spark-infrastructure/values.yaml',
       'pyspark-demo-deploy/src/main/resources/apps/spark-infrastructure/values-dev.yaml']
)
k8s_yaml(yaml)

yaml = helm(
   'pyspark-demo-deploy/src/main/resources/apps/s3-local',
   name='s3-local',
   values=['pyspark-demo-deploy/src/main/resources/apps/s3-local/values.yaml',
       'pyspark-demo-deploy/src/main/resources/apps/s3-local/values-dev.yaml']
)
k8s_yaml(yaml)
yaml = helm(
   'pyspark-demo-deploy/src/main/resources/apps/pipeline-invocation-service',
   name='pipeline-invocation-service',
   values=['pyspark-demo-deploy/src/main/resources/apps/pipeline-invocation-service/values.yaml',
       'pyspark-demo-deploy/src/main/resources/apps/pipeline-invocation-service/values-dev.yaml']
)
k8s_yaml(yaml)

yaml = helm(
   'pyspark-demo-deploy/src/main/resources/apps/kafka-cluster',
   name='kafka-cluster',
   values=['pyspark-demo-deploy/src/main/resources/apps/kafka-cluster/values.yaml',
       'pyspark-demo-deploy/src/main/resources/apps/kafka-cluster/values-dev.yaml']
)
k8s_yaml(yaml)
# policy-decision-point
docker_build(
    ref='pyspark-demo-policy-decision-point-docker',
    context='pyspark-demo-docker/pyspark-demo-policy-decision-point-docker',
    build_args=build_args,
    dockerfile='pyspark-demo-docker/pyspark-demo-policy-decision-point-docker/src/main/resources/docker/Dockerfile'
)

yaml = helm(
   'pyspark-demo-deploy/src/main/resources/apps/policy-decision-point',
   name='policy-decision-point',
   values=['pyspark-demo-deploy/src/main/resources/apps/policy-decision-point/values.yaml',
       'pyspark-demo-deploy/src/main/resources/apps/policy-decision-point/values-dev.yaml']
)
k8s_yaml(yaml)