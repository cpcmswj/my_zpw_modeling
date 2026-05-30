import os
import json
import threading

try:
    import psycopg2
    from psycopg2 import pool
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

try:
    from vercel_sdk import Vercel
    VERCEL_SDK_AVAILABLE = True
except ImportError:
    VERCEL_SDK_AVAILABLE = False


class NeonDatabase:
    """
    Neon 数据库实现类
    
    Neon 是一个 Serverless PostgreSQL 数据库服务。
    本类提供用户数据的持久化存储支持。
    
    环境变量配置：
        NEON_DATABASE_URL - Neon 数据库连接URL（优先）
        NEON_HOST - 数据库主机
        NEON_PORT - 数据库端口（默认5432）
        NEON_DATABASE - 数据库名称
        NEON_USER - 数据库用户名
        NEON_PASSWORD - 数据库密码
    
    使用示例：
    >>> from database import neon_db, init_db
    >>> init_db()
    >>> neon_db.add_user("admin", "hashed_password")
    >>> user = neon_db.get_user("admin")
    """
    
    def __init__(self):
        self._lock = threading.Lock()
        self._connection_pool = None
        self._initialized = False
        self._use_neon = False
    
    def _get_connection(self):
        """从连接池获取数据库连接"""
        if self._connection_pool is None:
            return None
        return self._connection_pool.getconn()
    
    def _release_connection(self, conn):
        """释放数据库连接回连接池"""
        if self._connection_pool is not None and conn is not None:
            self._connection_pool.putconn(conn)
    
    def _init_tables(self, conn):
        """初始化用户表（如果不存在）"""
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        hashed_password VARCHAR(255) NOT NULL,
                        avatar_path VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                print("[Neon] 用户表初始化完成")
        except Exception as e:
            print(f"[Neon] 初始化表失败: {e}")
            conn.rollback()
    
    def _parse_connection_string(self, url):
        """解析 PostgreSQL 连接字符串"""
        # 格式: postgres://user:password@host:port/database
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return {
            'host': parsed.hostname,
            'port': parsed.port or 5432,
            'database': parsed.path[1:],  # 移除开头的 '/'
            'user': parsed.username,
            'password': parsed.password
        }
    
    def init(self):
        """
        初始化 Neon 数据库连接
        
        连接优先级：
        1. NEON_DATABASE_URL 环境变量
        2. POSTGRES_URL 环境变量（Vercel Postgres）
        3. DATABASE_URL 环境变量（其他 Postgres 服务）
        4. 分别设置的 NEON_HOST, NEON_USER, NEON_PASSWORD 等变量
        
        如果没有配置 Neon，将不初始化连接池（使用回退存储）
        """
        with self._lock:
            if self._initialized:
                return
            
            # 检查 psycopg2 是否可用
            if not PSYCOPG2_AVAILABLE:
                print("[Neon] psycopg2 库未安装，跳过 Neon 初始化")
                self._initialized = True
                return
            
            # 检查是否配置了 Neon 或其他 Postgres 数据库
            # 支持多种环境变量名称
            neon_url = (
                os.environ.get("NEON_DATABASE_URL") or 
                os.environ.get("POSTGRES_URL") or 
                os.environ.get("DATABASE_URL")
            )
            
            if neon_url:
                print(f"[DB] 检测到数据库连接 URL: {neon_url[:50]}...")
                try:
                    config = self._parse_connection_string(neon_url)
                    self._connection_pool = psycopg2.pool.SimpleConnectionPool(
                        minconn=1,
                        maxconn=10,
                        **config
                    )
                    
                    # 测试连接并初始化表
                    conn = self._get_connection()
                    if conn:
                        self._init_tables(conn)
                        self._release_connection(conn)
                        self._use_neon = True
                        print("[Neon] 成功连接到 Neon 数据库")
                    else:
                        print("[Neon] 无法建立连接")
                except Exception as e:
                    print(f"[Neon] 初始化失败: {e}")
            else:
                print("[Neon] 未配置 NEON_DATABASE_URL，跳过 Neon 初始化")
            
            self._initialized = True
    
    def get_user(self, username):
        """
        获取用户信息
        
        参数：
            username (str): 用户名
            
        返回：
            dict or None: 用户数据字典
        """
        if not self._use_neon or not self._connection_pool:
            return None
        
        conn = None
        try:
            conn = self._get_connection()
            if not conn:
                return None
            
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT username, hashed_password, avatar_path 
                    FROM users 
                    WHERE username = %s
                """, (username,))
                row = cur.fetchone()
                
                if row:
                    return {
                        'username': row[0],
                        'hashed_password': row[1],
                        'avatar_path': row[2]
                    }
                return None
        except Exception as e:
            print(f"[Neon] 查询用户失败: {e}")
            return None
        finally:
            self._release_connection(conn)
    
    def add_user(self, username, hashed_password, avatar_path=None):
        """
        添加新用户
        
        参数：
            username (str): 用户名
            hashed_password (str): 哈希后的密码
            avatar_path (str, optional): 头像路径
            
        返回：
            bool: 添加成功返回True，失败返回False
            
        异常：
            当数据库连接不可用时抛出 RuntimeError
        """
        if not self._use_neon or not self._connection_pool:
            print("[Neon] 数据库连接不可用，无法添加用户")
            raise RuntimeError("数据库连接不可用，请检查 DATABASE_URL 环境变量配置")
        
        conn = None
        try:
            conn = self._get_connection()
            if not conn:
                print("[Neon] 无法获取数据库连接")
                raise RuntimeError("无法获取数据库连接")
            
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (username, hashed_password, avatar_path)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (username) DO NOTHING
                """, (username, hashed_password, avatar_path))
                conn.commit()
                
                if cur.rowcount > 0:
                    print(f"[Neon] 用户 {username} 成功添加到数据库")
                    return True
                else:
                    print(f"[Neon] 用户 {username} 已存在，未插入")
                    return False
        except RuntimeError:
            raise
        except Exception as e:
            print(f"[Neon] 添加用户失败: {e}")
            if conn:
                conn.rollback()
            raise RuntimeError(f"添加用户失败: {e}")
        finally:
            self._release_connection(conn)
    
    def user_exists(self, username):
        """
        检查用户是否存在
        
        参数：
            username (str): 用户名
            
        返回：
            bool: 用户存在返回True
        """
        if not self._use_neon or not self._connection_pool:
            return False
        
        conn = None
        try:
            conn = self._get_connection()
            if not conn:
                return False
            
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 1 FROM users WHERE username = %s
                """, (username,))
                return cur.fetchone() is not None
        except Exception as e:
            print(f"[Neon] 检查用户失败: {e}")
            return False
        finally:
            self._release_connection(conn)
    
    def get_all_users(self):
        """
        获取所有用户名列表
        
        返回：
            list: 用户名列表
        """
        if not self._use_neon or not self._connection_pool:
            return []
        
        conn = None
        try:
            conn = self._get_connection()
            if not conn:
                return []
            
            with conn.cursor() as cur:
                cur.execute("SELECT username FROM users ORDER BY username")
                return [row[0] for row in cur.fetchall()]
        except Exception as e:
            print(f"[Neon] 获取用户列表失败: {e}")
            return []
        finally:
            self._release_connection(conn)
    
    def update_user(self, username, hashed_password=None, avatar_path=None):
        """
        更新用户信息
        
        参数：
            username (str): 用户名
            hashed_password (str, optional): 新密码
            avatar_path (str, optional): 新头像路径
            
        返回：
            bool: 更新成功返回True
        """
        if not self._use_neon or not self._connection_pool:
            return False
        
        conn = None
        try:
            conn = self._get_connection()
            if not conn:
                return False
            
            updates = []
            params = []
            
            if hashed_password:
                updates.append("hashed_password = %s")
                params.append(hashed_password)
            
            if avatar_path is not None:
                updates.append("avatar_path = %s")
                params.append(avatar_path)
            
            if not updates:
                return False
            
            params.append(username)
            
            with conn.cursor() as cur:
                cur.execute(f"""
                    UPDATE users SET {', '.join(updates)}
                    WHERE username = %s
                """, params)
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"[Neon] 更新用户失败: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            self._release_connection(conn)
    
    def delete_user(self, username):
        """
        删除用户
        
        参数：
            username (str): 用户名
            
        返回：
            bool: 删除成功返回True
        """
        if not self._use_neon or not self._connection_pool:
            return False
        
        conn = None
        try:
            conn = self._get_connection()
            if not conn:
                return False
            
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE username = %s", (username,))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            print(f"[Neon] 删除用户失败: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            self._release_connection(conn)


class SimpleUserStore:
    """
    用户数据存储类，支持多种存储后端：
    1. Neon 数据库（优先）
    2. Vercel Edge Config
    3. 本地内存存储（回退）
    
    使用示例：
    >>> from database import user_store, init_db
    >>> init_db()
    >>> user_store.add_user("admin", "hashed_password")
    """
    
    def __init__(self):
        self._lock = threading.Lock()
        self._users = {}
        self._initialized = False
        self._vercel_client = None
        self._edge_config_item = "users_data"
        self._use_edge_config = False
        self._neon_db = NeonDatabase()
        self._use_neon = False

    def _get_vercel_client(self):
        if self._vercel_client is None and VERCEL_SDK_AVAILABLE:
            self._vercel_client = Vercel()
        return self._vercel_client

    def _load_from_edge_config(self):
        if not VERCEL_SDK_AVAILABLE:
            return False

        vercel = self._get_vercel_client()
        if vercel is None:
            return False

        try:
            edge_config_id = os.environ.get("EDGE_CONFIG_ID")
            edge_config_token = os.environ.get("EDGE_CONFIG_TOKEN")

            if not edge_config_id or not edge_config_token:
                return False

            items = vercel.getEdgeConfigItems(edge_config_id)
            for item in items:
                if item.key == self._edge_config_item:
                    if item.value:
                        self._users = json.loads(item.value)
                        print(f"[Edge Config] 从Edge Config加载了 {len(self._users)} 个用户")
                        return True
        except Exception as e:
            print(f"[Edge Config] 加载数据失败: {e}")
        return False

    def _save_to_edge_config(self):
        if not self._use_edge_config or not VERCEL_SDK_AVAILABLE:
            return

        vercel = self._get_vercel_client()
        if vercel is None:
            return

        try:
            edge_config_id = os.environ.get("EDGE_CONFIG_ID")
            edge_config_token = os.environ.get("EDGE_CONFIG_TOKEN")

            if not edge_config_id or not edge_config_token:
                return

            vercel.patchEdgeConfigItems(
                edge_config_id,
                items=[{
                    "operation": "upsert",
                    "key": self._edge_config_item,
                    "value": json.dumps(self._users)
                }]
            )
        except Exception as e:
            print(f"[Edge Config] 保存数据失败: {e}")

    def init(self):
        """初始化存储系统，按优先级选择存储后端"""
        with self._lock:
            if self._initialized:
                return

            # 优先尝试 Neon 数据库
            self._neon_db.init()
            if self._neon_db._use_neon:
                self._use_neon = True
                print("[DB] 使用 Neon 数据库存储")
                self._initialized = True
                return

            # 其次尝试 Edge Config
            self._use_edge_config = os.environ.get("EDGE_CONFIG_ID") and os.environ.get("EDGE_CONFIG_TOKEN")
            if self._use_edge_config:
                print("[Edge Config] 初始化Edge Config存储")
                if self._load_from_edge_config():
                    self._initialized = True
                    return

            # 回退到本地内存存储
            print("[Local] 使用本地内存存储")
            self._initialized = True

    def get_user(self, username):
        """获取用户信息"""
        if self._use_neon:
            return self._neon_db.get_user(username)
        
        with self._lock:
            return self._users.get(username)

    def add_user(self, username, hashed_password, avatar_path=None):
        """添加新用户
        
        返回：
            bool: 添加成功返回True
            
        异常：
            当数据库连接失败时抛出 RuntimeError
        """
        if self._use_neon:
            return self._neon_db.add_user(username, hashed_password, avatar_path)
        
        with self._lock:
            if username in self._users:
                return False
            self._users[username] = {
                "username": username,
                "hashed_password": hashed_password,
                "avatar_path": avatar_path
            }
            self._save_to_edge_config()
            print(f"[Local] 用户 {username} 已添加到本地存储")
            return True

    def user_exists(self, username):
        """检查用户是否存在"""
        if self._use_neon:
            return self._neon_db.user_exists(username)
        
        with self._lock:
            return username in self._users

    def get_all_users(self):
        """获取所有用户名列表"""
        if self._use_neon:
            return self._neon_db.get_all_users()
        
        with self._lock:
            return list(self._users.keys())


# 全局用户存储实例
user_store = SimpleUserStore()


def init_db():
    """初始化数据库（应在应用启动时调用）"""
    user_store.init()
    print("[DB] 存储初始化完成")


class User:
    """用户模型类"""
    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password


def get_db():
    """获取数据库会话对象（模拟SQLAlchemy风格）"""
    class DbSession:
        def __init__(self):
            pass

        def query(self, model):
            return UserQuery(user_store._users if not user_store._use_neon else {})

        def add(self, user):
            user_store.add_user(user.username, user.hashed_password)

        def commit(self):
            pass

        def refresh(self, user):
            pass

    return DbSession()


class UserQuery:
    """用户查询类"""
    def __init__(self, users_dict):
        self._users = users_dict

    def filter(self, condition):
        return self

    def first(self):
        return None


class DbContext:
    """数据库上下文管理器"""
    def __enter__(self):
        return get_db()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def get_db_context():
    """获取数据库上下文管理器"""
    return DbContext()
