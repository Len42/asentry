""" asentry - Monitor the JPL Sentry database for asteroid impact threats.

    This program downloads a list of potential Earth-threatening asteroids
    from NASA JPL's Sentry (https://cneos.jpl.nasa.gov/sentry/) service
    and displays an alert message if there are any new or increased threats
    since the last time it ran.

    If there is a sound file named "alert.mp3" in this directory, it will be
    played when a warning message is displayed.

    Copyright 2023 Len Popp - see LICENSE
"""

import sys
import os.path
import traceback
import json
import requests
import playsound3

def configFilePath() -> str: return os.path.join(os.path.expanduser('~'), '.asentry')

def loadSavedData() -> list:
    """ Load the list of known potential threat objects. """
    try:
        with open(configFilePath(), 'r') as file:
            data = json.load(file)
            return data['objects']
    except:
        # If there's no config file, return no data.
        return []
    
def writeSavedData(objects: list):
    """ Save the list of known potential threat objects for next time. """
    # Only save certain data fields for each object.
    saveObjects = [
        { 'id': object['id'], 'ps_cum': object['ps_cum'], 'ts_max': object['ts_max'] }
        for object in objects ]
    data = { 'objects': saveObjects }
    with open(configFilePath(), 'w') as file:
        json.dump(data, file)

def fetchLatestData() -> list:
    """ Fetch the latest set of "interesting" objects from NASA JPL. """
    # Only fetch a few of the most threatening objects.
    response = requests.get('https://ssd-api.jpl.nasa.gov/sentry.api',
                            params={'ps-min':'-3'})
    response.raise_for_status()
    results = json.loads(response.text)
    if (results['signature']['source'] != 'NASA/JPL Sentry Data API'
            or results['signature']['version'] != '2.0'):
        raise RuntimeError('Unexpected data format')
    return results['data']

def fetchDummyData() -> list:
    """ Return a dummy dataset for testing. """
    return [
            {'id': 'a0101955', 'ps_cum': '-1.55', 'ts_max': None, 'last_obs_jd': '2459126.3016', 'v_inf': '5.9916984432395', 'last_obs': '2020-10-3.80160', 'fullname': '101955 Bennu (1999 RQ36)', 'range': '2178-2290', 'h': '20.63', 'ip': '0.000571699999999996', 'diameter': '0.49', 'ps_max': '-1.59', 'n_imp': 157, 'des': '101955'},
            {'id': 'bK23T04L', 'ps_cum': '-1.77', 'ts_max': '1', 'last_obs_jd': '2460262.5', 'ip': '3.93877e-05', 'h': '20.09', 'range': '2119-2121', 'fullname': '(2023 TL4)', 'last_obs': '2023-11-14', 'v_inf': '34.9494547282527', 'ps_max': '-1.80', 'diameter': '0.32', 'des': '2023 TL4', 'n_imp': 3}
        ]

def checkForUpdates(savedObjects: list, latestObjects: list) -> bool:
    """ Compare the saved data to the latest data and alert the user to any
        new objects or objects with increased threat levels.
        Return True if there are any new or increased threats.
    """
    anyChanges = False
    for object in latestObjects:
        printObject = False
        found = [ obj for obj in savedObjects if obj['id'] == object['id'] ]
        if len(found) == 0:
            # new object
            anyChanges = True
            print(f"WARNING: New threat: {object['fullname']}")
            printObject = True
        else:
            savedObject = found[0]
            if (float(object['ps_cum']) > float(savedObject['ps_cum'])
                    or (object['ts_max'] != None and savedObject['ts_max'] == None)
                    or (object['ts_max'] != None and savedObject['ts_max'] != None
                        and float(object['ts_max']) > float(savedObject['ts_max']))):
                # object threat level has increased
                anyChanges = True
                print(f"WARNING: Increased threat: {object['fullname']}")
                printObject = True
        if printObject:
            print(f"Impact date {object['range']}, " \
                f"Palermo = {object['ps_cum']}, Torino = {object['ts_max']}\n" \
                f"Details: https://cneos.jpl.nasa.gov/sentry/details.html#?des={object['des']}\n")
    return anyChanges


cmdName, *args = sys.argv
cmdDir = os.path.dirname(cmdName)
cmdName = os.path.basename(cmdName)
try:
    savedObjects = loadSavedData()

    latestObjects = fetchLatestData()
    #latestObjects = fetchDummyData() # DEBUG

    anyChanges = checkForUpdates(savedObjects, latestObjects)

    writeSavedData(latestObjects)

    if anyChanges:
        # Play an obnoxiously loud alert sound. (No error if the file is missing)
        soundFile = os.path.join(cmdDir, 'alert.mp3')
        if os.path.isfile(soundFile):
            try:
                playsound3.playsound(soundFile)
            except:
                pass
        exitCode = 1
    else:
        print('No new threats')
        exitCode = 0

except BaseException as ex:
    print(f'{cmdName}: Error: {ex}')
    traceback.print_tb(ex.__traceback__)
    exitCode = 2

sys.exit(exitCode)
