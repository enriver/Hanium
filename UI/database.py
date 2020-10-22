import pymysql
import pandas as pd

class database():
    
    def __init__(self):
        self.conn = pymysql.connect(
            host = '3.21.41.113', 
            port =3306, 
            user = 'root',
            password = 'hanium', 
            db='NEWHAN', 
            charset='utf8')
        self.cursor = self.conn.cursor()
        
        
    
    # RETAINED_STOCK 테이블에 데이터가 있는지 확인    
    def check_data_in_retained_stock(self,account_num):
        
        sql = "select EXISTS (select * from RETAINED_STOCK where user_account="+account_num+");"
        self.cursor.execute(sql)
        self.conn.commit()
        
        db_res = self.cursor.fetchall()
        return db_res[0][0]
    
    # RETAINED_STOCK 테이블에 데이터 넣기 (처음 접속했을 때 한번만 실행)
    def retained_update(self,account_num, retained_list):
        
        for i in range(len(retained_list)):
            #sql = "INSERT INTO RETAINED_STOCK (user_account,stock_code,retained_volume) VALUES ('"+account_num+"','"+retained_list[i][0]+"','"+retained_list[i][1]+"') ON DUPLICATE KEY UPDATE user_account='"+account_num+"', stock_code='"+retained_list[i][0]+"', retained_volume='"+retained_list[i][1]+"';"
            
            sql = "INSERT INTO RETAINED_STOCK (user_account,stock_code,retained_volume) VALUES ('"+account_num+"','"+retained_list[i][0]+"','"+retained_list[i][1]+"');"
            self.cursor.execute(sql)
            self.conn.commit()
        

    # 보유종목 종목명 받아오기 - 파라미터 : (계좌명)
    def retained_get(self,data):
        sql = "SELECT stock_code FROM RETAINED_STOCK WHERE user_account="+data+";"
        self.cursor.execute(sql,data)
        self.conn.commit()
        db_res = self.cursor.fetchall()
        return db_res

    # 관심종목 종목명 받아오기 - 파라미터 : (계좌명)
    def interest_get(self,data):
        sql = "SELECT stock_code FROM INTEREST_STOCK WHERE user_account='"+data+"';"
        self.cursor.execute(sql)
        self.conn.commit()
        db_res = self.cursor.fetchall()
        return db_res

    # 보유종목 삭제 - 파라미터 : (계좌명, 종목코드)
    def ratained_delete(self, data):
        sql= "DELETE FROM RETAINED_STOCK WHERE user_account=$s and stock_code=$s;"
        self.cursor.execute(sql,data)
        self.conn.commit()
        
        print('보유종목이 삭제되었습니다.')

    # 관심종목 삭제 - 파라미터 : (계좌명, 종목코드)
    def interest_delete(self, account_num, interest_stock_code_deleted):
        sql= "DELETE FROM INTEREST_STOCK WHERE user_account='"+account_num+"' and stock_code='"+interest_stock_code_deleted+"';"
        self.cursor.execute(sql)
        self.conn.commit()

        print('관심종목이 삭제되었습니다.')

    # 관심종목 추가 - 파라미터 : (계좌명, 종목코드)
    def interest_insert(self, account_num, interest_stock_code):
        sql = "INSERT INTO INTEREST_STOCK(user_account,stock_code) VALUES ("+account_num+",'"+interest_stock_code+"');"
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

        print('관심종목이 추가되었습니다.')