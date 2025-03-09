import sqlite3
import uuid

class SessionManager:
    def __init__(self, db_path='test.db'):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # 按列名访问结果
        self.cursor = self.conn.cursor()
        self._create_table()  # 初始化时创建表（如果不存在）

    def _create_table(self):
        """创建会话表（如果不存在）"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                uuid TEXT PRIMARY KEY,  -- UUID作为主键
                title TEXT NOT NULL     -- 会话标题
            )
        ''')
        self.conn.commit()

    def create_session(self, title: str) -> str:
        """创建新会话并返回生成的UUID"""
        session_uuid = str(uuid.uuid4())
        try:
            self.cursor.execute(
                "INSERT INTO sessions (uuid, title) VALUES (?, ?)",
                (session_uuid, title)
            )
            self.conn.commit()
            return session_uuid
        except sqlite3.IntegrityError:
            raise ValueError("UUID冲突（理论上不可能发生）")

    def delete_session(self, uuid_str: str) -> bool:
        """删除指定UUID的会话"""
        self.cursor.execute("DELETE FROM sessions WHERE uuid=?", (uuid_str,))
        self.conn.commit()
        return self.cursor.rowcount > 0  # 返回是否删除成功

    def update_session(self, uuid_str: str, new_title: str) -> bool:
        """更新会话标题"""
        self.cursor.execute(
            "UPDATE sessions SET title=? WHERE uuid=?",
            (new_title, uuid_str)
        )
        self.conn.commit()
        return self.cursor.rowcount > 0  # 返回是否更新成功

    def get_all_sessions(self) -> list[dict]:
        """获取所有会话"""
        self.cursor.execute("SELECT uuid, title FROM sessions")
        return [dict(row) for row in self.cursor.fetchall()]

    def get_session(self, uuid_str: str) -> dict | None:
        """通过UUID获取单个会话"""
        self.cursor.execute("SELECT uuid, title FROM sessions WHERE uuid=?", (uuid_str,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def close(self):
        """关闭数据库连接"""
        self.conn.close()

    def __del__(self):
        """对象销毁时确保连接关闭"""
        try:
            self.conn.close()
        except:
            pass  # 避免在异常时重复关闭

if __name__ == '__main__':
    # 初始化管理器
    manager = SessionManager()
    
    # 创建会话
    new_uuid = manager.create_session("测试会话A")
    print(f"新建会话UUID: {new_uuid}")
    
    # 更新会话
    success = manager.update_session(new_uuid, "更新后的测试会话")
    print(f"更新结果: {'成功' if success else '失败'}")
    
    # 获取所有会话
    all_sessions = manager.get_all_sessions()
    print("所有会话:", all_sessions)
    
    # 删除会话
    delete_success = manager.delete_session(new_uuid)
    print(f"删除结果: {'成功' if delete_success else '失败'}")
    
    # 关闭连接
    manager.close()
