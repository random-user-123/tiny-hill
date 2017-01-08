import argparse
import math
import random
import logging

from Corewar.Redcode import *

log = logging.getLogger('')

class core_config:
  def __init__(self, *args, **kwargs):
    self._set_config_defaults()
    self.set_config_overrides(**kwargs)

  def _set_config_defaults(self):
    self.debug = False
    
    self.author = "anonymous"
    self.hillkey = "tiny"

    # Core settings for running the entries, these aren't editable via command line because
    # they need to be the same for all entries on the server. 
    self.coresize = 800
    self.cycles = 8000
    self.max_length = 20
    self.processes = 800
    self.min_sep = 20

    self.p_mode = True
    if self.p_mode is True:
      self.rounds = 2 * (self.coresize - self.min_sep + 1)
    else:
      self.rounds = 200

    # 'score' to push entries off hill based on score
    # 'd_avg' to run the hill based on avg distance between scores
    # 'd_entropy' to use entropy estimate
    # d_avg is a stab at novelty search
    self.sort_attr = 'score'

    # Minimum hill size to keep, and maximum to fill to
    self.hill_size = 50

  def set_config_overrides(self, **kwargs):
    for key, value in kwargs.items():
      if value is not None:
        log.warning('setting override config option %s -> %s', key, value)
        setattr(self, key, value)

