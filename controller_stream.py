import keyboard
def controller(valence_mp, arousal_mp, currently_running, eeg_setup_phase, composer_setup_phase):
    from time import sleep

    while True:
        with composer_setup_phase.get_lock():
            with eeg_setup_phase.get_lock():
                if (not composer_setup_phase.value) and (not eeg_setup_phase.value):
                    break
                else:
                    sleep(0.25)
    print('Controller running')
    while True:
        with valence_mp.get_lock():
            valence_val = valence_mp.value
        with arousal_mp.get_lock():
            arousal_val = arousal_mp.value

        print('Current Valence: %s Arousal: %s' % (str(valence_val), str(arousal_val)) + '\n Press and hold 1 and q to exit')
        if keyboard.is_pressed('q') and keyboard.is_pressed('1'):
            print('1+q was pressed, exiting.')
            with currently_running.get_lock():
                currently_running.value = False        
        #else:
        #    try:
        #        splitted = inp.split(' ')
        #        v = float(splitted[0])
        #        a = float(splitted[1])
        #        if v >= 0 and v <= 1 and a >= 0 and a <= 1:
        #            with valence_mp.get_lock():
        #                valence_mp.value = v
        #            with arousal_mp.get_lock():
        #                arousal_mp.value = a
        #    except ValueError:
        #        print('Invalid input.')
        #    except IndexError:
        #        print('Invalid input.')


        with currently_running.get_lock():
            if not currently_running.value:
                break
        sleep(1)