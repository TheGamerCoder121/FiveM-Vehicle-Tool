from setuptools import setup, find_packages

setup(
    name="gta-meta-tool",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'lxml',
    ],
    entry_points={
        'console_scripts': [
            'gta-meta-tool=meta_tool.cli:cli',
        ],
    },
    python_requires='>=3.8',
    author="Devin",
    description="GTA V FiveM Meta File Conflict Resolution Tool",
    keywords="gta5,fivem,modding,tools",
    project_urls={
        "Source": "https://github.com/username/gta-meta-tool",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
