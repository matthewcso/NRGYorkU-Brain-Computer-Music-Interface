### EMOTIV EPOC+

We don't know exactly how to get data out of the Emotiv, but we do have at least one good emotion dataset using the Emotiv.

### How to use:
- If you haven't installed Python 3.x yet, [Anaconda](https://docs.anaconda.com/anaconda/install/) is highly recommended. Follow the instructions on the website. 
- (Optional) If using Anaconda, create a new environment by running `conda create -n BCMI-env` (once). Then, every time you need to run the code, activate the environment by running `conda activate BCMI-env`.
- Install the requirements (once) using `pip install -r requirements.txt`. 
- Run `split_gameemo.py` by using `python split_gameemo.py`, using your IDE, or interactively in vscode.
- Run `regression.ipynb` .

### Citations:
- [GAMEEMO dataset, used for current classifier training](https://www.kaggle.com/sigfest/database-for-emotion-recognition-system-gameemo)