import setuptools  # type: ignore
import toml

with open("README.md", "r") as readme_file:
    readme_content = readme_file.read()

with open("pyproject.toml") as pyproject_file:
    pyproject_content = toml.load(pyproject_file)
    version = pyproject_content["tool"]["poetry"]["version"]

setuptools.setup(
    name="pylic",
    version=version,
    description="A Python license checker",
    author="Sandro Huber",
    author_email="sandrochuber@gmail.com",
    url="https://github.com/sandrochuber/pylic",
    packages=["pylic"],
    license="MIT",
    long_description=readme_content,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    install_requires=["toml", "importlib-metadata"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    entry_points={"console_scripts": ["pylic=pylic.pylic:main"]},
)
