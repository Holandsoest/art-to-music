# art-to-music

## Setup

### Venv

A **v**irtual **env**ironment is used to sync all our modules.  

#### VScode  

> - Press: `Ctrl` + `Shift` + `P`, To open the pallet.  
> - Type: `Python: Create Environment`  
> - Choose: Venv  
> - Choose: Python  
> - This **might** prompt you to install the `requirements.txt`. If it does then do so.  

VScode: `Ctrl` + `Shift` + `B`, Installs all requirements ***AND*** attach your dependencies to this list.  

#### Powershell (other)

> - `& 'PATH_TO_PYTHON' -m venv .venv` for me this was `& 'C:\Program Files\Python311\python.exe' -m venv .venv` as I installed Python for all users, but for you it might be in a different location under `%appdata%` or smh.  
> - Remember to "to install all the packages that are in the `requirements.txt`" see next bit.  

Manually: Use `pip install -r requirements.txt` to install all the packages that are in the `requirements.txt`  
Manually: Use `pip freeze > requirements.txt` to update `requirements.txt` with the packages that you have installed.  

---
