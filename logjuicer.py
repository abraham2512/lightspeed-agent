import subprocess
import sys


class LogJuicer():
    """Python client for Logjuicer
    https://github.com/logjuicer/logjuicer
    """
    def __init__(self, logpath):
        self.logfile = logpath
        self.baseline = self.baseline()
        self.juicer = "/home/apalanis/.cargo/bin/logjuicer"
        self.config = 'logjuicer.config'

    def baseline(self):
        return 'baselines/' + str.split(self.logfile, '_')[0] + '.log'

    def logtype(self):
        return str.split(self.logfile, '_')[0]

    def juice(self):

        command = [self.juicer, "--config", self.config, "diff",
                   self.baseline, self.logfile]
        print("Juicing logfile with:", command)
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode != 0:
            print(f"Error during logjuicer execution: {process.stderr}")
            return None
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
