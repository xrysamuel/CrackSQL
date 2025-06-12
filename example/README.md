# CrackSQL 复现实验

## 开始

下载数据集

BIRD:


```bash
mkdir downloads
wget https://bird-bench.oss-cn-beijing.aliyuncs.com/dev.zip -O downloads/BIRD-dev.zip
unzip downloads/BIRD-dev.zip -d downloads/BIRD-dev
rm -f downloads/BIRD-dev.zip
unzip downloads/BIRD-dev/dev_20240627/dev_databases.zip -d downloads/BIRD-dev/dev_20240627/dev_databases
rm -f downloads/BIRD-dev/dev_20240627/dev_databases.zip
```

```bash
huggingface-cli login
```

```python
from huggingface_hub import hf_hub_download
hf_hub_download(repo_id="Exploration-Lab/BookSQL", filename="BookSQL/accounting.sqlite", local_dir="downloads", repo_type="dataset")
```