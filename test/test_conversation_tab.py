import unittest
from unittest.mock import patch, MagicMock
import gradio as gr
from src.tabs.conversation_tab import handle_conversation, create_conversation_tab
from src.agents.conversation_agent import ConversationAgent

class TestConversationTab(unittest.TestCase):

    @patch('src.tabs.conversation_tab.conversation_agent')
    @patch('src.tabs.conversation_tab.LOG')
    def test_handle_conversation(self, mock_log, mock_conversation_agent):
        """
        测试 handle_conversation 函数是否正确处理用户输入并调用 ConversationAgent。
        """
        # 模拟 conversation_agent 的 chat_with_history 方法
        mock_conversation_agent.chat_with_history.return_value = "Mocked bot response"

        # 模拟用户输入和历史记录
        user_input = "Hello, how are you?"
        chat_history = []

        # 调用 handle_conversation
        response = handle_conversation(user_input, chat_history)

        # 确保 conversation_agent.chat_with_history 被调用一次
        mock_conversation_agent.chat_with_history.assert_called_once_with(user_input)

        # 确保返回了正确的聊天机器人回复
        self.assertEqual(response, "Mocked bot response")

        # 更新日志信息的期望值，匹配实际输出
        mock_log.info.assert_called_once_with("[Conversation ChatBot]: Mocked bot response")

    def test_create_conversation_tab(self):
        """
        测试 create_conversation_tab 函数是否正确创建 Gradio 界面组件。
        """
        with gr.Blocks() as demo:
            create_conversation_tab()

        # 打印调试输出，查看 demo.blocks 里创建的组件
        # print(f"Blocks created: {demo.blocks}")

        # 查找创建的 Chatbot 和 ChatInterface 组件
        chatbot_component = None
        for component in demo.blocks.values():  # 通过 blocks.values() 遍历所有组件
            if isinstance(component, gr.Chatbot):
                chatbot_component = component

        # 检查是否正确创建了 Chatbot 组件
        self.assertIsNotNone(chatbot_component, "Chatbot component was not found")
        self.assertEqual(chatbot_component.placeholder, "<strong>你的英语私教 DjangoPeng</strong><br><br>想和我聊什么话题都可以，记得用英语哦！")
        self.assertEqual(chatbot_component.height, 800)

if __name__ == '__main__':
    unittest.main()
