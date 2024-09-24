from setuptools import setup
version = "2.0.0"

setup(
    name="PToolkit",
    version=version,
    description="A set of tools to make working in a lab easier.",
    url="https://github.com/JDVHA/PToolkit",
    author="H.A.J de Vries",
    author_email="",
    license="MIT",
    download_url="https://github.com/JDVHA/PToolkit/archive/refs/tags/1.0.tar.gz",
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

