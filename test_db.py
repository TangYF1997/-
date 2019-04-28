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


def update_student_count(user_id, course_id):  # 记录拍到次数
    sql = "update "+course_id+" SET 拍到次数=Isnull(拍到次数,0)+1 where [学号（student_id）]=\'"+user_id+"\'"
    return sql


def update_student_efficiency(course_id):  # 改抬头率和是否到勤
    sql = "update "+course_id+" SET 抬头率=Isnull(拍到次数,0)/40.0,是否到勤 = Isnull(拍到次数,0)"

    return sql


def search_student_in_course(course_id):  # 查全部
    sql = "SELECT * FROM "+course_id+""
    return sql


def search_student(user_id, course_id):  # 查一行
    sql = "SELECT * FROM "+course_id+" where [学号（student_id）]=\'"+user_id+"\'"
    return sql


def copy_student(user_id, src_course_id, dst_course_id):
    sql = """
    insert into """+dst_course_id+""" select * from """+src_course_id+""" where [学号（student_id）]=\'"""+user_id+"""\'
    UPDATE """+dst_course_id+""" SET [课程]=\'"""+dst_course_id+"""\' WHERE [学号（student_id）] = \'"""+user_id+"""\'
    """
    return sql


def creat_table(course_id):
    sql = """
    CREATE TABLE """+course_id+"""(
        [学号（student_id）] [nchar](13) NOT NULL,
        [姓名（student_name）] [nchar](5) NULL,
        [课程] [nchar](10) NOT NULL,
        [拍到次数] [int] NULL,
        [抬头率] [float] NULL,
        [是否到勤] [bit] NULL,
     CONSTRAINT ["""+course_id+"""_1] PRIMARY KEY CLUSTERED 
    (
        [学号（student_id）] ASC
    )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
    ) ON [PRIMARY]
    """
    return sql


def del_table(course_id):
    sql = """
    DROP TABLE """+course_id+"""
    """
    return sql

def wipe_data(course_id):
    sql = "UPDATE "+course_id+" SET 拍到次数=null,抬头率=null,是否到勤=null"
    return sql


def output_table(course_id):
    output = open('data.xls', 'w', encoding='gbk')
    output.write('学号\t姓名\t课程\t拍到次数\t抬头率\t是否到勤\n')
    row = mssql.ExecQuery(search_student_in_course(course_id))  # 输出excel
    for i in range(len(row)):
        for j in range(len(row[i])):
            output.write(str(row[i][j]))  # write函数不能写int类型的参数，所以使用str()转化
            output.write('\t')  # 相当于Tab一下，换一个单元格
        output.write('\n')  # 写完一行立马换行
    output.close()


# def test():
    # rows = mssql.ExecNonQuery(add_student('0121509350314', '吴博二号', 'DIP'))  #注册
    # rows = mssql.ExecNonQuery(del_student('0121509350314', 'DIP'))  # 删除
    # mssql.ExecNonQuery(creat_table('DQP'))  # 创建表
    # mssql.ExecNonQuery(del_table('DMP'))  # 删除表
    # mssql.ExecNonQuery(update_student_count('0121509350313', 'DSP'))
    # mssql.ExecNonQuery(update_student_efficiency('DSP'))
    # output_table('DSP')



# if __name__ == '__main__':
#     main()
#     test()

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