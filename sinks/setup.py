from setuptools import setup, find_packages

requirements = [
    "loguru==0.5.3",
    "click==7.1.2"
]

setup(
    author="Breno Costa",
    author_email="brenoccosta7@gmail.com",
    python_requires=">=3.7",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    name="sinks",
    description="Feature Store Sinks",
    version="0.1.0",
    keywords="sinks",
    packages=find_packages(
        include=["sinks", "sinks.*"],
        exclude=["tests*"]
    ),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sinks = sinks.cli:run_sinks"
        ]
    }
)
