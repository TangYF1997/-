import pymssql


class MSSQL:
    def __init__(self, host, user, pwd, db):  # 类的构造函数，初始化数据库连接ip或者域名，以及用户名，密码，要连接的数据库名称
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):  # 得到数据库连接信息函数， 返回: conn.cursor()
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset='utf8')
        cur = self.conn.cursor()  # 将数据库连接信息，赋值给cur。
        if not cur:
            return (NameError, "连接数据库失败")
        else:
            return cur

    # 执行查询语句,返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
    def ExecQuery(self, sql):  # 执行Sql语句函数，返回结果
        cur = self.__GetConnect()  # 获得数据库连接信息
        cur.execute(sql)  # 执行Sql语句
        resList = cur.fetchall()  # 获得所有的查询结果
        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList  # 返回查询结果

    def ExecNonQuery(self, sql):  # 执行Sql语句，不返回结果

        cur = self.__GetConnect()  # 获得数据库连接信息
        cur.execute(sql)  # 执行Sql语句
        self.conn.commit()
        self.conn.close()



server = "127.0.0.1:1433"
user = "lzx"
password = "251066"
database = "studentAttendance"

mssql = ""


def main():
    global mssql
    mssql = MSSQL(server, user, password, database)


def add_student(user_id, user_name, course_id):  # 增
    sql = "INSERT "+course_id+" VALUES (\'"+user_id+"\', \'"+user_name+"\', \'"+course_id+"\', null, null, null)"
    return sql


def del_student(user_id, course_id):  # 删
    sql = "delete "+course_id+" where [学号（student_id）]=\'"+user_id+"\'"
    return sql


def update_student(user_id, user_name, course_id):  # 改
    sql = "update "+course_id+" SET [姓名（student_name）]=\'"+user_name+"\' where [学号（student_id）]=\'"+user_id+"\'"
    return sql


def search_student_in_course(course_id):  # 查全部
    sql = "SELECT * FROM "+course_id+""
    return sql


def search_student(user_id, course_id):  # 查一行
    sql = "SELECT * FROM "+course_id+" where [学号（student_id）]=\'"+user_id+"\'"
    return sql


def copy_student(user_id, src_course_id, dst_course_id):
    sql = "insert into "+dst_course_id+" select * from "+src_course_id+" where [学号（student_id）]=\'"+user_id+"\'"
    return sql


def test():
    # rows = mssql.ExecNonQuery(add_student('0121509350314', '吴博二号', 'DIP'))  #注册
    rows = mssql.ExecNonQuery(del_student('0121509350314', 'DIP'))  # 删除
    print(rows)


if __name__ == '__main__':
    main()
    test()

#
#
# # 数据库连
# conn = pymssql.connect(host='127.0.0.1:1433', user='lzx', password='251066', database='studentAttendance')
#
# # 打开游标
# cur = conn.cursor()
#
# if not cur:
#     raise Exception('数据库连接失败！')
#
#
# def InsertData():
#     sql = "INSERT INTO Table_1 VALUES ('0121509350312', '吴博二号', '数电', '35', '0.875', 1)"
#     cur.execute(sql)
#     # 如果没有指定autocommit属性为True的话就需要调用commit()方法
#     conn.commit()
#
# InsertData()
#
# conn.close()