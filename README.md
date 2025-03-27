# S3-RealSync-Cloud-Native-Monitor. Project
This project monitors an S3 bucket (`salmon-monitoring-data`) using Python, Prometheus, and Grafana on an AWS EC2 instance. It tracks the number of files in the bucket, exposes metrics via a Python script, scrapes them with Prometheus, and visualizes them in Grafana.

## Features
- Counts files in the S3 bucket every 30 seconds.
- Exposes metrics at `http://3.83.161.202:8000`.
- Prometheus scrapes metrics and serves them at `http://3.83.161.202:9090`.
- Grafana displays a live dashboard at `http://3.83.161.202:3000`.

## Files
- `s3_monitor.py`: Python script that queries S3 and serves metrics via Prometheus client.
- `prometheus.yml`: Configuration file for Prometheus to scrape metrics from `localhost:8000` and itself.

## How It Works
1. **S3 Bucket**: The `salmon-monitoring-data` bucket holds files to monitor (e.g., `test.txt`).
2. **Python Script**: `s3_monitor.py` uses `boto3` to count files in S3 every 30 seconds and exposes the count as a Prometheus metric (`s3_file_count`) on port 8000.
3. **Prometheus**: Scrapes the metric from `localhost:8000` every minute (configurable in `prometheus.yml`) and stores time-series data, accessible at port 9090.
4. **Grafana**: Pulls data from Prometheus and displays it in a dashboard on port 3000, showing the file count over time.
5. **EC2**: Runs all components on a single Ubuntu instance (`3.83.161.202`), with ports 8000, 9090, and 3000 opened via security group rules.

## Setup Instructions
Follow these steps to replicate this project:

### 1. Launch EC2 Instance
- AWS Console → EC2 → Launch instance:
  - Name: `MonitoringServer`.
  - AMI: Ubuntu Server 22.04 LTS.
  - Instance type: `t2.micro` (free tier).
  - Key pair: Create `monitoring-key.pem`, download to `~/cloud-monitoring/`.
  - Security group: Allow SSH (22), TCP 8000, 9090, 3000 from Anywhere (0.0.0.0/0).
- Note the public IP (e.g., `3.83.161.202`).

### 2. Configure AWS Credentials
- Create an IAM user (`Salmon`) with `AmazonS3FullAccess`.
- Run `aws configure` on your Mac and EC2:
  - Access Key ID and Secret Access Key from IAM.
  - Region: `us-east-1`.
  - Output: `json`.

### 3. Set Up S3 Bucket
- AWS Console → S3 → Create bucket: `salmon-monitoring-data`.
- Upload a test file (e.g., `test.txt`).

### 4. Write and Test Python Script
- On your Mac in `~/cloud-monitoring/`:
  ```python
  import boto3
  from prometheus_client import start_http_server, Gauge
  import time

  s3 = boto3.client('s3')
  file_count = Gauge('s3_file_count', 'Number of files in S3 bucket')

  def update_s3_metrics(bucket_name):
      response = s3.list_objects_v2(Bucket=bucket_name)
      count = len(response.get('Contents', [])) if 'Contents' in response else 0
      file_count.set(count)
Your README looks solid so far—nice and concise! It’s 7:16 PM PDT on March 26, 2025, and I’ll expand it to explain how your S3 monitoring project works, how to set it up, and the steps you followed. Since you’ve been working through this with me (setting up EC2, S3, Prometheus, Grafana, etc.), I’ll weave in those details to make it a complete guide. You can add this to your README.md via the GitHub website or Terminal—your call! Here’s the enhanced version:

markdown

Collapse

Wrap

Copy
# S3 Monitoring Project
This project monitors an S3 bucket (`salmon-monitoring-data`) using Python, Prometheus, and Grafana on an AWS EC2 instance. It tracks the number of files in the bucket, exposes metrics via a Python script, scrapes them with Prometheus, and visualizes them in Grafana.

## Features
- Counts files in the S3 bucket every 30 seconds.
- Exposes metrics at `http://3.83.161.202:8000`.
- Prometheus scrapes metrics and serves them at `http://3.83.161.202:9090`.
- Grafana displays a live dashboard at `http://3.83.161.202:3000`.

## Files
- `s3_monitor.py`: Python script that queries S3 and serves metrics via Prometheus client.
- `prometheus.yml`: Configuration file for Prometheus to scrape metrics from `localhost:8000` and itself.

