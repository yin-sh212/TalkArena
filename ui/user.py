"""
用户系统 - 简易用户状态管理
"""
import uuid
from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class User:
    user_id: str
    name: str
    surname: str = ""
    email: str = ""
    avatar_letter: str = "Z"
    
    @property
    def display_name(self) -> str:
        return f"{self.name} {self.surname}".strip() or "访客"
    
    @property
    def avatar_color(self) -> str:
        return "#EC4899"  # 粉红色

# 全局用户存储
_users: Dict[str, User] = {}
_current_user_id: Optional[str] = None

def register_user(name: str, surname: str = "", email: str = "", message: str = "") -> User:
    """注册新用户"""
    user_id = str(uuid.uuid4())[:8]
    
    # 取名字首字母作为头像
    avatar_letter = name[0].upper() if name else "Z"
    
    user = User(
        user_id=user_id,
        name=name,
        surname=surname,
        email=email,
        avatar_letter=avatar_letter
    )
    
    _users[user_id] = user
    
    global _current_user_id
    _current_user_id = user_id
    
    return user

def get_current_user() -> User:
    """获取当前用户"""
    global _current_user_id
    
    if _current_user_id and _current_user_id in _users:
        return _users[_current_user_id]
    
    # 默认访客用户
    return User(
        user_id="guest",
        name="访客",
        avatar_letter="Z"
    )

def set_current_user(user_id: str) -> bool:
    """设置当前用户"""
    global _current_user_id
    if user_id in _users:
        _current_user_id = user_id
        return True
    return False

def get_user_avatar_html(size: int = 40) -> str:
    """生成用户头像HTML"""
    user = get_current_user()
    return f'''
    <div class="user-avatar" style="
        width: {size}px;
        height: {size}px;
        border-radius: 50%;
        background: {user.avatar_color};
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: {size // 2}px;
        border: 3px solid #1F2937;
    ">{user.avatar_letter}</div>
    '''
