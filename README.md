# Exercise 1

## Table of Contents

1. [Install Python](#install-python)
2. [Set Up a Virtual Environment](#set-up-a-virtual-environment)
3. [Create a Python Script](#create-a-python-script)
4. [Set Up IPython Shell](#set-up-ipython-shell)
5. [Export a Requirements File](#export-a-requirements-file)
6. [Create a Github Repo](#create-a-github-repo)

## Install Python

First, install Python 3.8.7 on your system. Check your Python version by using the command `python --version` from your terminal.

![Step 1](./Exercise_1.1/1.png)

## Set Up a Virtual Environment

Set up a new virtual environment named “cf-python-base”.

![Step 2](./Exercise_1.1/2.png)

## Create a Python Script

Install Visual Studio Code or another text editor of your preference, and then create a Python script named "add.py." This script is designed to receive two numbers as user input, add them together, and display the result. Below is the template for your Python script:

![Step 3](./Exercise_1.1/3.png)

```python
a = int(input("Enter First Number"))
b = int(input("Enter Second Number"))

c = a + b

print(c)
```

## Set Up IPython Shell

To establish an IPython shell within the virtual environment "cf-python-base," you can leverage pip for installation. The IPython shell closely resembles the standard Python REPL but offers enhanced features such as syntax highlighting, auto-indentation, and robust auto-complete capabilities.

![Step 4](./Exercise_1.1/4.png)

## Export a Requirements File

First, generate a “requirements.txt” file from your source environment. To do this, you use the pip freeze command and all packages (including version numbers) installed in the currently activated environment will be compiled: > pip freeze > requirements.txt.
Next, create a new environment called “cf-python-copy”. In this new environment, install packages from the “requirements.txt” file that you generated earlier. To install the packages from this file in any other environment, you run the pip install command with the extra -r argument, followed by the name of your requirements file: > pip install -r requirements.txt.

![Step 5](./Exercise_1.1/5.png)
