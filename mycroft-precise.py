from precise_runner import PreciseEngine, PreciseRunner
from subprocess import call
import json
import logging
import sys

waiting = 1

def on_act():
    global waiting
    waiting = 0

def main():
    # Load OAuth 2.0 credentials.
    try:
        with open('/data/mycroft-precise.json', 'r') as json_file:
            gva_config = json.load(json_file)
            engine_path = gva_config["engine_path"]
            model_path = gva_config["model_path"]
            trigger_level = gva_config["trigger_level"]
            sensitivity = gva_config["sensitivity"]
            command = gva_config["command"]
    except Exception as e:
        logging.error("Error loading mycroft-precise.json: %s", e)
        sys.exit(-1)

    try:
        # initiate precise engine with mycroft model
        engine = PreciseEngine(engine_path, model_path)

        # initiate precise runner that will listen, predict, and detect wakeword
        runner = PreciseRunner(engine, on_activation=on_act, trigger_level=trigger_level, sensitivity=sensitivity)

        # start runner
        runner.start()
    except Exception as e:
        logging.error("Wake Word Engine Error: %s", e)
        sys.exit(-1)

    # keep main thread active until user interrupt
    try:
        wait_for_user_trigger = True
        global waiting
        while True:
            if wait_for_user_trigger:
                logging.info("Waiting Wake Word")
                while waiting == 1:
                    pass
            if not command:
                logging.info("Wake Word Detected")
            else:
                call(command)
            waiting = 1
    except Exception as e:
        runner.stop()
        logging.error("Mycroft Precise Error: %s", e)
        sys.exit(-1)

if __name__ == '__main__':
    main()
