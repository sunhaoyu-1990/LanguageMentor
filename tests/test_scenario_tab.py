import unittest
from unittest.mock import patch, mock_open
import gradio as gr
from src.tabs.scenario_tab import (
    start_new_scenario_chatbot,
    get_page_desc,
    handle_scenario,
    create_scenario_tab,
)
from src.agents.scenario_agent import ScenarioAgent


class TestScenarioTab(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="This is a test scenario introduction.")
    def test_get_page_desc_success(self, mock_file):
        # 测试成功加载文件
        result = get_page_desc('job_interview')
        self.assertEqual(result, "This is a test scenario introduction.")

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('src.utils.logger.LOG.error')
    def test_get_page_desc_file_not_found(self, mock_log_error, mock_open_file):
        # 测试文件不存在时的情况
        result = get_page_desc('non_existent_scenario')
        self.assertEqual(result, "场景介绍文件未找到。")
        mock_log_error.assert_called_once_with("场景介绍文件 content/page/non_existent_scenario.md 未找到！")

    @patch.object(ScenarioAgent, 'start_new_session', return_value="Hello from AI!")
    def test_start_new_scenario_chatbot(self, mock_start_session):
        # 测试是否能正确初始化新的Chatbot
        chatbot = start_new_scenario_chatbot('job_interview')
        self.assertIsInstance(chatbot, gr.Chatbot)
        
        # 修正这里的预期返回值格式，使用元组而非列表
        self.assertEqual(chatbot.value, [[None, "Hello from AI!"]])
        self.assertEqual(chatbot.height, 600)

    @patch.object(ScenarioAgent, 'chat_with_history', return_value="AI response")
    @patch('src.utils.logger.LOG.info')
    def test_handle_scenario(self, mock_log_info, mock_chat_with_history):
        # 测试是否调用了代理的 chat_with_history 并正确返回响应
        result = handle_scenario("user input", [], "job_interview")
        self.assertEqual(result, "AI response")
        mock_chat_with_history.assert_called_once_with("user input")
        mock_log_info.assert_called_once_with("[ChatBot]: AI response")

    def test_create_scenario_tab(self):
        # 测试 Gradio 界面组件是否正确创建
        with gr.Blocks() as demo:
            create_scenario_tab()

        # 查找组件
        tab_component = None
        chatbot_component = None
        radio_component = None

        for component in demo.blocks.values():
            if isinstance(component, gr.Tab):
                tab_component = component
            elif isinstance(component, gr.Chatbot):
                chatbot_component = component
            elif isinstance(component, gr.Radio):
                radio_component = component

        self.assertIsNotNone(tab_component)
        self.assertIsNotNone(chatbot_component)
        self.assertIsNotNone(radio_component)
        self.assertEqual(chatbot_component.height, 600)


if __name__ == '__main__':
    unittest.main()
