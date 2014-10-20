#!/usr/bin/env python

import os
import argparse
import yaml
import time
import subprocess


def run_backup(workdir, backup, logfile):
    logfile.write('\tStart backup ' + backup[0] + '\n')
    exclude = workdir + '/' + backup[0] + '.exclude'
    try:
        subprocess.check_call(['rsync', '-ae', 'ssh', '--delete', '--exclude-from=' + exclude, backup[1]['from'], backup[1]['to']])
        logfile.write('\tBackup ' + backup[0] + ' finished\n')
        return 1
    except subprocess.CalledProcessError as e:
        logfile.write('\tBackup ' + backup[0] + ' error, exit code ' + str(e.returncode) + '\n')
        return 0


def main():
    parser = argparse.ArgumentParser(description="backupApp arguments")
    parser.add_argument('configFile', type=argparse.FileType('r'), help="Config file specifying backups")
    parser.add_argument('workingDir', help="Working directory, where to find exclusion files and store logs")

    args = parser.parse_args()

    if not os.path.exists(args.workingDir) or not os.path.isdir(args.workingDir):
        raise Exception('Given working dir \'' + args.workingDir + '\' doesn\'t exist or is not a directory')

    config = yaml.load(args.configFile)
    working_dir = args.workingDir

    with open(working_dir + '/backupApp.log', 'a') as logfile:
        logfile.write(time.strftime("%c") + " Starting backup\n")
        successCount = 0
        for backup in config.items():
            successCount += run_backup(working_dir, backup, logfile)

        logfile.write(time.strftime("%c") + " Finished backup (" + str(successCount) + " sucessfull from " + str(len(config.items())) + ")\n")


if __name__ == '__main__':
    main()