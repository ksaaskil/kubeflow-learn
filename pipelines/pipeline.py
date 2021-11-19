import kfp
from kfp.v2 import dsl
from kfp.v2.dsl import component
from kfp.v2.dsl import (
    Input,
    Output,
    Artifact,
    Dataset,
)

"""
import glob
import pandas as pd
import tarfile
import urllib.request

def download_and_merge_csv(url: str, output_csv: str):
  with urllib.request.urlopen(url) as res:
    tarfile.open(fileobj=res, mode="r|gz").extractall('data')
  df = pd.concat(
      [pd.read_csv(csv_file, header=None) 
       for csv_file in glob.glob('data/*.csv')])
  df.to_csv(output_csv, index=False, header=False)

"""

@component(
    packages_to_install=['pandas==1.1.4'],
    output_component_file='component.yaml'
)
def merge_csv(tar_data: Input[Artifact], output_csv: Output[Dataset]):
  import glob
  import pandas as pd
  import tarfile

  tarfile.open(name=tar_data.path, mode="r|gz").extractall('data')
  df = pd.concat(
      [pd.read_csv(csv_file, header=None) 
       for csv_file in glob.glob('data/*.csv')])
  df.to_csv(output_csv.path, index=False, header=False)

web_downloader_op = kfp.components.load_component_from_url(
    'https://raw.githubusercontent.com/kubeflow/pipelines/master/components/web/Download/component-sdk-v2.yaml')

# Define a pipeline and create a task from a component:
@dsl.pipeline(
    name='my-pipeline',
    # You can optionally specify your own pipeline_root
    # pipeline_root='gs://my-pipeline-root/example-pipeline',
)
def my_pipeline(url: str):
  web_downloader_task = web_downloader_op(url=url)
  merge_csv_task = merge_csv(tar_data=web_downloader_task.outputs['data'])

kfp.compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE).compile(
    pipeline_func=my_pipeline,
    package_path='pipeline.yaml')

client = kfp.Client() # change arguments accordingly

client.create_run_from_pipeline_func(
    my_pipeline,
    mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE,
    # You can optionally override your pipeline_root when submitting the run too:
    # pipeline_root='gs://my-pipeline-root/example-pipeline',
    arguments={
        'url': 'https://storage.googleapis.com/ml-pipeline-playground/iris-csv-files.tar.gz'
    }
)
