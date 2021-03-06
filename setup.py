from setuptools import setup, find_packages

with open("README.md", "rb") as f:
    long_description = f.read().decode("utf8")


setup(
    name="ParameterChecker",
    version="0.0.5",
    author="lipo",
    author_email="lipo8081@gmail.com",
    description="Parameter manager system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lipopo/pchecker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires='>3.0'
)
