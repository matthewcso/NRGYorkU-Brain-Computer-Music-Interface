def controller(valence_mp, arousal_mp, currently_running, composer_setup_phase):
    from time import sleep

    while True:
        with composer_setup_phase.get_lock():
            if not composer_setup_phase.value:
                break
            else:
                sleep(0.25)
    print('Controller running')
    while True:
        with valence_mp.get_lock():
            valence_val = valence_mp.value
        with arousal_mp.get_lock():
            arousal_val = arousal_mp.value
        inp = input('Current Valence: %s Arousal: %s' % (str(valence_val), str(arousal_val)) + '\n Input Valence and Arousal, separated by spaces. Or exit ')
        

        if inp == 'exit':
            with currently_running.get_lock():
                currently_running.value = False
        else:
            try:
                splitted = inp.split(' ')
                v = float(splitted[0])
                a = float(splitted[1])
                if v >= 0 and v <= 1 and a >= 0 and a <= 1:
                    with valence_mp.get_lock():
                        valence_mp.value = v
                    with arousal_mp.get_lock():
                        arousal_mp.value = a
            except ValueError:
                print('Invalid input.')
            except IndexError:
                print('Invalid input.')


        with currently_running.get_lock():
            if not currently_running.value:
                break
        sleep(1)