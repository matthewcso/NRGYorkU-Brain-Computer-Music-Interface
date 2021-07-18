### OpenBCI Ganglion
It's also fairly simple to get data streams out of the Ganglion, but it's much more finicky than the Muse. There is potentially a good dataset for it, though, and it is certainly a lot more flexible.

INTERFACES dataset: 
- https://github.com/IoBT-VISTEC/EEG-Emotion-Recognition-INTERFACES-datasets

Notes:
- Use OpenBCI GUI to check the impedence on each electrode and reference
- If it's not working, press the top right hand button and check the logs, I had an issue with it trying to write to my administrator account's directory

Requirements:
- OpenBCI-GUI [well, strongly recommended](https://docs.openbci.com/docs/06Software/01-OpenBCISoftware/GUIDocs)
- brainflow
