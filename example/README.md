# CrackSQL 测试

## 开始

### 配置环境

```bash
conda create -n cracksql python=3.10
conda activate cracksql
pip install -r requirements.txt
```

### 下载数据集

BIRD：下载数据集并解压


```bash
mkdir -p downloads
wget https://bird-bench.oss-cn-beijing.aliyuncs.com/dev.zip -O downloads/BIRD-dev.zip
unzip downloads/BIRD-dev.zip -d downloads/BIRD-dev
rm -f downloads/BIRD-dev.zip
unzip downloads/BIRD-dev/dev_20240627/dev_databases.zip -d downloads/BIRD-dev/dev_20240627/dev_databases
rm -f downloads/BIRD-dev/dev_20240627/dev_databases.zip
```

BookSQL：

- 要访问 BookSQL 数据集，你需要先填写一份表格并登录 Hugging Face
    - 先去 [Exploration-Lab/BookSQL - Datasets at Hugging Face](https://huggingface.co/datasets/Exploration-Lab/BookSQL) 填写表单
    - 通过终端登录 Hugging Face。按照终端中的提示完成登录过程。

    ```bash
    huggingface-cli login
    ```
- 登录后，打开 Python 解释器并运行以下命令下载数据集：
    ```python
    from huggingface_hub import hf_hub_download
    hf_hub_download(
        repo_id="Exploration-Lab/BookSQL", 
        filename="BookSQL/accounting.sqlite", local_dir="downloads", 
        repo_type="dataset"
    )
    ```

### 检查 Docker 环境

