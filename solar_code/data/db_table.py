import sqlite3
import uuid

class Chat:
    session_text=""
    session_id=""
    role=""
    content=""
    sql=""
    def __init__(self,db_path='app.db'):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor=self.conn.cursor()
        pass
    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- 自增主键
            session_id TEXT NOT NULL,            -- 会话ID
            role TEXT NOT NULL CHECK(role IN ('assistant', 'user', 'system')), -- 角色约束
            content TEXT NOT NULL,               -- 消息内容
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP -- 自动时间戳
                            )
                    ''')
        self.conn.commit()
    def create_chat(self,session_text,role,content):
        self.session_text=session_text
        namespace = uuid.NAMESPACE_DNS
        name = self.session_text
        self.session_id=str(uuid.uuid1())
        self.role=role
        self.content=content
        self.cursor.execute('''
            INSERT INTO chat_messages (session_id, role, content) 
            VALUES (?, ?, ?)
        ''', (self.session_id, self.role, self.content))
        self.conn.commit()  # 提交事务，确保数据持久化

    def delete_chat(self,session_id:str)->bool:
        self.session_id=session_id
        self.cursor.execute(
            '''
                delete from chat_messages where session_id=?
            ''',(self.session_id,)
        )
        self.conn.commit()
        return self.cursor.rowcount>0
    def update_chat(self,session_id:str,**kwargs)->bool:
        #更新用户信息（支持部分字段更新）
        set_clauses=[]
        params=[]
        if 'role' in kwargs:
            self.cursor.execute(f'''update chat_messages 
                                set role=?
                                where session_id=?''',(kwargs['role'],session_id))
            self.conn.commit()
        
        
    def get_all_sessions(self)->list[dict]:
        #获取所有会话信息
        self.cursor.execute("select * from chat_messages")
        return [dict(row) for row in self.cursor.fetchall()]
    def get_session(self,session_id:str)->dict:
        #获取特定会话信息
        self.cursor.execute("select * from chat_messages where session=?",(session_id,))
        row=self.cursor.fetchone()
        return dict(row)
    def close(self):
        self.cursor.close()
        self.conn.close()
    def __del__(self):
        """对象销毁时关闭连接"""
        try:
            self.conn.close()
        except:
            pass

# 用户信息存储表管理类
class UserInfoManager:
    def __init__(self, db_path='app.db'):
        """初始化数据库连接并创建表"""
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")  # 启用外键约束
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """创建用户信息表（如果不存在）"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,   -- 用户唯一标识
                name TEXT NOT NULL,         -- 用户姓名
                gender TEXT CHECK (gender IN ('男', '女', '其他')),
                birthday DATE               -- 生日
            )
        ''')
        self.conn.commit()

    def create_user(self, name: str, gender: str, birthday: str) -> str:
        """创建新用户，返回生成的 user_id"""
        user_id = str(uuid.uuid4())
        self.cursor.execute(
            "INSERT INTO users (user_id, name, gender, birthday) VALUES (?, ?, ?, ?)",
            (user_id, name, gender, birthday)
        )
        self.conn.commit()
        return user_id

    def delete_user(self, user_id: str) -> bool:
        """删除指定用户"""
        self.cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0  # 返回是否删除成功

    def update_user(self, user_id: str, **kwargs) -> bool:
        """更新用户信息（支持部分字段更新）"""
        set_clauses = []
        params = []
        for key in ['name', 'gender', 'birthday']:
            if key in kwargs:
                set_clauses.append(f"{key} = ?")
                params.append(kwargs[key])
        if not set_clauses:
            return False  # 无更新字段
        query = f"UPDATE users SET {', '.join(set_clauses)} WHERE user_id = ?"
        params.append(user_id)
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_all_users(self) -> list[dict]:
        """获取所有用户信息"""
        self.cursor.execute("SELECT * FROM users")
        return [dict(row) for row in self.cursor.fetchall()]

    def get_user(self, user_id: str) -> dict | None:
        """通过 user_id 获取用户信息"""
        self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def close(self):
        """关闭数据库连接"""
        self.conn.close()

    def __del__(self):
        """对象销毁时关闭连接"""
        try:
            self.conn.close()
        except:
            pass

