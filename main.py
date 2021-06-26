# %%
import multiprocessing
from composer_algorithm_multiprocess_test import composer_process
from controller_test import controller

valence_mp = multiprocessing.Value('d',0.5)
arousal_mp = multiprocessing.Value('d',0.5)
currently_running = multiprocessing.Value('b', True)
if __name__ == '__main__':

    p2 = multiprocessing.Process(target=composer_process, args=(valence_mp, arousal_mp, currently_running))
    p2.start()

    controller(valence_mp, arousal_mp, currently_running)

# %%
