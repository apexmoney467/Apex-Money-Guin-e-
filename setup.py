from setuptools import setup, find_packages

setup(
    name="apex-money-gn",
    version="1.0.0",
    description="APEX Money Guinée - Flask API for Orange Money + MTN MoMo",
    author="APEX Money",
    packages=find_packages(),
    install_requires=[
        "Flask==3.0.2",
        "cinetpay-sdk==1.0.0",
        "python-dotenv==1.0.1",
    ],
    python_requires=">=3.8",
)
