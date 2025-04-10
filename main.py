from server import Server
import argparse
import sys
import logging
import os
from datetime import datetime as dt

def handle_exception(exc_type, exc_value, exc_traceback):
  cwd = os.path.join(os.getcwd(), 'log')
  log_name = dt.now().isoformat()
  if issubclass(exc_type, KeyboardInterrupt): return
  logging.basicConfig(filename=os.path.join(cwd, f'log{log_name}.txt'), level=logging.ERROR)
  logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

def main():
  sys.excepthook = handle_exception
  parser = argparse.ArgumentParser()
  parser.add_argument('-prod', '--production', type=bool)
  args = parser.parse_args()
  production = args.production if args.production != None else False
  server = Server()
  server.start(production)

if __name__ == "__main__":
  main()