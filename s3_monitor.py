import boto3
from prometheus_client import start_http_server, Gauge
import time

s3 = boto3.client('s3')
file_count = Gauge('s3_file_count', 'Number of files in S3 bucket')

def update_s3_metrics(bucket_name):
    response = s3.list_objects_v2(Bucket=bucket_name)
    count = len(response.get('Contents', [])) if 'Contents' in response else 0
    file_count.set(count)

if __name__ == '__main__':
    start_http_server(8000)
    bucket = 'salmon-monitoring-data'  # Replace if your bucket name is different
    while True:
        update_s3_metrics(bucket)
        time.sleep(30)