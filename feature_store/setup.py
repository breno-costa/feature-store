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
    name="feature_store",
    description="Feature Store",
    version="0.1.0",
    keywords="feature_store",
    packages=find_packages(
        include=["feature_store", "feature_store.*"],
        exclude=["tests*"]
    ),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "feature_store = feature_store.cli:run"
        ]
    }
)
