import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="byzvis",
    version="0.1.0",
    author="Rodolfo Pereira Araujo",
    author_email="rodolfo.pereira@ime.uerj.br",
    description="Byzantine problem visualizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rodoufu/byzvis",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
