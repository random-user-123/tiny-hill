#!/usr/bin/env python
import os
import multiprocessing
import traceback
import logging
import math
import time
from math import sqrt
from operator import attrgetter

import Corewar
import Corewar.Benchmarking as CwB

import core_config

log = logging.getLogger('')


class entry:

  def __init__(self, name, code, cfg, new_flag=True):
    self.cfg = cfg
    self.scores = dict()
    self.score = 0.0
    self.p_wins = 0.0
    self.p_ties = 0.0
    self.p_loss = 0.0
    self.new_flag = new_flag

    # For scoring by score distances
    self.dist = dict()
    self.d_avg = None

    # For scoring by delta entropy hack
    self.d_entropy = None

    self.name = name
    self.code = code
    self.wobj = None
    self.age = 0

  def __cmp__(self, other):
    if self.cfg.sort_attr == 'score':
      return cmp(other.score, self.score)
    elif self.cfg.sort_attr == 'd_avg':
      return cmp(other.d_avg, self.d_avg)
    elif self.cfg.sort_attr == 'd_entropy':
      return cmp(other.d_entropy, self.d_entropy)
    else:
      raise ValueError('self.cfg.sort_attr not a valid type')

  def __str__(self):
    return "%s Scores %3.2f" % (self.name, self.score)

  def __len__(self):
    return len(self.wobj.instructions)

  def add_score(self, wname, scores):
    self.scores[wname] = scores

  def del_score(self, wname):
    try:
      del self.scores[wname]
    except:
      pass

  def calculate_score(self, names=None, weight=1.0, divisor=None):
    lscore = 0.0
    t_wins = t_ties = t_loss = 0

    if names == None:
      names = self.scores.keys()

    for name in names:
      wins, loss, ties = self.scores[name]
      t_wins += wins
      t_ties += ties
      t_loss += loss
      lscore += ((wins * 3) + ties)

    count = t_wins + t_ties + t_loss
    if divisor == None:
      self.score = float(lscore) / float(count)
      self.score = self.score * 100.0
      self.raw_score = self.score
      self.p_ties = (float(t_ties) / float(count)) * 100.0
      self.p_loss = (float(t_loss) / float(count)) * 100.0
      self.p_wins = (float(t_wins) / float(count)) * 100.0
    else:
      lscore = (lscore / float(count)) * 100.0
      lscore = lscore * weight
      self.raw_score = self.raw_score + lscore
      self.score = self.raw_score / divisor

  def clear_scores(self):
    self.score = 0.0
    self.p_ties = self.p_loss = self.p_wins = 0.0
    self.scores.clear()


