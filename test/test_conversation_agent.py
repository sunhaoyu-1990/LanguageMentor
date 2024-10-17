import unittest
from unittest.mock import patch, mock_open
from src.agents.agent_base import AgentBase  # 确保正确的模块路径
from src.agents.conversation_agent import ConversationAgent  # 假设文件名为 conversation_agent.py

class TestConversationAgent(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="This is a test prompt.")
    @patch('src.agents.agent_base.ChatPromptTemplate')  # 确保路径正确
    @patch('src.agents.agent_base.ChatOllama')  # 确保路径正确
    def test_initialization_with_session(self, mock_chat_ollama, mock_chat_prompt_template, mock_file):
        """
        测试带有 session_id 的 ConversationAgent 初始化
        """
        # 设置 ChatPromptTemplate 的返回值
        mock_chat_prompt_template.from_messages.return_value = mock_chat_prompt_template
        
        # 测试代理初始化时传入 session_id
        agent = ConversationAgent(session_id="test_session")
        
        # 验证父类初始化被正确调用
        self.assertEqual(agent.name, "conversation")
        self.assertEqual(agent.prompt_file, "prompts/conversation_prompt.txt")
        self.assertEqual(agent.session_id, "test_session")
        
        # 验证 ChatPromptTemplate 的调用
        mock_chat_prompt_template.from_messages.assert_called_once()
        
    @patch('builtins.open', new_callable=mock_open, read_data="This is a test prompt.")
    @patch('src.agents.agent_base.ChatPromptTemplate')  # 确保路径正确
    @patch('src.agents.agent_base.ChatOllama')  # 确保路径正确
    def test_initialization_without_session(self, mock_chat_ollama, mock_chat_prompt_template, mock_file):
        """
        测试不带有 session_id 的 ConversationAgent 初始化
        """
        mock_chat_prompt_template.from_messages.return_value = mock_chat_prompt_template
        
        agent = ConversationAgent()  # 不传入 session_id
        
        # 验证父类初始化被正确调用
        self.assertEqual(agent.name, "conversation")
        self.assertEqual(agent.prompt_file, "prompts/conversation_prompt.txt")
        self.assertEqual(agent.session_id, "conversation")  # 默认 session_id 应该是 name
        
        # 验证 ChatPromptTemplate 的调用
        mock_chat_prompt_template.from_messages.assert_called_once()
        
    @patch('builtins.open', new_callable=mock_open, read_data="This is a test prompt.")
    @patch('src.agents.agent_base.ChatPromptTemplate')  # 确保路径正确
    def test_prompt_loading(self, mock_chat_prompt_template, mock_file):
        """
        测试 ConversationAgent 是否正确加载了 prompt 文件
        """
        mock_chat_prompt_template.from_messages.return_value = mock_chat_prompt_template
        
        agent = ConversationAgent()
        
        # 验证 prompt 文件是否被正确加载
        mock_file.assert_called_once_with("prompts/conversation_prompt.txt", "r", encoding="utf-8")
        self.assertEqual(agent.prompt, "This is a test prompt.")

if __name__ == '__main__':
    unittest.main()
