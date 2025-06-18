# CrackSQL 测试

## 1 配置环境

环境前提：debian / ubuntu，docker

配置 python 环境

```bash
conda create -n cracksql python=3.10
conda activate cracksql
pip install -r requirements.txt
```

安装 MySQL 客户端和 PostgreSQL 客户端

```bash
sudo apt update
sudo apt install default-mysql-client postgresql-client
```

## 2 在 BIRD Critic 数据集上测试

### 2.1 配置集测试环境

下载数据库，并放在指定位置

```bash
mkdir -p downloads
gdown "https://drive.google.com/drive/folders/1nJReLrvZVVrnfgBYwwNEgYvLroPGbcPD" -O downloads/ --folder
unzip downloads/BIRD-CRITIC-DB/mysql_table_dumps.zip -d bird_critic
unzip downloads/BIRD-CRITIC-DB/postgre_table_dumps.zip -d bird_critic
unzip downloads/BIRD-CRITIC-DB/oracle_table_dumps.zip -d bird_critic
unzip downloads/BIRD-CRITIC-DB/mssql_table_dumps.zip -d bird_critic
rm -rf bird_critic/__MACOSX
```

首先确保 Docker daemon 正在运行，然后启动 Docker Compose，请耐心等待

```bash
cd bird_critic
docker compose up --build
```

验证安装和容器启动情况，尝试连接到容器，并检查是否成功导入了 BIRD Critic 的所有数据库

```bash
mysql -h 127.0.0.1 -P 13306 -u root -pmysql_root_password -e "SHOW DATABASES;"
PGPASSWORD='postgres_password' psql -h 127.0.0.1 -p 15432 -U root -d postgres -c "SELECT version(); SELECT datname FROM pg_database;"
```

如果之后要删除环境，运行

```bash
docker compose down -v
```

### 2.2 开始翻译

运行

```bash
python test_cracksql_translate.py -p "BIRD Critic.*"
python test_jooq_translate.py -p ".*"
```

运行完毕之后，在 `output/test_translated_*.json` 查看结果。

### 2.3 准确率测试

运行

```bash
python test_accuracy.py -i "./output/test_translated_craksql.json" -p ".*" > cracksql_result.txt
python test_accuracy.py -i "./output/test_translated_jooq.json" -p "BIRD Critic.*" > jooq_result.txt
```

运行完毕之后，在 `*_result.txt` 查看结果，包含在每个样本测试运行结果（查询语句的返回内容、执行语句之后的数据库内容）及其差异。

### 2.4 ‼️已知问题

实际上，BIRD Critic 数据集本身不保证不同数据库系统的数据库的一致性。

比如在 Postgresql 版本的数据库中有一个表的名字是 `pitstops`，而在 MySQL 版本的数据库中对应表的名字是 `pitStops`。

此外还有很多表中数据的差异。

所以在 BIRD Critic 数据集上测试翻译准确率是不合适的，最后的翻译一致准确率应该是 0%，翻译后的 SQL 语句执行成功率也接近 0%。

## 3 在 BIRD 和 BookSQL 数据集上测试

### 3.1 下载数据集

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

### 3.2 配置数据库系统 Docker 环境

BIRD 和 BookSQL 没有提供数据库系统 docker 测试环境，需要自己配置数据库环境

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
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=postgres_password \
  postgres:14.18
```

验证安装和容器启动情况，尝试连接到容器

```bash
mysql -h 127.0.0.1 -P 13306 -u root -pmysql_root_password -e "SHOW DATABASES; SELECT DATABASE();"
PGPASSWORD='postgres_password' psql -h 127.0.0.1 -p 15432 -U root -d postgres -c "SELECT version(); SELECT current_database();"
```

### 3.3 查看并导入数据

需要安装两个工具将 sqlite3 数据库迁移到 MySQL 和 Postgresql

```bash
pip install sqlite3-to-mysql # 之前应该已经安装过了
sudo apt install pgloader
```

‼️TODO: 需要完善，这部分用这些工具无法成功转换

### 3.4 测试

‼️TODO: 需要完善