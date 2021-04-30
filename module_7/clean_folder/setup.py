from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="clean_folder",
    version="0.0.1",
    author="Romanskyy Andrey",
    author_email="andrey.romanskyy@icloud.com",
    entry_points={
        'console_scripts': ['clean-folder=clean_folder.clean:main']
    },
    description="Pachage to make clear files and dirs structure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
)
