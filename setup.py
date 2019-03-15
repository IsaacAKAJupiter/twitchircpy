import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="twitchircpy",
    version="1.0.4",
    author="IsaacAKAJupiter",
    description="A wrapper for the Twitch IRC used for creating chat bots.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IsaacAKAJupiter/twitchircpy",
    packages=["twitchircpy", "twitchircpy.extensions.customcommandbot"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
)