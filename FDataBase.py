class FDataBase:
   def __init__(self, db):
      self.__db = db
      self.__cur = db.cursor()
      
   def getComments(self):
      sql = '''SELECT * FROM comments'''
      try:
         self.__cur.execute(sql)
         res = self.__cur.fetchall()
         if res: return res[::-1]
      except:
         print("Ошибка чтения из БД")
      return []
   
   def addComment(self, username, email, comment):
      try:
         self.__cur.execute("INSERT INTO comments VALUES(?, ?, ?)", (username, email, comment))
         self.__db.commit()
      except:
         print("Ошибка добавления комментария в БД")
         return False
      return True
   