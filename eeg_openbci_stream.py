# %%
from brainflow.board_shim import BrainFlowError
from brainflow.board_shim import BoardShim, BrainFlowInputParams,  BoardIds
import numpy as np
import time

def openbci_setup(n_last=5, use_synthetic = False):
    params = BrainFlowInputParams()
    params.serial_port='COM3' # I think? check Device Manager --> Ports
    if not use_synthetic:
        board_id = BoardIds.GANGLION_BOARD.value 
    else: 
        board_id = BoardIds.SYNTHETIC_BOARD.value

    sampling_rate = BoardShim.get_sampling_rate(board_id)
    n_samples = int(sampling_rate * n_last)
    board = BoardShim(board_id, params)
    return board, n_samples

    
def openbci_streamer(last_eeg_mp, eeg_setup_phase, currently_running, n_last=5, use_synthetic=False):
    board, n_samples = openbci_setup(n_last, use_synthetic)
    try:
        board.prepare_session()
        board.start_stream()
    except BrainFlowError:
        with currently_running.get_lock():
            currently_running.value=False

    # populate EEG data stream
    while len(np.transpose(board.get_current_board_data(n_samples))) < n_samples:
        time.sleep(0.25)
    
    with eeg_setup_phase.get_lock():
        eeg_setup_phase.value = False

    while True:
        last_eeg_mp = np.frombuffer(last_eeg_mp)
        new_data = board.get_current_board_data(n_samples)
    
        print(new_data.shape)
        new_data = np.ravel(new_data)
        np.copyto(last_eeg_mp, new_data)
        print('You are in the OpenBCI Recording stream!')
        with currently_running.get_lock():
            if not currently_running.value:
                board.stop_stream()
                board.release_session()
                break
        time.sleep(0.25)

# %%