class hill:

  def __init__(self, cfg):
    self.cfg = cfg
    self.mars = CwB.MARS_94nop(coresize=cfg.coresize,
                               maxprocesses=cfg.processes,
                               maxcycles=cfg.cycles,
                               mindistance=cfg.min_sep,
                               maxlength=cfg.max_length)

    self.parser = Corewar.Parser(coresize=cfg.coresize,
                                 maxprocesses=cfg.processes,
                                 maxcycles=cfg.cycles,
                                 mindistance=cfg.min_sep,
                                 maxlength=cfg.max_length,
                                 standard=Corewar.STANDARD_94)

    self.entries = []
    self.bias = []
    self.hill_age = 0
    self.rounds_executed = 0

    self.hill_min = 0.0
    self.hill_max = 0.0
    self.hill_avg = 0.0
    self.hill_median = 0.0

  def __getitem__(self, key):
    return self.entries[key]

  def __len__(self):
    return len(self.entries)

  def __str__(self):
    output = []
    rank = 0
    output.append("Hill Age: %5d\n" % self.hill_age)
    output.append("Hill Score Stats: %3.2f/%3.2f/%3.2f/%3.2f (Min/Max/Avg/Med)\n" %
                  (self.hill_min, self.hill_max, self.hill_avg, self.hill_med))
    for e in self.entries:
      rank += 1
      score = "%3.2f" % e.score
      p_wins = "%3.1f" % e.p_wins
      p_ties = "%3.1f" % e.p_ties
      p_loss = "%3.1f" % e.p_loss
      sort_field = None
      if self.cfg.sort_attr == 'd_avg':
        sort_field = "%3.2f" % e.d_avg
      if self.cfg.sort_attr == 'd_entropy':
        sort_field = "%3.2f" % e.d_entropy

      new = ''
      if e.new_flag is True:
        new = 'New'

      if sort_field is None:
        output.append("%3s %32s %6s WTL%% %5s %5s %5s %3d %3s\n" %
                      (rank, e.name[0:32], score, p_wins, p_ties, p_loss, e.age, new))
      else:
        output.append("%3s %32s %6s %6s WTL%% %5s %5s %5s %3d %3s\n" %
                      (rank, e.name[0:32], score, sort_field, p_wins, p_ties, p_loss, e.age, new))
    return ''.join(output)

  def get_stats(self):
    return (self.hill_min, self.hill_max, self.hill_avg, self.hill_med)

  def quick_test(self, pe):
    score = self.quick_test_score(pe)
    if score > self.cfg.qmin_score:
      return True
    return False

  def quick_test_score(self, pe):
    self.run_optimizer_battles(quick_test=pe)
    pe.calculate_score()
    score = pe.score
    pe.clear_scores()
    return score

  def load_file(self, fname):
    name = fname.split("/")[-1]
    code = ';redcode' + file(fname).read()
    new = entry(name, code, self.cfg, new_flag=False)
    new.wobj = self.parser.parse(new.code)
    new.wobj.name = name
    self.entries.append(new)

  def load_string(self, name, string):
    new = entry(name, string, self.cfg)
    new.wobj = self.parser.parse(new.code)
    new.wobj.name = name
    self.entries.append(new)

  def load_directory(self, directory, debug=False):
    files = os.listdir(directory)
    for fname in files:
      log.info('loading %s', fname)
      try:
        self.load_file("%s/%s" % (directory, fname))
      except Corewar.WarriorParseError, e:
        log.exception(e)
        log.error('failed to parse %s', fname)

  def load_bias(self, directory):
    files = os.listdir(directory)
    for fname in files:
      code = ";redcode" + file("%s/%s" % (directory, fname)).read()
      new = entry(fname, code, self.cfg)
      new = self.parser.parse(new.code)
      log.info('loaded %s', new.name)
      self.bias.append(new)

  def save_hill(self, directory, count=False):
    if not count:
      count = self.cfg.hill_size
    for e in self.entries[0:count]:
      log.debug('writing %s', e.name)
      open("%s/%s" % (directory, e.name), "w+").write(str(e.wobj))

  def add_entry(self, entry):
    entry.scores.clear()  # remove any stale scores
    if not self.find_entry(entry.name):
      self.entries.append(entry)
    else:
      log.info("add_entry(): already had a copy of: %s", entry.name)

  def find_entry(self, name):
    for e in self.entries:
      if e.name == name:
        return e
    return None

  def prep_entry(self, pentry):
    if pentry.wobj is None:
      log.debug('prep_entry: running parser?')
      pentry.wobj = self.parser.parse(pentry.code)
    return pentry.wobj

  def clear_scores(self):
    for e in self.entries:
      e.clear_scores()

  def run_battles(self):
    start_time = time.time() * 1.0
    start_rounds = self.rounds_executed 
    for w1 in self.entries:
      for w2 in self.entries:
        if not (w1.name in w2.scores) or \
                not (w2.name in w1.scores):
          if self.cfg.p_mode is True:
            result = self.mars.p_run((self.prep_entry(w1),
                                      self.prep_entry(w2)))
            w1_score, w2_score = result[:]
            w1.add_score(w2.name, w1_score)
            w2.add_score(w1.name, w2_score)
            self.rounds_executed += self.cfg.rounds
          else:
            result = self.mars.run((self.prep_entry(w1),
                                    self.prep_entry(w2)),
                                   self.cfg.rounds)
            w1_score, w2_score, trash = result[:]
            w1.add_score(w2.name, w1_score)
            w2.add_score(w1.name, w2_score)
            self.rounds_executed += self.cfg.rounds
    end_time = time.time() * 1.0
    total_rounds = self.rounds_executed - start_rounds 
    log.warning('run_battles %d rounds in %ds (%3.2f r/s)', total_rounds, end_time - start_time,
                float(total_rounds) / (end_time - start_time))

  def score_hill(self, quiet=False):
    self.run_battles()

    total = 0
    for w in self.entries:
      w.calculate_score()
      total += w.score

    if self.cfg.sort_attr == 'd_avg':
      self.calculate_distance()

    if self.cfg.sort_attr == 'd_entropy':
      self.calculate_d_entropy()

    self.entries.sort()

    while len(self.entries) > self.cfg.hill_size:
      dead = self.entries[-1]
      total -= dead.score

      if not quiet:
        print dead.name, "was pushed off... (%3.2f %s)" % (getattr(dead, self.cfg.sort_attr),
                                                           self.cfg.sort_attr)
      for w in self.entries:
        w.del_score(dead.name)
        w.calculate_score()

      dead.scores.clear()
      del self.entries[-1]

      if self.cfg.sort_attr == 'd_avg':
        self.calculate_distance()

      if self.cfg.sort_attr == 'd_entropy':
        self.calculate_d_entropy()

      self.entries.sort()

    if self.entries:
      self.hill_min = self.entries[-1].score
      self.hill_max = self.entries[0].score
      self.hill_avg = float(total) / float(len(self.entries))
      self.hill_med = self.median_score()
      
    self.hill_age += 1
    for e in self.entries:
      e.age += 1

  def run_optimizer_battles(self, quick_test=None):
    if quick_test is None:
      log.debug('run_optimizer_battles: running all battles against %d bias warriors',
                len(self.bias))
      entries = self.entries
      rounds = self.cfg.rounds
    else:
      log.debug('run_optimizer_battles: quick_test for %s', quick_test.name)
      entries = [quick_test]
      rounds = self.cfg.quick_rounds

    for w1 in entries:
      for w2 in self.bias:
        if not (w2.name in w1.scores):
          if self.cfg.p_mode is True and rounds == self.cfg.rounds:
            log.debug('run_optimizer_battles: p_run(%s, %s)', w1.name, w2.name)
            result = self.mars.p_run((self.prep_entry(w1), w2))
            w1_score, w2_score = result[:]
            w1.add_score(w2.name, w1_score)
          else:
            log.debug('run_optimizer_battles: rounds: %s, run(%s, %s)', rounds, w1.name, w2.name)
            result = self.mars.run((self.prep_entry(w1), w2), rounds)
            w1_score, w2_score, trash = result[:]
            w1.add_score(w2.name, w1_score)
          self.rounds_executed += rounds
        else:
          log.debug('run_optimizer_battles: already ran(%s, %s): %s', w1.name, w2.name,
                    w1.scores[w2.name])

  def run_mp_optimizer_battles(self):
    to_run = []
    for i, w1 in enumerate(self.entries):
      for w2 in self.bias:
        if not (w2.name in w1.scores):
          to_run.append((i, w1, w2, self.cfg))

    pool = multiprocessing.Pool()
    results = pool.imap_unordered(run_mp_battles, to_run, chunksize=5)
    for result in results:
      i, w2_name, w1_score = result
      self.entries[i].add_score(w2_name, w1_score)
      self.rounds_executed += self.cfg.rounds

    pool.terminate()

  def score_optimizer_hill(self, quiet=False, names=None, mp=False):
    if mp is True:
      self.run_mp_optimizer_battles()
    else:
      self.run_optimizer_battles()

    total = 0
    for w in self.entries:
      w.calculate_score()
      total += w.score

    if self.cfg.sort_attr == 'd_avg':
      self.calculate_distance()

    if self.cfg.sort_attr == 'd_entropy':
      self.calculate_d_entropy()

    self.entries.sort()

    while len(self.entries) > self.cfg.hill_size:
      dead = self.entries[-1]
      total -= dead.score

      if not quiet:
        print dead.name, "was pushed off... (%3.2f %s)" % (getattr(dead, self.cfg.sort_attr),
                                                           self.cfg.sort_attr)

      if names is not None and dead.name in names:
        del names[dead.name]

      dead.scores.clear()
      del self.entries[-1]
      if self.cfg.sort_attr == 'd_avg':
        self.calculate_distance()

      if self.cfg.sort_attr == 'd_entropy':
        self.calculate_d_entropy()

      self.entries.sort()

    if self.entries:
      self.hill_min = self.entries[-1].score
      self.hill_max = self.entries[0].score
      self.hill_avg = float(total) / float(len(self.entries))
      self.hill_med = self.median_score()

    self.hill_age += 1
    for e in self.entries:
      e.age += 1

  def median_score(self):
    if len(self) < 1:
            return None
    if len(self) % 2 == 1:
            return self[((len(self)+1)/2)-1]
    else:
            return float(sum([x.score for x in self[(len(self)/2)-1:(len(self)/2)+1]]))/2.0

  def calculate_distance(self):
    for e in self.entries:
      e.dist = dict()

    for e1 in self.entries:
      for e2 in self.entries:
        if (e1.name == e2.name) or (e1.name in e2.dist) or (e2.name in e1.dist):
          continue
        dist = dict()
        names = e1.scores.keys()
        for name in names:
          rdis = 0.0
          e1_wins, e1_loss, e1_ties = e1.scores[name]
          e2_wins, e2_loss, e2_ties = e2.scores[name]

          # Calculate the distances between 3d points, but stretch
          # distances on the wins axis and compress distances on the
          # losses axis. Novelty on the wins axis is more valuable
          # than novelty on the losses axis.
          rdis += ((e1_wins - float(e2_wins)) * 1.5) ** 2
          rdis += ((e1_loss - float(e2_loss)) * 0.5) ** 2
          rdis += (e1_ties - float(e2_ties)) ** 2
          dist[name] = math.sqrt(rdis)

        # Take the average distance to the others as a metric of novelty
        d_avg = sum(dist.values()) / float(len(dist))
        e1.dist[e2.name] = d_avg
        e2.dist[e1.name] = d_avg

    for e in self.entries:
      e.d_avg = sum(e.dist.values()) / float(len(e.dist))

  def calculate_d_entropy(self):

    def freq(sym_occurances, global_occurances):
      return float(sym_occurances) / float(global_occurances)

    def calc_entropy(instructions, global_symbols, total_symbols):
      total = 0.0
      symbols = set([str(i) for i in instructions])
      for sym in symbols:
        f = freq(global_symbols[sym], total_symbols)
        total += f * math.log(f)
      return -1.0 * total

    global_symbols = {}

    for e in self.entries:
      e.symbols = {}
      for i in e.wobj.instructions:
        sym = str(i)
        if sym not in global_symbols:
          global_symbols[sym] = 1
        else:
          global_symbols[sym] += 1

    total_symbols = sum(global_symbols.values())

    # Order by score for the next step        
    self.entries.sort(key=lambda c: c.score, reverse=True)
    
    for index, e in enumerate(self.entries):
      d_entropy = calc_entropy(e.wobj.instructions, global_symbols, total_symbols)
      if index > 0:
        e.d_entropy = d_entropy - calc_entropy(self.entries[index - 1].wobj.instructions,
                                               global_symbols, total_symbols)
      else:
        if e.score < self.cfg.qmin_score:
          e.d_entropy = -99.9
        else:
          e.d_entropy = d_entropy
        
    # Re-order by d_entropy to finish
    self.entries.sort()

def run_mp_battles(battle):
  i, w1, w2, cfg = battle
  try:
    mars = CwB.MARS_94nop(coresize=cfg.coresize,
                          maxprocesses=cfg.processes,
                          maxcycles=cfg.cycles,
                          mindistance=cfg.min_sep,
                          maxlength=cfg.max_length)

    if w1.wobj == None:
      parser = Corewar.Parser(coresize=cfg.coresize,
                              maxprocesses=cfg.processes,
                              maxcycles=cfg.cycles,
                              mindistance=cfg.min_sep,
                              maxlength=cfg.max_length,
                              standard=Corewar.STANDARD_94)
      w1.wobj = parser.parse(w1.code)

    if cfg.p_mode is True:
      result = mars.p_run((w1.wobj, w2))
      w1_score, w2_score = result[:]
    else:
      result = mars.run((w1.wobj, w2), cfg.rounds)
      w1_score, w2_score, trash = result[:]
  except:
    print traceback.format_exc()
    raise

  return (i, w2.name, w1_score)

if __name__=='__main__':
  h = hill(core_config.core_config())
  h.load_directory('valhalla')
  h.score_hill()
  print h
