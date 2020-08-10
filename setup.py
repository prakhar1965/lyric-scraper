from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="lyric-scraper",
    version="1.0.6",
    description='A tool to get lyrics for your favourite songs',
    author='Prakhar Omar',
    author_email='praomar12@gmail.com',
    license='MIT',
    url='https://github.com/prakhar1965/lyric-scraper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["lyric_scraper"],
    install_requires=['beautifulsoup4',
                      'eyeD3',
                      'urllib3',
                      'click'],
    entry_points={
        "console_scripts": ['lyrics=lyric_scraper.main:to_get_lyrics']
    },
    classifiers=[

                  'Topic :: Software Development :: Build Tools',
                  'License :: OSI Approved :: MIT License',
                  'Programming Language :: Python :: 3',
                  'Programming Language :: Python :: 3.4',
                  'Programming Language :: Python :: 3.5',
                  'Programming Language :: Python :: 3.6',
              ],
)