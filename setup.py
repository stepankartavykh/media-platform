from setuptools import setup

requires_packages = [
    'python-telegram-bot[job-queue]',
    'requests',
    'aiohttp',
    'beautifulsoup4',
    'python-dotenv',
]

setup(
    version='1.0',
    install_requires=requires_packages,
)