## How It Works
1. **S3 Bucket**: The `salmon-monitoring-data` bucket holds files to monitor (e.g., `test.txt`).
2. **Python Script**: `s3_monitor.py` uses `boto3` to count files in S3 every 30 seconds and exposes the count as a Prometheus metric (`s3_file_count`) on port 8000.
3. **Prometheus**: Scrapes the metric from `localhost:8000` every minute (configurable in `prometheus.yml`) and stores time-series data, accessible at port 9090.
4. **Grafana**: Pulls data from Prometheus and displays it in a dashboard on port 3000, showing the file count over time.
5. **EC2**: Runs all components on a single Ubuntu instance (`3.83.161.202`), with ports 8000, 9090, and 3000 opened via security group rules.

## Setup Instructions
Follow these steps to replicate this project:

### 1. Launch EC2 Instance
- AWS Console → EC2 → Launch instance:
  - Name: `MonitoringServer`.
  - AMI: Ubuntu Server 22.04 LTS.
  - Instance type: `t2.micro` (free tier).
  - Key pair: Create `monitoring-key.pem`, download to `~/cloud-monitoring/`.
  - Security group: Allow SSH (22), TCP 8000, 9090, 3000 from Anywhere (0.0.0.0/0).
- Note the public IP (e.g., `3.83.161.202`).

### 2. Configure AWS Credentials
- Create an IAM user (`Salmon`) with `AmazonS3FullAccess`.
- Run `aws configure` on your Mac and EC2:
  - Access Key ID and Secret Access Key from IAM.
  - Region: `us-east-1`.
  - Output: `json`.

### 3. Set Up S3 Bucket
- AWS Console → S3 → Create bucket: `salmon-monitoring-data`.
- Upload a test file (e.g., `test.txt`).

### 4. Write and Test Python Script
- On your Mac in `~/cloud-monitoring/`:
  ```python
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
      bucket = 'salmon-monitoring-data'
      while True:
          update_s3_metrics(bucket)
          time.sleep(30)
Save as s3_monitor.py (plain text, not .rtf).
Test locally: python3 s3_monitor.py, check http://localhost:8000.
5. Deploy to EC2
SSH in: ssh -i ~/cloud-monitoring/monitoring-key.pem ubuntu@3.83.161.202.
Install dependencies:
text

Collapse

Wrap

Copy
sudo apt update
sudo apt install -y python3-pip awscli
pip3 install boto3 prometheus_client
Upload script: scp -i ~/cloud-monitoring/monitoring-key.pem ~/cloud-monitoring/s3_monitor.py ubuntu@3.83.161.202:~/.
Run: nohup python3 s3_monitor.py &.
6. Install and Configure Prometheus
Install:
text

Collapse

Wrap

Copy
sudo apt install -y prometheus
Edit /etc/prometheus/prometheus.yml:
yaml

Collapse

Wrap

Copy
scrape_configs:
  - job_name: 's3_metrics'
    static_configs:
      - targets: ['localhost:8000']
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
Upload: scp -i ~/cloud-monitoring/monitoring-key.pem ~/cloud-monitoring/prometheus.yml ubuntu@3.83.161.202:~/, then sudo mv ~/prometheus.yml /etc/prometheus/.
Restart: sudo systemctl restart prometheus.
7. Install and Set Up Grafana
Install:
text

Collapse

Wrap

Copy
sudo apt install -y grafana
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
Access http://3.83.161.202:3000, log in (admin/admin, set password to password123).
Add data source:
Type: Prometheus.
URL: http://localhost:9090.
Save & Test.
Create dashboard:
New dashboard → Add panel.
Query: s3_file_count.
Title: “S3 File Count.”
Apply and save.
8. Verify
Upload another file to S3—Grafana should update to “2” within 30 seconds.
Steps Followed
Launched EC2 with Ubuntu and opened ports.
Configured AWS CLI with IAM user Salmon.
Created S3 bucket salmon-monitoring-data and uploaded test.txt.
Wrote s3_monitor.py, tested locally, fixed file format issues (RTF to .py).
Deployed to EC2, added AWS credentials, ran script in background.
Installed Prometheus, configured to scrape localhost:8000, fixed targets URL (/classic/targets).
Installed Grafana, connected to Prometheus, built a dashboard showing s3_file_count.




