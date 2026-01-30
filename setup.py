from setuptools import setup, find_packages

setup(
    name="blm-financial-report-analysis",
    version="0.1.0",
    description="Bureau of Land Management Financial Report Analysis Tool",
    author="BLM Financial Analysis Team",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "openpyxl>=3.1.0",
        "tabula-py>=2.7.0",
        "pdfplumber>=0.9.0",
        "jinja2>=3.1.0",
        "click>=8.1.0",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "blm-analyze=src.main:cli",
        ],
    },
)
