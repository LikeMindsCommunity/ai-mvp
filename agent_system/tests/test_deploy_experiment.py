"""
Unit tests for the deploy_experiment.py module.
"""

import unittest
import asyncio
from unittest.mock import patch, MagicMock

# Fix import path - import directly from the module
import sys
import os

# Add the parent directory to sys.path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agent_system.deploy_experiment import DeploymentExperiment

class TestDeploymentExperiment(unittest.TestCase):
    """
    Test cases for the DeploymentExperiment class.
    """
    
    @patch('agent_system.deploy_experiment.Gemini')
    @patch('agent_system.deploy_experiment.Agent')
    def test_init(self, mock_agent_class, mock_gemini_class):
        """
        Test that DeploymentExperiment initializes with the expected configuration.
        """
        # Setup mock Gemini
        mock_gemini_instance = MagicMock()
        mock_gemini_class.return_value = mock_gemini_instance
        
        # Setup mock Agent
        mock_agent_class.return_value = MagicMock()
        
        # Create instance
        experiment = DeploymentExperiment()
        
        # Verify Agent was created with expected parameters
        mock_agent_class.assert_called_once()
        
        # Extract the call arguments
        _, kwargs = mock_agent_class.call_args
        
        # Verify expected configuration
        self.assertEqual(kwargs['description'], "You are a Flutter integration expert assistant.")
        self.assertIn("Think step by step", kwargs['instructions'][0])
        self.assertTrue(kwargs['markdown'])
    
    @patch('agent_system.deploy_experiment.Gemini')
    @patch('agent_system.deploy_experiment.Agent')
    def test_analyze_flutter_integration(self, mock_agent_class, mock_gemini_class):
        """
        Test the synchronous analyze_flutter_integration method.
        """
        # Setup mock Gemini
        mock_gemini_instance = MagicMock()
        mock_gemini_class.return_value = mock_gemini_instance
        
        # Setup mock Agent
        mock_agent_instance = MagicMock()
        mock_agent_instance.run.return_value = "Mock response about Flutter integration"
        mock_agent_class.return_value = mock_agent_instance
        
        # Create instance and call method
        experiment = DeploymentExperiment()
        response = experiment.analyze_flutter_integration("How do I integrate feature X?")
        
        # Verify
        self.assertEqual(response, "Mock response about Flutter integration")
        mock_agent_instance.run.assert_called_once()
        
        # Verify the query is passed correctly
        args, kwargs = mock_agent_instance.run.call_args
        self.assertEqual(args[0], "How do I integrate feature X?")
        self.assertTrue(kwargs['show_full_reasoning'])
    
    @patch('agent_system.deploy_experiment.Gemini')
    @patch('agent_system.deploy_experiment.Agent')
    async def test_analyze_flutter_integration_async(self, mock_agent_class, mock_gemini_class):
        """
        Test the asynchronous analyze_flutter_integration_async method.
        """
        # Setup mock Gemini
        mock_gemini_instance = MagicMock()
        mock_gemini_class.return_value = mock_gemini_instance
        
        # Setup mock Agent
        mock_agent_instance = MagicMock()
        mock_agent_instance.run.return_value = "Mock async response"
        mock_agent_class.return_value = mock_agent_instance
        
        # Create instance and call method
        experiment = DeploymentExperiment()
        response = await experiment.analyze_flutter_integration_async("Async question")
        
        # Verify
        self.assertEqual(response, "Mock async response")
        mock_agent_instance.run.assert_called_once()
        
        # Verify the query is passed correctly
        args, kwargs = mock_agent_instance.run.call_args
        self.assertEqual(args[0], "Async question")
        self.assertTrue(kwargs['show_full_reasoning'])

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

# Override the async test method with the decorator
TestDeploymentExperiment.test_analyze_flutter_integration_async = async_test(
    TestDeploymentExperiment.test_analyze_flutter_integration_async
)

if __name__ == '__main__':
    unittest.main() 