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
    exit()
    ```

### 配置数据库 Docker 环境

首先确保 Docker daemon 正在运行

拉取 MySQL 8.4.0 镜像

```bash
docker pull mysql:8.4.0
```

后台启动容器

```bash
docker run -d \
    --name mysql-container \
    -p 13306:3306 \
    -e MYSQL_ROOT_PASSWORD=mysql_root_password \
    mysql:8.4.0
```

> 测试环境，方便起见，密码全部编码在命令和代码中，实际工作中不要这样干

拉取 PostgreSQL 14.18 镜像

```bash
docker pull postgres:14.18
```

后台启动容器

```bash
docker run -d \
  --name pg-container \
  -p 15432:5432 \
  -e POSTGRES_PASSWORD=postgres_password \
  postgres:14.18
```

安装 MySQL 客户端和 PostgreSQL 客户端

```bash
sudo apt update
sudo apt install default-mysql-client postgresql-client
```

验证安装和容器启动情况，尝试连接到容器

```bash
mysql -h 127.0.0.1 -P 13306 -u root -pmysql_root_password -e "SHOW DATABASES; SELECT DATABASE();"
PGPASSWORD='postgres_password' psql -h 127.0.0.1 -p 15432 -U postgres -d postgres -c "SELECT version(); SELECT current_database();"
```

### 查看并导入数据

需要安装两个工具从 sqlite3 数据库迁移到 MySQL 数据库和 Postgresql 数据库

```bash
pip install sqlite3-to-mysql # 之前应该已经安装过了
sudo apt install pgloader
```
