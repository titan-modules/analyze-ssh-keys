#!/usr/bin/env python
"""
This is a Titan module

- AnalyzeSSHKeys

To use:

    sudo pip install --upgrade titantools

"""

import json
import logging
from sys import argv, exit
from titantools.orm import TiORM
from titantools.data_science import DataScience
from titantools.system import execute_command as shell_out

# from sys import argv
from time import time, gmtime, strftime
from os.path import dirname,basename,isfile
from os import chmod

# Set Logging Status
logging_enabled = False

# Set datastore directory
DATASTORE = argv[1]

class AnalyzeSSHKeys(object):
    """ AnalyzeSSHKeys """

    def __init__(self):
      self.message = type(self).__name__
      self.status = 0
      self.datastore = []

    def getkeys(self):
      """
      Find all ssh public keys and fingerprints
      """
      fingerprints = [ keys for keys in shell_out('find /Users/*/.ssh/ ! -name "known_hosts" -type f -exec bash -c "echo -n \'{} \' && ssh-keygen -lf {}" \;').split('\n') if '  ' in keys]

      # Loop through found fingerprints
      for key in fingerprints:
        
        # Key Parts
        key_parts = key.split()

        # Append to master
        self.datastore.append({
            "path": key_parts[0].replace('//', '/'),
            "strength": key_parts[1],
            "fingerprint": key_parts[2],
            "comment": key_parts[3],
            "key_type": key_parts[4],
            "date": exec_date
          })

      # Set Message
      self.message = "Found %d public ssh keys" % len(self.datastore)

      # If no issues, return 0
      self.status = 0

    def analyze(self):
      """w
      This is the 'main' method that launches all of the other checks
      """
      self.getkeys()

      return json.JSONEncoder().encode({"status": self.status, "message": self.message})

    def store(self):
      # the table definitions are stored in a library file. this is instantiating
      # the ORM object and initializing the tables
      module_schema_file = '%s/schema.json' % dirname(__file__)

      # Is file
      if isfile(module_schema_file):
        with open(module_schema_file) as schema_file:   
          schema = json.load(schema_file)

        # ORM 
        ORM = TiORM(DATASTORE)
        if isfile(DATASTORE):
            chmod(DATASTORE, 0600)
        for k, v in schema.iteritems():
            ORM.initialize_table(k, v)

        data_science = DataScience(ORM, self.datastore, "ssh_public_keys")
        data_science.get_all()

if __name__ == "__main__":

    start = time()

    # the "exec_date" is used as the "date" field in the datastore
    exec_date = strftime("%a, %d %b %Y %H:%M:%S", gmtime())

    ###########################################################################
    # Gather data
    ###########################################################################
    try:
        a = AnalyzeSSHKeys()
        if a is not None:
            output = a.analyze()
            a.store()
            print output

    except Exception, error:
        print error

    end = time()

    # to see how long this module took to execute, launch the module with
    # "--log" as a command line argument
    if "--log" in argv[1:]:
      logging_enabled = True
      logging.basicConfig(format='%(message)s', level=logging.INFO)
    
    logging.info("Execution took %s seconds.", str(end - start))
