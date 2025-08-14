#!/usr/bin/env python3
"""
XorLang Programming Language
Setup script for installation and distribution
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        return f.read()

setup(
    name="xorlang",
    version="1.0.0",
    description="XorLang Programming Language Interpreter",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Ali Jafari",
    author_email="your.email@example.com",
    url="https://github.com/Mr-Ali-Jafari/Xorlang",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "xorlang": ["stdlib/*.xor", "stdlib/**/*.xor"],
    },
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        # Add any external dependencies here
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "gui": [
            "tkinter",  # Usually included with Python
        ],
    },
    entry_points={
        "console_scripts": [
            "xorlang=xorlang.cli:main",
            "xorlang-ide=xorlang.ide:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: Compilers",
    ],
    keywords="programming-language interpreter lexer parser xorlang",
)
