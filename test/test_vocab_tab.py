import unittest
from unittest.mock import patch, MagicMock
import gradio as gr
from src.tabs.vocab_tab import (
    get_page_desc, restart_vocab_study_chatbot, handle_vocab, create_vocab_tab
)
from src.agents.vocab_agent import VocabAgent

class TestVocabTab(unittest.TestCase):

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data="这是词汇学习模块的介绍")
    @patch("src.tabs.vocab_tab.LOG")
    def test_get_page_desc(self, mock_log, mock_open):
        # 测试是否能正确读取文件内容
        result = get_page_desc("vocab_study")
        self.assertEqual(result, "这是词汇学习模块的介绍")

        # 测试文件不存在时是否返回默认消息
        mock_open.side_effect = FileNotFoundError
        result = get_page_desc("non_existing_feature")
        self.assertEqual(result, "词汇学习介绍文件未找到。")
        mock_log.error.assert_called_once_with("词汇学习介绍文件 content/page/non_existing_feature.md 未找到！")

    @patch.object(VocabAgent, 'chat_with_history', return_value="Mocked bot response")
    @patch.object(VocabAgent, 'restart_session')
    def test_restart_vocab_study_chatbot(self, mock_restart_session, mock_chat_with_history):
        chatbot = restart_vocab_study_chatbot()
        self.assertIsInstance(chatbot, gr.Chatbot)
        self.assertEqual(chatbot.value, [["Let's do it", "Mocked bot response"]])
        self.assertEqual(chatbot.height, 800)
        mock_restart_session.assert_called_once()
        mock_chat_with_history.assert_called_once_with("Let's do it")

    @patch.object(VocabAgent, 'chat_with_history', return_value="Mocked bot response")
    @patch("src.tabs.vocab_tab.LOG")
    def test_handle_vocab(self, mock_log, mock_chat_with_history):
        result = handle_vocab("Test input", [])
        self.assertEqual(result, "Mocked bot response")
        mock_log.info.assert_called_once_with("[Vocab ChatBot]: Mocked bot response")
        mock_chat_with_history.assert_called_once_with("Test input")

    @patch("src.tabs.vocab_tab.gr.Chatbot", wraps=gr.Chatbot)
    @patch("src.tabs.vocab_tab.gr.Markdown", wraps=gr.Markdown)
    @patch("src.tabs.vocab_tab.gr.Tab", wraps=gr.Tab)
    def test_create_vocab_tab(self, mock_tab, mock_markdown, mock_chatbot):
        # Simulate the Gradio Blocks context
        with gr.Blocks():
            # Call the function to create the vocab tab within a Blocks context
            create_vocab_tab()

        # Ensure components were created correctly
        mock_tab.assert_called_once()
        mock_markdown.assert_called()
        mock_chatbot.assert_called_once()

if __name__ == "__main__":
    unittest.main()
