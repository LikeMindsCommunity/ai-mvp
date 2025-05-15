"""
Test runner for agent_system.

This script sets up the Python path and runs all tests in the tests directory.
"""

import unittest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import test modules
from agent_system.tests.test_hello_world import TestHelloWorld
from agent_system.tests.test_deploy_experiment import TestDeploymentExperiment
from agent_system.tests.test_integration import TestAgentIntegration, TestEndToEndFlow
from agent_system.tests.test_user_scenarios import TestUserScenarios

if __name__ == '__main__':
    # Create a test loader
    test_loader = unittest.TestLoader()
    
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestHelloWorld))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestDeploymentExperiment))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestAgentIntegration))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestEndToEndFlow))
    test_suite.addTests(test_loader.loadTestsFromTestCase(TestUserScenarios))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite) 