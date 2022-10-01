import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def db_local_connect():
    "This function for connect postgresql database"
    host = ""
    if host == "cloud":
        project_db = psycopg2.connect(
            host="db.qkgjtcncguuailctmjwa.supabase.co",
            user="postgres",
            password="FBmnRsy7h96Lbeg9",
            database="postgres")
        project_db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT);
    else:
        project_db = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="root",
            database="project_db")
        project_db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT); #Important to 'cannot run inside a transaction block'
    return project_db





