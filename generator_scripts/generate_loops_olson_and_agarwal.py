#!/usr/bin/python

import argparse
import sys
import traceback
from subprocess import check_call
import os

# as in Olson and Agarwal's IJRR paper, generate a number of outlier loops, to up 4000.
# #outlier schedule (as per table 1 of the paper) is: 10, 100, 200, 300, 400, 500, 1000, 2000, 3000, 4000


n_outliers = [10, 100, 200, 300, 400, 500, 1000, 2000, 3000, 4000]
n_trials = 1

class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


if __name__ == "__main__":

	parser = DefaultHelpParser(description='Generate outlier loops like in Olson and Agarwal\'s IJRR paper.')

	parser.add_argument("original", help = "Path to the original, outlier-free, dataset file (in g2o format).")
	parser.add_argument("output_directory", help = "Output directory for outlier files")
	parser.add_argument("--outlier-generator", default=os.path.normpath(os.path.dirname(os.path.realpath(__file__))+"/../bin/outlier_generator"), help="Path to the outlier_generator executable")
	parser.add_argument("--outlier-format", default='%(n_outliers)02d_%(trial)02d.outliers', help="Format of outlier files, keys to be used: n_outliers, trial. Default: '%%(n_outliers)05d_%%(trial)02d.outliers'")
	parser.add_argument("--seed-format", default='1%(n_outliers)02d%(trial)02d', help="Like --outlier-format, but used to generate a seed number. Same keys as above. Default: '1%%(n_outliers)05d%%(trial)02d'")
	parser.add_argument("--loop-information", type=float, nargs=2, default=[42,42], help="Information values for generated outlier loops. Default: [42,42]")


	args = parser.parse_args()

	if not os.path.isfile(args.outlier_generator):
		print "ERROR: path to outlier_generator executable does not exist!"
		exit(1)

	if os.path.exists(args.output_directory) and not os.path.isdir(args.output_directory):
		print "ERROR: output dir exists, but is not a directory!"
		exit(2)
	elif not os.path.exists(args.output_directory):
		os.makedirs(args.output_directory)
	
	

	try:

		for no in range(0,len(n_outliers)):
			for nt in range(0,n_trials):
				cur = {'n_outliers': no, 'trial': nt }
				commandline = [args.outlier_generator, args.original, os.path.normpath(args.output_directory + "/" + args.outlier_format % cur ), ]                
				commandline += ['--false-loops', str(n_outliers[no]), '--seed', args.seed_format % cur ]
				commandline += ['--loop-variance-translation', str(1.0/(args.loop_information[0])), '--loop-variance-rotation', str(1.0/(args.loop_information[1])) ]
				if no > 0:
					prev = cur
					prev['n_outliers'] = no-1
					commandline += ['--previous-outliers', os.path.normpath(args.output_directory + "/" + args.outlier_format % prev )]

				print "*************************"
				print " ".join(commandline)
				check_call(commandline, stdout=sys.stdout, stderr=sys.stderr)
		

	except:
		traceback.print_exc(file=sys.stderr)
		exit(100)
