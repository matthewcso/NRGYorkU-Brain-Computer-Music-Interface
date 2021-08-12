# %%
import multiprocessing
from composer_stream import composer_process
from controller_stream import controller
from classify_stream import classify
from eeg_openbci_stream import openbci_streamer, openbci_setup
import numpy as np

USE_SYNTHETIC = True
RUN_COMPOSER = True
DEBUG_STREAMER = False
DEBUG_CLASSIFIER = False
N_LAST = 5
channel_names = 'Fp1,Fp2,T3,T4'.split(',')
valence_mp = multiprocessing.Value('d',0.5)
arousal_mp = multiprocessing.Value('d',0.5)
currently_running = multiprocessing.Value('b', True)
composer_setup_phase = multiprocessing.Value('b', True)
eeg_setup_phase = multiprocessing.Value('b', True)

if __name__ == '__main__':
  board, n_samples = openbci_setup(n_last=N_LAST, use_synthetic=USE_SYNTHETIC)
  board_id = board.get_board_id()
  BRAINFLOW_MAGIC_N = board.get_num_rows(board_id)
  last_eeg_mp = multiprocessing.RawArray('d', n_samples*BRAINFLOW_MAGIC_N)

  if not USE_SYNTHETIC:
    eeg_idx = np.asarray(board.get_eeg_channels(board_id))
  else:
    eeg_idx = np.asarray([1, 2, 3, 4])

  print('[Debug Info]:')
  print('Package number channel %s' % (str(board.get_package_num_channel(board_id))))
  print('EEG channels %s' % (str(eeg_idx)))
  print('Accel channels %s' % (str(board.get_accel_channels(board_id))))
  print('Resistance channels %s' % (str(board.get_resistance_channels(board_id))))
  print('Timestamp channel %s' % (str(board.get_timestamp_channel(board_id))))

  print('Performing pre-connection check:')

  board.prepare_session()
  board.release_session()
  print('Pre-connection check was a success!')

  if not DEBUG_STREAMER:
    p1 = multiprocessing.Process(target=openbci_streamer, args=(last_eeg_mp, \
      eeg_setup_phase, currently_running, N_LAST, USE_SYNTHETIC))
    p1.start()
  else:
    openbci_streamer(last_eeg_mp, eeg_setup_phase, currently_running, N_LAST, USE_SYNTHETIC)

  if RUN_COMPOSER:
    p2 = multiprocessing.Process(target=composer_process, args=(valence_mp, arousal_mp, currently_running, composer_setup_phase, eeg_setup_phase))
    p2.start()

  if not DEBUG_CLASSIFIER:
    p3 = multiprocessing.Process(target=classify, args=(last_eeg_mp, valence_mp, \
      arousal_mp, eeg_setup_phase, currently_running, \
      n_samples, BRAINFLOW_MAGIC_N, n_samples/N_LAST, channel_names, eeg_idx, USE_SYNTHETIC))
    p3.start()
  else:
    classify(last_eeg_mp, valence_mp, arousal_mp, eeg_setup_phase, currently_running, \
      n_samples, n_rows=BRAINFLOW_MAGIC_N, sampling_rate = n_samples/N_LAST, \
      channel_names = channel_names, eeg_channel_idx = eeg_idx, \
      use_synthetic = USE_SYNTHETIC)

  controller(valence_mp, arousal_mp, currently_running, eeg_setup_phase, composer_setup_phase)


# %%
