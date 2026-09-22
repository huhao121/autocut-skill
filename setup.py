from setuptools import setup, find_packages

setup(
    name="autocut-skill",
    version="0.1.0",
    author="huhao121",
    description="A zero-drift, Markdown-driven video cut engine & Agent skill. Built on top of AutoCut's philosophy, rewritten with native FFmpeg FilterGraph.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/huhao121/autocut-skill",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "srt>=3.5.0",
    ],
    entry_points={
        "console_scripts": [
            "autocut-skill=autocut_skill.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Video",
    ],
)
