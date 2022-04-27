import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyeiote",
    version="0.2.1",
    author="Craig Koroscil",
    author_email="ckoroscil@circadence.com",
    description="A simple enterprise IoT traffic emulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ckoroscil/pyeiote",
    project_urls={
        "Bug Tracker": "https://github.com/ckoroscil/pyeiote/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'PyYAML==6.0',
        'scapy @ git+https://github.com/secdev/scapy@eb1e56d676c78ccbd5a3c820b931ac50f6a5a4f8'
    ],
    package_data={'': ['config.yaml']},
    include_package_data=True
)
