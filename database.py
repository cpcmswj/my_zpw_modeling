import os
import json
import threading

try:
    from vercel_sdk import Vercel
    VERCEL_SDK_AVAILABLE = True
except ImportError:
    VERCEL_SDK_AVAILABLE = False

class SimpleUserStore:
    def __init__(self):
        self._lock = threading.Lock()
        self._users = {}
        self._initialized = False
        self._vercel_client = None
        self._edge_config_item = "users_data"
        self._use_edge_config = False

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
        with self._lock:
            if self._initialized:
                return

            self._use_edge_config = os.environ.get("EDGE_CONFIG_ID") and os.environ.get("EDGE_CONFIG_TOKEN")

            if self._use_edge_config:
                print("[Edge Config] 初始化Edge Config存储")
                if self._load_from_edge_config():
                    self._initialized = True
                    return

            print("[Local] 使用本地内存存储")
            self._initialized = True

    def get_user(self, username):
        with self._lock:
            return self._users.get(username)

    def add_user(self, username, hashed_password):
        with self._lock:
            if username in self._users:
                return False
            self._users[username] = {
                "username": username,
                "hashed_password": hashed_password
            }
            self._save_to_edge_config()
            return True

    def user_exists(self, username):
        with self._lock:
            return username in self._users

    def get_all_users(self):
        with self._lock:
            return list(self._users.keys())

user_store = SimpleUserStore()

def init_db():
    user_store.init()
    print("[DB] 存储初始化完成")

class User:
    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password

def get_db():
    class DbSession:
        def __init__(self):
            pass

        def query(self, model):
            return UserQuery(self._users_ref())

        def add(self, user):
            user_store.add_user(user.username, user.hashed_password)

        def commit(self):
            pass

        def refresh(self, user):
            pass

        def _users_ref(self):
            return user_store._users

    return DbSession()

class UserQuery:
    def __init__(self, users_dict):
        self._users = users_dict

    def filter(self, condition):
        return self

    def first(self):
        return None

class DbContext:
    def __enter__(self):
        return get_db()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

def get_db_context():
    return DbContext()
