import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylic",
    version="0.0.1",
    author="Sandro Huber",
    author_email="sandrochuber@gmail.com",
    description="Python license checker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sandrochuber/pylic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
