import unittest
from unittest.mock import patch
from langchain_core.chat_history import InMemoryChatMessageHistory
from src.agents.session_history import get_session_history, store  # 假设该代码存储在 session_history.py 文件中
from langchain_core.messages import HumanMessage

class TestGetSessionHistory(unittest.TestCase):
    
    def setUp(self):
        """
        在每个测试之前，清空存储，以确保不会有历史数据污染测试。
        """
        store.clear()

    def test_new_session_history(self):
        """
        测试当提供一个新的会话ID时，是否会创建一个新的聊天历史对象。
        """
        session_id = "test_session"
        
        # 调用函数并获取会话历史
        history = get_session_history(session_id)
        
        # 验证返回的对象类型
        self.assertIsInstance(history, InMemoryChatMessageHistory)
        
        # 验证该会话ID已经存储在 store 中
        self.assertIn(session_id, store)
        self.assertIs(store[session_id], history)

    def test_existing_session_history(self):
        """
        测试当会话ID已经存在时，是否会返回已存储的聊天历史对象。
        """
        session_id = "existing_session"
        
        # 先人为创建并存储一个历史记录
        store[session_id] = InMemoryChatMessageHistory()
        
        # 调用函数并获取会话历史
        history = get_session_history(session_id)
        
        # 验证返回的对象是存储的同一个对象
        self.assertIs(history, store[session_id])

    def test_different_sessions(self):
        """
        测试多个不同的会话ID是否会返回不同的聊天历史对象。
        """
        session_id1 = "session_1"
        session_id2 = "session_2"
        
        # 获取两个不同会话的历史记录
        history1 = get_session_history(session_id1)
        history2 = get_session_history(session_id2)
        
        ## 向每个历史对象添加一条不同的消息
        history1.add_message(HumanMessage(content="Message for session 1"))
        history2.add_message(HumanMessage(content="Message for session 2"))
        
        # 验证两个会话的历史记录是不同的对象
        self.assertNotEqual(history1, history2)
        
        # 验证消息内容不同
        self.assertNotEqual(history1.messages, history2.messages)

if __name__ == '__main__':
    unittest.main()
