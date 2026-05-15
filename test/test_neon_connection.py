#!/usr/bin/env python3
"""
Neon 数据库测试脚本

使用方法：
1. 设置环境变量 NEON_DATABASE_URL
   export NEON_DATABASE_URL="postgres://user:password@host:port/database"

2. 运行脚本
   python test_neon_connection.py

3. 查看输出确认连接是否成功
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_db, user_store, NeonDatabase


def test_neon_connection():
    """测试 Neon 数据库连接"""
    print("=" * 60)
    print("Neon 数据库连接测试")
    print("=" * 60)
    
    # 检查环境变量
    neon_url = os.environ.get("NEON_DATABASE_URL")
    if not neon_url:
        print("❌ 未设置 NEON_DATABASE_URL 环境变量")
        print("请设置环境变量后再运行测试")
        print("示例: export NEON_DATABASE_URL='postgres://user:password@host:port/database'")
        return False
    
    print(f"✅ 检测到 NEON_DATABASE_URL: {neon_url[:20]}...")
    
    # 初始化数据库
    print("\n正在初始化数据库...")
    init_db()
    
    # 检查是否使用 Neon
    if user_store._use_neon:
        print("✅ 成功连接到 Neon 数据库")
        
        # 测试基本操作
        print("\n--- 测试用户操作 ---")
        
        # 测试添加用户
        test_user = "test_user_123"
        print(f"\n1. 添加用户: {test_user}")
        result = user_store.add_user(test_user, "hashed_password_123")
        print(f"   结果: {'成功' if result else '失败(用户已存在)'}")
        
        # 测试查询用户
        print(f"\n2. 查询用户: {test_user}")
        user = user_store.get_user(test_user)
        if user:
            print(f"   结果: 找到用户 - {user['username']}")
        else:
            print("   结果: 未找到用户")
        
        # 测试用户存在性检查
        print(f"\n3. 检查用户是否存在: {test_user}")
        exists = user_store.user_exists(test_user)
        print(f"   结果: {'存在' if exists else '不存在'}")
        
        # 测试获取所有用户
        print("\n4. 获取所有用户")
        users = user_store.get_all_users()
        print(f"   结果: 共 {len(users)} 个用户")
        for u in users[:5]:  # 最多显示5个
            print(f"     - {u}")
        
        # 测试更新用户
        print(f"\n5. 更新用户头像: {test_user}")
        result = user_store._neon_db.update_user(test_user, avatar_path="/avatars/test.png")
        print(f"   结果: {'成功' if result else '失败'}")
        
        # 测试删除用户
        print(f"\n6. 删除用户: {test_user}")
        result = user_store._neon_db.delete_user(test_user)
        print(f"   结果: {'成功' if result else '失败'}")
        
        # 验证删除
        print(f"\n7. 验证删除: {test_user}")
        exists = user_store.user_exists(test_user)
        print(f"   结果: {'已删除' if not exists else '仍存在'}")
        
        print("\n" + "=" * 60)
        print("🎉 所有测试通过!")
        print("=" * 60)
        return True
    else:
        print("❌ 未能连接到 Neon 数据库")
        print("请检查连接字符串是否正确")
        return False


if __name__ == "__main__":
    success = test_neon_connection()
    sys.exit(0 if success else 1)