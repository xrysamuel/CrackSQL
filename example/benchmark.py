import sys
from dataset import parse_sql_translation_pairs

sys.path.append("../backend")

from cracksql import translate, initkb

def initkb_func():
    try:
        initkb("./init_config.yaml")  # 首先在`.yaml`中填写基本配置
        print("Knowledge base initialized successfully")
    except Exception as e:
        print(f"Knowledge base initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()


def trans_func():
    target_db_config = {
        "host": "目标数据库主机",
        "port": "目标数据库端口号（整数类型）",
        "user": "目标数据库用户名",
        "password": "目标数据库密码",
        "db_name": "目标数据库数据库名"
    }

    vector_config = {
        "src_kb_name": "源数据库知识库名称",
        "tgt_kb_name": "目标数据库知识库名称"
    }

    try:
        print("Starting SQL translation...")
        translated_sql, model_ans_list, used_pieces, lift_histories = translate(
            model_name="DeepSeek-R1-Distill-Qwen-32B", 
            src_sql='SELECT DISTINCT "t1"."id" , EXTRACT(YEAR FROM CURRENT_TIMESTAMP) - EXTRACT(YEAR FROM CAST( "t1"."birthday" AS TIMESTAMP )) FROM "patient" AS "t1" INNER JOIN "examination" AS "t2" ON "t1"."id" = "t2"."id" WHERE "t2"."rvvt" = "+"',
            src_dialect="postgresql",
            tgt_dialect="mysql",
            target_db_config=target_db_config,
            vector_config=vector_config,
            out_dir="./", 
            retrieval_on=False, 
            top_k=3
        )

        print("Translation completed!")
        print(f"Translated SQL: {translated_sql}")
        print(f"Model answer list: {model_ans_list}")
        print(f"Used knowledge pieces: {used_pieces}")
        print(f"Lift histories: {lift_histories}")
    except Exception as e:
        print(f"Error occurred during translation: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    pairs = parse_sql_translation_pairs("test.json")
    # initkb_func()
    # trans_func()