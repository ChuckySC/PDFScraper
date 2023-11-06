# Preconditions

* *Install Visual Studio Code:*    https://code.visualstudio.com/
* *Install Extension:*   Python Extension Pack
* *Install Python:*   https://code.visualstudio.com/docs/python/python-tutorial or from  MicrosoftStore
* *Use poppler for converting pdf into xml*, with command:
  `pdftohtml -xml -i file.pdf file.xml`

  Option -xml forms xml page
  Option -i ignores the images

  Additional options:
  -f xxx from what page you want to start
  -l xxx what page you want it to be the last one

# Initial set up

1. *Create virtual environment:*   ```python -m venv .<environmentname>```
2. *Activate virtual environment:*  ```.<environmentname>/scripts/activate```
3. *Check pip version [optional]:*   ```python -m pip --version```
4. *Upgrade pip version [optional]*:   ```python -m pip install --upgrade pip```
5. *Install required dependencies:*   ```python -m pip install -r requirements.txt```
6. *Run Flask development server:* `python -m flask run`

**Or on macOS**

1. *Create virtual environment:*   ```python3 -m venv .<environmentname>```
2. *Activate virtual environment:*  ```.<environmentname>/scripts/activate```
3. *Check pip version [optional]:*   ```python3 -m pip --version```
4. *Upgrade pip version [optional]*:   ```python3 -m pip install --upgrade pip```
5. *Install required dependencies:*   ```python3 -m pip install -r requirements.txt```
6. *Run Flask development server:* `python3 -m flask run`
