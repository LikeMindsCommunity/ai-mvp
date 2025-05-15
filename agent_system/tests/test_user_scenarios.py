"""
Test user scenarios for agent interactions.

These tests simulate real-world user questions and verify
that agents provide appropriate responses.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agent_system.deploy_experiment import DeploymentExperiment


class TestUserScenarios(unittest.TestCase):
    """
    Tests that simulate real-world user scenarios.
    """
    
    @patch('agent_system.deploy_experiment.Gemini')
    @patch('agent_system.deploy_experiment.Agent')
    def test_basic_flutter_questions(self, mock_agent_class, mock_gemini_class):
        """
        Test handling of common Flutter questions.
        """
        # Setup mocks
        mock_gemini_instance = MagicMock()
        mock_gemini_class.return_value = mock_gemini_instance
        
        mock_agent_instance = MagicMock()
        
        # Define expected responses for various user scenarios
        scenarios = {
            "What's Flutter?": "Flutter is a UI toolkit from Google for building natively compiled applications.",
            "How do I install Flutter?": "To install Flutter, download the SDK from flutter.dev and add it to your PATH.",
            "What are Flutter widgets?": "Widgets are the basic building blocks of Flutter UI, similar to components in React.",
            "Is Flutter better than React Native?": "Both have strengths and weaknesses. Flutter offers great performance..."
        }
        
        def side_effect_func(query, **kwargs):
            for key, response in scenarios.items():
                if key.lower() in query.lower():
                    return response
            return "I need more information to answer that question."
            
        mock_agent_instance.run.side_effect = side_effect_func
        mock_agent_class.return_value = mock_agent_instance
        
        # Create the experiment object
        experiment = DeploymentExperiment()
        
        # Test each scenario
        for question, expected_answer in scenarios.items():
            response = experiment.analyze_flutter_integration(question)
            self.assertEqual(response, expected_answer)
    
    @patch('agent_system.deploy_experiment.Gemini')
    @patch('agent_system.deploy_experiment.Agent')
    def test_likeminds_integration_questions(self, mock_agent_class, mock_gemini_class):
        """
        Test responses to questions about LikeMinds integration.
        """
        # Setup mocks
        mock_gemini_instance = MagicMock()
        mock_gemini_class.return_value = mock_gemini_instance
        
        mock_agent_instance = MagicMock()
        
        # Define question and expected response templates
        integration_scenarios = {
            "How do I integrate LikeMinds Chat SDK?": 
                "To integrate LikeMinds Chat SDK, first add the dependency to your pubspec.yaml file...",
            "How do I customize the theme in LikeMinds?": 
                "To customize the theme in LikeMinds, you need to create a ThemeData object...",
            "What's the difference between LikeMinds Chat and Feed?": 
                "LikeMinds Chat focuses on real-time messaging capabilities, while Feed is designed for social media..."
        }
        
        def side_effect_func(query, **kwargs):
            for key, response in integration_scenarios.items():
                if key.lower() in query.lower():
                    return response
            return "I don't have specific information about that LikeMinds feature."
            
        mock_agent_instance.run.side_effect = side_effect_func
        mock_agent_class.return_value = mock_agent_instance
        
        # Create the experiment object
        experiment = DeploymentExperiment()
        
        # Test each integration scenario
        for question, expected_answer in integration_scenarios.items():
            response = experiment.analyze_flutter_integration(question)
            self.assertEqual(response, expected_answer)
    
    @patch('agent_system.deploy_experiment.Gemini')
    @patch('agent_system.deploy_experiment.Agent')
    def test_error_handling(self, mock_agent_class, mock_gemini_class):
        """
        Test how the agent handles errors and edge cases.
        """
        # Setup mocks
        mock_gemini_instance = MagicMock()
        mock_gemini_class.return_value = mock_gemini_instance
        
        mock_agent_instance = MagicMock()
        
        # Test empty or vague questions
        edge_cases = {
            "": "I need more information to answer your question about Flutter integration.",
            "help": "I'd be happy to help! What specific aspect of Flutter or LikeMinds integration do you need assistance with?",
            "???": "I'm not sure what you're asking. Could you please provide more details about your Flutter question?",
            "12345": "I don't understand what you mean by '12345'. Could you please clarify your question about Flutter integration?"
        }
        
        def side_effect_func(query, **kwargs):
            if not query or query.isspace():
                return edge_cases[""]
            
            for key, response in edge_cases.items():
                if key == query:
                    return response
            
            return "I'll need more specific information to help you with that."
            
        mock_agent_instance.run.side_effect = side_effect_func
        mock_agent_class.return_value = mock_agent_instance
        
        # Create the experiment object
        experiment = DeploymentExperiment()
        
        # Test each edge case
        for question, expected_answer in edge_cases.items():
            response = experiment.analyze_flutter_integration(question)
            self.assertEqual(response, expected_answer)


if __name__ == '__main__':
    unittest.main() 