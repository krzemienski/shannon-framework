"""Shannon Framework - Advanced information processing system."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="shannon-framework",
    version="0.1.0",
    author="Shannon Framework Contributors",
    author_email="",
    description="Advanced information processing framework with parallel computation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/shannon-framework",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0,<2.0.0",
        "pytest>=7.0.0",
        "pytest-asyncio>=0.21.0",
        "psutil>=5.9.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "mypy>=1.0.0",
            "ruff>=0.0.254",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "shannon=shannon.cli:main",
        ],
    },
)