from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name="openspeechlib",
    version="0.0.0",
    description="Useful libraries to process and generate speech",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/open-speech-org/openspeech",
    keyboards="speech processing",
    author="contraslash S.A.S.",
    author_email='ma0@contraslash.com',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    license="MIT",
    install_requires=[
        "requests>=2.22.0"
    ],
    packages=[
        "openspeechlib",
    ],
    scripts=[

    ],
    zip_safe=False,
    include_package_data=True,
    project_urls={
        "Bug Reports": "https://github.com/open-speech-org/openspeech/issues",
        "Source": "https://github.com/open-speech-org/openspeech",
        "Contraslash": "https://contraslash.com/"
    },
)
