#!/usr/bin/python
import argparse
import os
import re
import subprocess
import sys
import textwrap

def get_peak_load_average(top_file):
    peak_load = 0.0
    pat = re.compile(r'load average: (\d+)\.(\d+)')
    for line in top_file:
        if 'load average' in line:
            la = pat.search(line).group()
            load = (float)(la.replace('load average: ', ''))
            if load > peak_load:
                peak_load = load
            
    return peak_load

def get_peak_avg_stats(infile):
    peak = 0
    total = 0
    num = 0
    for line in infile:
        try:
            stat = (float)(line)
        except:
            continue
        if stat > peak:
            peak = stat
        total += stat
        num += 1
    avg = total / num
    return peak, avg

def execute(args):
    test_name = getattr(args, "test_name", "")

    top_file = open('top_' + test_name)
    print "Peak Load:\t" + (str)(get_peak_load_average(top_file))

    os.system("sar -f sar_" + test_name + " | egrep -v 'user|Linux|Average|^$' | tr -s ' ' ' ' | cut -d' ' -f4 >cpu_" + test_name)
    cpu_file = open('cpu_' + test_name)
    peak, avg = get_peak_avg_stats(cpu_file)
    print "Peak CPU Usage:\t" + (str)(peak)
    print "Avg CPU Usage:\t" + (str)(avg)

    os.system("egrep -v 'connected|query|^$' ms_" + test_name + " | tr -s ' ' ' ' | cut -d' ' -f3 >queries_" + test_name)
    ms_file = open('queries_' + test_name)
    peak, avg = get_peak_avg_stats(ms_file)
    print "Peak Queries:\t" + (str)(peak)
    print "Avg Queries:\t" + (str)(avg)

    os.system("cat iostat_" + test_name + " | tr -s ' ' ' ' | cut -d' ' -f14 >disk_util_" + test_name)
    du_file = open('disk_util_' + test_name)
    peak, avg = get_peak_avg_stats(du_file)
    print "Peak Disk:\t" + (str)(peak)
    print "Avg Disk:\t" + (str)(avg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent('''\
        Example usage with valid parameters:
        ------------------------------------

            Required arguments: --test_name

                ->  test_name
                    name of the test of which to process the measured results
        '''))
    parser.add_argument("-t", "--test_name", type=str, help="Enter the parent directory containing mongodb.log* file(s)",
                        default="", metavar="")

    args_ = parser.parse_args()
    execute(args_)
