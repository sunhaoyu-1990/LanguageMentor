import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.agents.agent_base import AgentBase  # 假设您的代码模块为 your_module

class TestAgentBase(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='Test Prompt')
    def test_load_prompt(self, mock_file):
        agent = AgentBase(name="test_agent", prompt_file="prompt.txt")
        self.assertEqual(agent.prompt, 'Test Prompt')
        mock_file.assert_called_once_with("prompt.txt", "r", encoding="utf-8")

    @patch('builtins.open', new_callable=mock_open)
    def test_load_intro(self, mock_file):
        # 模拟文件的不同读取内容：先读取 prompt.txt，后读取 intro.json
        mock_file.side_effect = [
            mock_open(read_data="Test Prompt").return_value,
            mock_open(read_data='{"messages": "Test Intro"}').return_value
        ]

        agent = AgentBase(name="test_agent", prompt_file="prompt.txt", intro_file="intro.json")
        self.assertEqual(agent.intro_messages, {"messages": "Test Intro"})
        # 验证文件的调用
        mock_file.assert_any_call("prompt.txt", "r", encoding="utf-8")
        mock_file.assert_any_call("intro.json", "r", encoding="utf-8")

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_prompt_file_not_found(self, mock_file):
        with self.assertRaises(FileNotFoundError):
            AgentBase(name="test_agent", prompt_file="non_existent_prompt.txt")

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_intro_file_not_found(self, mock_file):
        with self.assertRaises(FileNotFoundError):
            AgentBase(name="test_agent", prompt_file="prompt.txt", intro_file="non_existent_intro.json")

    @patch('builtins.open', new_callable=mock_open, read_data='Invalid JSON')
    def test_load_intro_invalid_json(self, mock_file):
        with self.assertRaises(ValueError):
            AgentBase(name="test_agent", prompt_file="prompt.txt", intro_file="invalid_intro.json")

    @patch('src.agents.agent_base.ChatOllama')  # 假设你在某个模块中导入了 ChatOllama
    @patch('src.agents.agent_base.ChatPromptTemplate')
    @patch('src.agents.agent_base.MessagesPlaceholder')
    @patch('builtins.open', new_callable=mock_open, read_data='Test Prompt')  # 模拟prompt.txt读取
    def test_create_chatbot(self, mock_file, mock_messages_placeholder, mock_chat_prompt_template, mock_chat_ollama):
        mock_chat_ollama.return_value = MagicMock()
        mock_chat_prompt_template.from_messages.return_value = mock_chat_ollama

        agent = AgentBase(name="test_agent", prompt_file="prompt.txt")
        agent.create_chatbot()

        mock_chat_ollama.assert_called()
        mock_chat_prompt_template.from_messages.assert_called()
        mock_file.assert_called_once_with("prompt.txt", "r", encoding="utf-8")

    @patch('src.agents.agent_base.RunnableWithMessageHistory.invoke', return_value=MagicMock(content="Test response"))
    @patch('src.agents.agent_base.LOG')  # 假设LOG是你日志记录模块的一部分
    @patch('builtins.open', new_callable=mock_open, read_data="Test Prompt")  # 模拟文件读取
    def test_chat_with_history(self, mock_file, mock_log, mock_invoke):
        agent = AgentBase(name="test_agent", prompt_file="prompt.txt")
        response = agent.chat_with_history("Hello")

        mock_invoke.assert_called_once()
        self.assertEqual(response, "Test response")

        mock_log.debug.assert_called()

if __name__ == '__main__':
    unittest.main()
