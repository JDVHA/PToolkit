from setuptools import setup
version = "2.0.5"
import pathlib
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="PToolkit",
    version=version,
    description="A set of tools to make working in a lab easier.",
    long_description_content_type='text/markdown',
    long_description="README",
    url="https://github.com/JDVHA/PToolkit",
    author="H.A.J de Vries",
    author_email="",
    license="MIT",
    include_package_data = True,
    download_url="https://github.com/JDVHA/PToolkit/archive/refs/tags/2.0.tar.gz",
    install_requires=[
          'numpy',
          "matplotlib",
          "sympy",
          "scipy",
          "pyserial"
      ],
    entry_points = {
        'console_scripts': [
            'PToolkit = PToolkit.cmd:main'
        ]
    },
)