# 备忘录/日程提醒表管理类
class ReminderManager:
    def __init__(self, db_path='app.db'):
        """初始化数据库连接并创建表"""
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """创建备忘录表（如果不存在）"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                title TEXT NOT NULL,           -- 事件标题   
                content TEXT,                  -- 事件内容
                event_type TEXT,                -- 事件类型(单次/循环/每日/每周/每月/每年)
                remind_time DATETIME,          -- 提醒时间（可为空）
                status TEXT CHECK(status IN ('未完成','已完成','已过期')),      
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP  -- 时间戳      
                    )
        ''')
        self.conn.commit()

    def create_reminder(self, title: str, content: str, event_type: str,remind_time: str, status: str) -> str:
        """创建新提醒事件"""
        reminder_id = str(uuid.uuid4())
        self.cursor.execute(
            "INSERT INTO reminders (title, content, event_type, remind_time, status) "
            "VALUES (?, ?, ?, ?, ?)",
            (title, content, event_type, remind_time, status)
        )
        self.conn.commit()
        return reminder_id

    def delete_reminder(self, reminder_id: str) -> bool:
        """删除指定提醒事件"""
        self.cursor.execute("DELETE FROM reminders WHERE reminder_id=?", (reminder_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def update_reminder(self, reminder_id: str, **kwargs) -> bool:      #待研究
        """更新提醒事件（支持部分字段更新）"""
        set_clauses = []
        params = []
        for key in ['remind_time', 'event_type', 'cycle_type', 'title', 'content', 'expired']:
            if key in kwargs:
                set_clauses.append(f"{key} = ?")
                params.append(kwargs[key])
        if not set_clauses:
            return False  # 无更新字段
        query = f"UPDATE reminders SET {', '.join(set_clauses)} WHERE reminder_id = ?"
        params.append(reminder_id)
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_all_reminders(self) -> list[dict]:
        """获取所有提醒事件"""
        self.cursor.execute("SELECT * FROM reminders")
        return [dict(row) for row in self.cursor.fetchall()]

    def get_reminder(self, reminder_id: str) -> dict | None:
        """通过 reminder_id 获取提醒事件"""
        self.cursor.execute("SELECT * FROM reminders WHERE reminder_id=?", (reminder_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def get_user_reminders(self, user_id: str) -> list[dict]:
        """获取指定用户的提醒事件"""
        self.cursor.execute("SELECT * FROM reminders WHERE user_id=?", (user_id,))
        return [dict(row) for row in self.cursor.fetchall()]

    def close(self):
        self.conn.close()

    def __del__(self):
        try:
            self.conn.close()
        except:
            pass

# 人格设定表管理类
class PersonaManager:
    def __init__(self, db_path='app.db'):
        """初始化数据库连接并创建表"""
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """创建人格设定表（如果不存在）"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS personas (
                name TEXT NOT NULL UNIQUE,    -- 人格名称（唯一）
                prompt TEXT                   -- 提示词
            )
        ''')
        self.conn.commit()

    def create_persona(self, name: str, prompt: str) -> str:
        """创建新的人格设定"""
        try:
            self.cursor.execute(
                "INSERT INTO personas (name, prompt) VALUES (?, ?)",
                (name, prompt)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"人格名称 '{name}' 已存在")

    def delete_persona(self, persona_id: str) -> bool:
        """删除指定人格设定"""
        self.cursor.execute("DELETE FROM personas WHERE persona_id=?", (persona_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def update_persona(self, persona_id: str, **kwargs) -> bool:
        """更新人格设定（支持部分字段更新）"""
        set_clauses = []
        params = []
        for key in ['name', 'prompt']:
            if key in kwargs:
                set_clauses.append(f"{key} = ?")
                params.append(kwargs[key])
        if not set_clauses:
            return False  # 无更新字段
        query = f"UPDATE personas SET {', '.join(set_clauses)} WHERE persona_id = ?"
        params.append(persona_id)
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_all_personas(self) -> list[dict]:
        """获取所有人格设定"""
        self.cursor.execute("SELECT * FROM personas")
        return [dict(row) for row in self.cursor.fetchall()]

    def get_persona(self, persona_id: str) -> dict | None:
        """通过 persona_id 获取人格设定"""
        self.cursor.execute("SELECT * FROM personas WHERE persona_id=?", (persona_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def get_persona_by_name(self, name: str) -> dict | None:
        """通过名称获取人格设定"""
        self.cursor.execute("SELECT * FROM personas WHERE name=?", (name,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def close(self):
        self.conn.close()

    def __del__(self):
        try:
            self.conn.close()
        except:
            pass
