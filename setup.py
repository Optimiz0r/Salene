#!/usr/bin/env python3
"""
Setup script for SALENE (Hermes fork)
Allows traditional pip install without editable mode issues.
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='salene-agent',
    version='0.1.0',
    description='SALENE - Hermes-based neural consciousness platform',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Daniel Miller',
    url='https://github.com/Optimiz0r/Salene',
    py_modules=['run_agent', 'model_tools', 'toolsets', 'batch_runner', 
                'trajectory_compressor', 'toolset_distributions', 
                'cli', 'hermes_constants', 'hermes_state', 'hermes_time', 
                'rl_cli', 'utils', 'salene_cli'],
    packages=find_packages(include=[
        'agent', 'tools', 'tools.*', 'hermes_cli', 'gateway', 'gateway.*',
        'cron', 'acp_adapter', 'plugins', 'plugins.*'
    ]),
    python_requires='>=3.10',
    install_requires=[
        'openai>=2.21.0',
        'anthropic>=0.39.0',
        'python-dotenv>=1.2.1',
        'fire>=0.7.1',
        'httpx>=0.28.1',
        'rich>=14.3.3',
        'tenacity>=9.1.4',
        'pyyaml>=6.0.2',
        'requests>=2.33.0',
        'jinja2>=3.1.5',
        'pydantic>=2.12.5',
        'prompt_toolkit>=3.0.52',
    ],
    entry_points={
        'console_scripts': [
            'hermes=hermes_cli.main:main',
            'hermes-agent=run_agent:main',
            'salene=salene_cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
