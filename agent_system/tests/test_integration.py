"""
Integration tests for agent interactions.

These tests verify that the different agents can work together
and interact correctly with external systems.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import asyncio

# Add the parent directory to sys.path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agent_system.hello_world import run_hello_world
from agent_system.deploy_experiment import DeploymentExperiment


class TestAgentIntegration(unittest.TestCase):
    """
    Integration tests for agent interactions.
    """
    
    @patch('agent_system.hello_world.Gemini')
    @patch('agent_system.deploy_experiment.Gemini')
    @patch('agent_system.hello_world.Agent')
    @patch('agent_system.deploy_experiment.Agent')
    def test_agent_coordination(self, mock_deploy_agent_class, mock_hello_agent_class,
                               mock_deploy_gemini_class, mock_hello_gemini_class):
        """
        Test that agents can coordinate and share information.
        """
        # Setup mock Gemini for both agents
        mock_hello_gemini_instance = MagicMock()
        mock_hello_gemini_class.return_value = mock_hello_gemini_instance
        
        mock_deploy_gemini_instance = MagicMock()
        mock_deploy_gemini_class.return_value = mock_deploy_gemini_instance
        
        # Setup mock Agent responses
        mock_hello_agent_instance = MagicMock()
        mock_hello_response = "Flutter is a UI toolkit for building natively compiled applications"
        mock_hello_agent_instance.run.return_value = mock_hello_response
        mock_hello_agent_class.return_value = mock_hello_agent_instance
        
        mock_deploy_agent_instance = MagicMock()
        mock_deploy_response = "To implement Flutter with a custom theme, follow these steps..."
        mock_deploy_agent_instance.run.return_value = mock_deploy_response
        mock_deploy_agent_class.return_value = mock_deploy_agent_instance
        
        # Execute the hello_world agent to get Flutter information
        flutter_info = run_hello_world()
        
        # Create deployment experiment to use the Flutter info
        experiment = DeploymentExperiment()
        integration_query = f"Based on this info '{flutter_info}', how would I implement a custom theme?"
        integration_response = experiment.analyze_flutter_integration(integration_query)
        
        # Verify the expected interactions
        mock_hello_agent_instance.run.assert_called_once()
        mock_deploy_agent_instance.run.assert_called_once()
        
        # Check that the correct query was passed with the information from the first agent
        args, kwargs = mock_deploy_agent_instance.run.call_args
        self.assertIn(mock_hello_response, args[0])
        self.assertEqual(integration_response, mock_deploy_response)


class TestEndToEndFlow(unittest.TestCase):
    """
    Tests for end-to-end flows involving multiple agents and external services.
    """
    
    @patch('agent_system.deploy_experiment.Gemini')
    @patch('agent_system.deploy_experiment.Agent')
    def test_async_workflow(self, mock_agent_class, mock_gemini_class):
        """
        Test an asynchronous workflow that simulates a real user interaction flow.
        """
        # Setup mocks
        mock_gemini_instance = MagicMock()
        mock_gemini_class.return_value = mock_gemini_instance
        
        mock_agent_instance = MagicMock()
        mock_responses = {
            "How would I integrate LikeMinds chat SDK into a Flutter application?": 
                "First, add the LikeMinds dependency to your pubspec.yaml...",
            "What are the best practices for error handling?": 
                "For error handling in Flutter, use try/catch blocks..."
        }
        
        def side_effect_func(query, **kwargs):
            for key in mock_responses:
                if key in query:
                    return mock_responses[key]
            return "I don't have an answer for that specific question."
            
        mock_agent_instance.run.side_effect = side_effect_func
        mock_agent_class.return_value = mock_agent_instance
        
        # Create the experiment object
        experiment = DeploymentExperiment()
        
        # Test a sequence of related questions in a workflow
        response1 = experiment.analyze_flutter_integration(
            "How would I integrate LikeMinds chat SDK into a Flutter application?"
        )
        self.assertEqual(response1, mock_responses["How would I integrate LikeMinds chat SDK into a Flutter application?"])
        
        # Test a follow-up question using the async_test decorator
        @async_test
        async def test_follow_up():
            response2 = await experiment.analyze_flutter_integration_async(
                "What are the best practices for error handling?"
            )
            self.assertEqual(response2, mock_responses["What are the best practices for error handling?"])
            
        # Run the async test
        test_follow_up()


def async_test(coro):
    """
    Decorator for async test methods.
    """
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()
    return wrapper


if __name__ == '__main__':
    unittest.main() 