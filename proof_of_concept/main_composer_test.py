# %%
import multiprocessing
from composer_algorithm_multiprocess_test import composer_process
from controller_test import controller

valence_mp = multiprocessing.Value('d',0.5)
arousal_mp = multiprocessing.Value('d',0.5)
currently_running = multiprocessing.Value('b', True)
composer_setup_phase = multiprocessing.Value('b', True)
eeg_setup_phase = multiprocessing.Value('b', False)
if __name__ == '__main__':
    p2 = multiprocessing.Process(target=composer_process, args=(valence_mp, arousal_mp, currently_running, composer_setup_phase, eeg_setup_phase))
    p2.start()
    #composer_process(valence_mp, arousal_mp, currently_running, composer_setup_phase, eeg_setup_phase)

    controller(valence_mp, arousal_mp, currently_running, composer_setup_phase)

# %%
