# Clash of LLMs

## Installations
### Using Virtual Environments - For windows/wsl users
- `python -m venv venv`: Creates a virtual environment called venv in the current directory
- `source venv/bin/activate`: Activate the environment
- https://docs.python.org/3/library/venv.html

### APIs
ChatGPT **Use ChatGPT-3.5 or lower models**
- `export OPENAI_API_KEY="your_api_key_here"`: Set the key as an environmental variable
- `pip install openai`: Install openai library
- https://platform.openai.com/docs/quickstartOPEN

Ilama - not tested
- `!pip install llamaapi -q`

## GitHub Commands
- `git pull`: Get most recent changes (most likely on main) 
- `git checkout -b [branchName]`: Branch out
- `git checkout [branch]`: Switch branches
- `git add [filename]`: Add file for commit
- `git commit -m "[message]"`: Commit with msg
- `git push`: Push changes to remote repository
- `git status`: Check what files have been changed
Other Option: use built in vscode git extension

## CI/CD installations
Pylint
- `pip install pylint`: linter for Python
- `apt install pylint`: terminal linter tool
  - `pylint [file.py]`: manually checking python files
- Also install the extension for Pylint in vscode

