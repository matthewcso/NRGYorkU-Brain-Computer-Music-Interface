# Doesn't work yet; just returns all 0s. 
# Use OpenBCI_GUI to run impedence check instead
while True:
    with eeg_setup_phase.get_lock():
        if not eeg_setup_phase.value:
            break
    sleep(0.25)
    print('Done waiting for EEG!')
    print('Checking impedences:')
    last_value = np.frombuffer(last_eeg_mp)
    last_value = np.reshape(last_value, [BRAINFLOW_MAGIC_N, n_samples])
    print(np.mean(last_value[board.get_resistance_channels(board_id)], axis=1))
