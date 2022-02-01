
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
long_description = (Path(__file__).parent / "readme.md").read_text()

setup(
    name="rpi_ws281x_hub",
    version="1.0.3",
    author="Thomas Vincent",
    author_email="vrince@gmail.com",
    license="MIT",
    packages=find_packages(),
    description="Raspberry Pi - WS281x Led hub 🎨",
    url="https://github.com/vrince/rpi-ws281x-hub",
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_data={
        'rpi_ws281x_hub': [
            'index.html',
            'variables.scss',
            'rpi-ws281x-hub.service'
            ],
        'images': [
            '*.png'
        ]
    },
    install_requires=[
        'fastapi==0.70.0',
        'uvicorn[standard]==0.15.0',
        'click==8.0.3',
        'appdirs==1.4.4',
        'colour==0.1.5',
        'easing-functions==1.0.4'
    ],
    entry_points={
    'console_scripts': [
        'rpi-ws281x-hub = rpi_ws281x_hub.api:cli',
        'rpi-ws281x-hub.service = rpi_ws281x_hub.service:cli'
    ]
}
)