import os
import subprocess

def backup(db_user='root', db_name='bi_db', out_file='backup.sql'):
    cmd = ['mysqldump', '-u', db_user, db_name]
    with open(out_file, 'wb') as f:
        subprocess.run(cmd, stdout=f)

if __name__ == '__main__':
    backup()
