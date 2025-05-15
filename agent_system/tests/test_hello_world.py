"""
Unit tests for the hello_world.py module.
"""

import unittest
from unittest.mock import patch, MagicMock

import sys
import os

# Add the parent directory to sys.path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agent_system.hello_world import run_hello_world

class TestHelloWorld(unittest.TestCase):
    """
    Test cases for the hello_world.py module.
    """
    
    @patch('agent_system.hello_world.Gemini')
    @patch('agent_system.hello_world.Agent')
    def test_run_hello_world(self, mock_agent_class, mock_gemini_class):
        """
        Test that run_hello_world creates an agent and gets a response.
        
        This test mocks the Agno Agent to avoid actual API calls.
        
        Note: When run with a real model, Agno returns a RunResponse object with 
        additional metadata. Our tests expect a string response, which is what 
        we mock for testing purposes.
        """
        # Setup mock Gemini
        mock_gemini_instance = MagicMock()
        mock_gemini_class.return_value = mock_gemini_instance
        
        # Setup mock agent
        mock_agent_instance = MagicMock()
        mock_agent_instance.run.return_value = "Mock response about Flutter"
        mock_agent_class.return_value = mock_agent_instance
        
        # Run the function
        response = run_hello_world()
        
        # Assertions
        self.assertEqual(response, "Mock response about Flutter")
        mock_agent_class.assert_called_once()
        mock_agent_instance.run.assert_called_once()
        
        # Check that the prompt is as expected
        args, _ = mock_agent_instance.run.call_args
        self.assertEqual(args[0], "What is Flutter and how does it differ from other mobile app frameworks?")

if __name__ == '__main__':
    unittest.main() 