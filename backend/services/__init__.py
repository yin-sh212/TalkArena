"""
服务层 - 全局单例
"""
from .game_service import GameService

# 全局共享的 GameService 实例
game_service = GameService()
