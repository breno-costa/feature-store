from setuptools import setup, find_packages

requirements = [
    "fastapi==0.63.0",
    "uvicorn[standard]==0.13.3",
    "loguru==0.5.3",
    "odmantic"
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
    name="registry",
    description="Feature Store Registry",
    version="0.1.0",
    keywords="registry",
    packages=find_packages(
        include=["registry", "registry.*"],
        exclude=["tests*"]
    ),
    install_requires=requirements
)
