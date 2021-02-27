import setuptools

with open("README.md", "r") as readme_file:
    readme_content = readme_file.read()

setuptools.setup(
    name="pylic",
    version="0.0.3",
    description="Python license checker",
    author="Sandro Huber",
    author_email="sandrochuber@gmail.com",
    url="https://github.com/sandrochuber/pylic",
    packages=["pylic"],
    license="MIT",
    long_description=readme_content,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
