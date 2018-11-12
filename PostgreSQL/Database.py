import psycopg2 as psycopg2


class DataBase:
    def __init__(self, host="localhost", database="twitter", user="postgres", password="123456"):
        self.conn = psycopg2.connect(host=host, database=database, user=user, password=password)

    def insert(self, from_name, from_user_name, to_name, to_user_name):
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO public.usernames VALUES(%s, %s)",
                        (from_name, from_user_name))
        except:
            pass
        self.conn.commit()
        cur.close()

        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO public.usernames VALUES(%s, %s)",
                        (to_name, to_user_name))
        except:
            pass

        self.conn.commit()
        cur.close()

        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO public.relationships VALUES(%s, %s)",
                        (from_name, to_name))
        except:
            pass
        self.conn.commit()
        cur.close()

    def check(self, from_user_name, to_user_name):
        cur = self.conn.cursor()
        cur.execute("select * from relationships where from_user_name = %s and to_user_name = %s", (from_user_name, to_user_name))
        if cur.rowcount > 0:
            return True
        else:
            return False