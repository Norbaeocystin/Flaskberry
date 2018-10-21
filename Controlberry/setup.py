import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="controlberry_pkg",
    version="0.0.1",
    author="Rastislav_Baran",
    author_email="baranrastislav@gmail.com",
    description="Package which needs to be installed on Raspberry Pi 3 to control it via Flaskberry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

