import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flaskberry",
    version="0.0.1",
    author="Rastislav_Baran",
    author_email="baranrastislav@gmail.com",
    description="Flaskberry web app to control Raspberry Pi with Controlberry",
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
