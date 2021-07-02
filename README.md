# NRGYorkU Brain Computer Music Interface

### Goal:
To develop a Brain-Computer Music Interface (BCMI) to generate music based on a person's emotions, as determined by real-time EEG classification using an Emotiv kit.

### Potential Steps:
There are 3 main parts of this project that can be developed in parallel. There may exist a number of technical difficulties involved in connecting multiple real-time data feeds to each other.

- **EEG data feed:** We need to develop a pipeline for acquiring a real-time EEG data feed that can be attached to a classifier. This may be the most difficult step conceptually, as there are few good libraries available for acquiring this type of data from the Emotiv EPOC. 
- **Emotion Classification:** We need to extract robust EEG features and we need to train a classifier or regressor to determine the emotional content from EEG data. We will use publicly available EEG datasets for this task, and might want to incorporate some elements of semi-supervised learning (given the abundance of EEG data without labels).
- **Music Generation:** We need to generate music based on the identified emotions. This can be done using Erlich's algorithm, which has been translated to Python at this point in time. As a brief note, it might potentially be better to do away with Erlich's algorithm entirely in the future and to use a generative adversarial music generation algorithm instead; however, this will be a technically difficult challenge.

### Requirements:
- Python 3.x. Anaconda installation highly recommended. Ability to run Jupyter Notebooks highly recommended.
- All libraries listed in requirements.txt. Run `pip install -r requirements.txt` from command line to install dependencies.
- VirtualMIDISynth. You can download this software from [here](https://coolsoft.altervista.org/en/download/CoolSoft_VirtualMIDISynth_2.11.2.exe).
- Sound fonts for VirtualMIDISynth. I used [these](https://github.com/urish/cinto/blob/master/media/FluidR3%20GM.sf2) soundfonts.


### How to use:
- If you haven't installed Python 3.x yet, [Anaconda](https://docs.anaconda.com/anaconda/install/) is highly recommended. Follow the instructions on the website. 
- (Optional) If using Anaconda, create a new environment by running `conda create -n BCMI-env` (once). Then, every time you need to run the code, activate the environment by running `conda activate BCMI-env`.
- Install the requirements (once) using `pip install -r requirements.txt`. 
- Run `split_gameemo.py` by using `python split_gameemo.py`, using your IDE, or interactively in vscode.
- Run `regression.ipynb` .

### Citations
- [Stefan Erlich's music generation algorithm](https://github.com/stefan-ehrlich/code-algorithmicMusicGenerationSystem).
- [GAMEEMO dataset, used for current classifier training](https://www.kaggle.com/sigfest/database-for-emotion-recognition-system-gameemo)
- We intend on using the [DEAP dataset](http://www.eecs.qmul.ac.uk/mmv/datasets/deap/) for classifier training in the future. 
- Ehrlich, S. K., Agres, K. R., Guan, C., & Cheng, G. (2019). A closed-loop, music-based brain-computer interface for emotion mediation. PloS one, 14(3), e0213516. URL/DOI: https://doi.org/10.1371/journal.pone.0213516

