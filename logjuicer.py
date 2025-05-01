import subprocess
import sys


class LogJuicer():
    """Python client for Logjuicer
    https://github.com/logjuicer/logjuicer
    """
    def __init__(self, logpath):
        self.logfile = logpath
        self.baseline = self.baseline()

    def baseline(self):
        return 'baselines/' + str.split(self.logfile, '_')[0] + '.log'

    def juice(self):
        juicer = "/home/apalanis/.cargo/bin/logjuicer"
        config = 'config.yaml'
        command = [juicer, "--config", config, "diff",
                   self.baseline, self.logfile]
        print("RUNNING COMMAND", command)
        process = subprocess.run(command, capture_output=True, text=True)
        print(process)
        diff = process.stdout
        return diff

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage help:\n\
        python logjuicer.py <logfile>")
        sys.exit(1)
    logpath = sys.argv[1]
    logjuicer = LogJuicer(logpath)
    print(logjuicer.juice())
