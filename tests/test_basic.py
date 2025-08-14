#!/usr/bin/env python3
"""
Basic tests for XorLang interpreter
"""

import unittest
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import xorlang


class TestXorLangBasics(unittest.TestCase):
    """Test basic XorLang functionality."""
    
    def test_arithmetic(self):
        """Test basic arithmetic operations."""
        result, error = xorlang.run_code("2 + 3;")
        self.assertIsNone(error)
        self.assertEqual(result, 5)
        
        result, error = xorlang.run_code("10 - 4;")
        self.assertIsNone(error)
        self.assertEqual(result, 6)
        
        result, error = xorlang.run_code("3 * 4;")
        self.assertIsNone(error)
        self.assertEqual(result, 12)
        
        result, error = xorlang.run_code("15 / 3;")
        self.assertIsNone(error)
        self.assertEqual(result, 5.0)
    
    def test_variables(self):
        """Test variable declaration and assignment."""
        result, error = xorlang.run_code("var x = 42; x;")
        self.assertIsNone(error)
        self.assertEqual(result, 42)
        
        result, error = xorlang.run_code("var y; y = 10; y;")
        self.assertIsNone(error)
        self.assertEqual(result, 10)
    
    def test_strings(self):
        """Test string operations."""
        result, error = xorlang.run_code('"Hello, World!";')
        self.assertIsNone(error)
        self.assertEqual(result, "Hello, World!")
        
        result, error = xorlang.run_code('"Hello" + " " + "World";')
        self.assertIsNone(error)
        self.assertEqual(result, "Hello World")
    
    def test_functions(self):
        """Test function definition and calling."""
        code = """
        func add(a, b) {
            return a + b;
        }
        add(5, 3);
        """
        result, error = xorlang.run_code(code)
        self.assertIsNone(error)
        self.assertEqual(result, 8)
    
    def test_classes(self):
        """Test class definition and member access."""
        code = """
        class Math {
            func multiply(a, b) {
                return a * b;
            }
        }
        Math.multiply(4, 5);
        """
        result, error = xorlang.run_code(code)
        self.assertIsNone(error)
        self.assertEqual(result, 20)
    
    def test_control_flow(self):
        """Test if statements."""
        code = """
        var x = 10;
        if (x > 5) {
            x = x * 2;
        }
        x;
        """
        result, error = xorlang.run_code(code)
        self.assertIsNone(error)
        self.assertEqual(result, 20)
    
    def test_loops(self):
        """Test for loops."""
        code = """
        var sum = 0;
        for (var i = 1; i <= 5; i = i + 1) {
            sum = sum + i;
        }
        sum;
        """
        result, error = xorlang.run_code(code)
        self.assertIsNone(error)
        self.assertEqual(result, 15)  # 1+2+3+4+5 = 15
    
    def test_tokenizer(self):
        """Test the tokenizer directly."""
        tokens, error = xorlang.tokenize("var x = 42;")
        self.assertIsNone(error)
        self.assertGreater(len(tokens), 0)
        
        # Check some token types
        token_types = [token.type for token in tokens]
        self.assertIn('KEYWORD', token_types)  # 'var'
        self.assertIn('IDENTIFIER', token_types)  # 'x'
        self.assertIn('EQ', token_types)  # '='
        self.assertIn('INT', token_types)  # '42'
    
    def test_parser(self):
        """Test the parser directly."""
        tokens, _ = xorlang.tokenize("var x = 42;")
        parse_result = xorlang.parse(tokens)
        self.assertIsNone(parse_result.error)
        self.assertIsNotNone(parse_result.node)


class TestXorLangErrors(unittest.TestCase):
    """Test error handling in XorLang."""
    
    def test_syntax_error(self):
        """Test syntax error handling."""
        result, error = xorlang.run_code("var x = ;")  # Missing value
        self.assertIsNotNone(error)
        self.assertIn("Syntax", error)
    
    def test_undefined_variable(self):
        """Test undefined variable error."""
        result, error = xorlang.run_code("undefined_var;")
        self.assertIsNotNone(error)
        self.assertIn("Undefined variable", error)
    
    def test_division_by_zero(self):
        """Test division by zero error."""
        result, error = xorlang.run_code("10 / 0;")
        self.assertIsNotNone(error)
        self.assertIn("Division by zero", error)


if __name__ == '__main__':
    unittest.main()
