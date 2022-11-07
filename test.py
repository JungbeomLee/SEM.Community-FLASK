import pymysql

db = pymysql.connect(
    user='root',
    passwd='0000',
    host='localhost',
    port=3306,
    db='sebuung_db',
    charset='utf8'
)
cursor = db.cursor()

cursor.execute("SELECT board_num, title, category, start_day, tech_stack FROM test")
post_list = cursor.fetchall()

print(post_list)
# for i in post_list:
#     print(i)