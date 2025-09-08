import oracledb
import pandas as pd
import sys
import traceback


def gen(src_kind):
    try:
        print(f"執行數據種類：{src_kind}")

        # 建立連線（純 Python 模式）
        oracledb.init_oracle_client(lib_dir=r"/Users/yangfengkai/Documents/instantclient-basic-macos")

        conn = oracledb.connect(
            user="prg",
            password="prg7695",
            dsn="192.168.70.21:1521/mis.gs.com.cn"
            # dsn="RAC-SCAN.ginko.com.tw/orcl"
        )

        # 撈資料
        # sql = "SELECT * FROM hrm.hrm_em_labor_health_adjust_v"
        # sql = "SELECT * FROM hrm.hrm_em_labor_health_adjust_v where 調整日期='114-09-01'"
        sql = f"SELECT * FROM idm.idm_user where rownum < 10"
        df = pd.read_sql(sql, conn)
        conn.close()
        # print(df)
        # 輸出 Excel
        df.to_excel(r"../data/train/hrmip11.xlsx", sheet_name="原始資料" + src_kind, index=False)
    except Exception as e:
        with open(r"../logs/oracle2bio.log", "a", encoding="utf-8") as f:
            f.write(f"錯誤發生於 gen {src_kind}：\n")
            f.write(traceback.format_exc())
        print(f"❌ gen 失敗，請查看 oracle2bio.log")


# 主程式入口
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("請提供數據類型參數，例如：CUSTOMER")
    else:
        gen(sys.argv[1])
