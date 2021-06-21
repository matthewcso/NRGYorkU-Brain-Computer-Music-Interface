
requirements.out: requirements.txt
	pip install -r $< > $@

eeg_splitted_labels.npy eeg_splitted_features.npy: split_gameemo.py GAMEEMO # requirements.out
	python split_gameemo.py