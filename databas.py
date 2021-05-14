import mysql.connector

def test():
    db = mysql.connector.connect(
        host="us-cdbr-east-03.cleardb.com",
        user="b785fbb89c1d88",
        password="5872c3bf",
        database="heroku_d100d1934e0d01d"
    )

    print(db.is_connected())
    db.close()


def insert(todo):
    db = mysql.connector.connect(
        host="us-cdbr-east-03.cleardb.com",
        user="b785fbb89c1d88",
        password="5872c3bf",
        database="heroku_d100d1934e0d01d"
    )
    cur = db.cursor()
    sql="insert into todo (id,task,dueby,status) values (%s , %s, %s, %s)"
    val=[todo["id"],todo["task"],todo["dueby"][:10],todo["status"]]
    cur.execute(sql,val)
    db.commit()
    cur.close()
    db.close()
