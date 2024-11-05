from esurv_db_manager import EPC_DB

pg_db = EPC_DB()
pg_conn = pg_db.connect()
#cursor = pg_conn.cursor()
pg_db.disconnect()