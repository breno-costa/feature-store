from setuptools import setup, find_packages

requirements = [
    "kafka-python==2.0.2",
    "loguru==0.5.3",
    "click==7.1.2"
]

setup(
    author="Breno Costa",
    email="brenoccosta7@gmail.com",
    python_requires=">=3.8",
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
    ],
    name="producer",
    description="Data producer to kafka",
    version="0.1.0",
    keywords="producer",
    packages=find_packages(
        include=["producer", "producer.*"],
        exclude=["tests*"]
    ),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "producer = producer.cli:run"
        ]
    }
)
