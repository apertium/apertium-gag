import sys, libhfst, glob;

if len(sys.argv) <= 1: #{
	print('test.py <lang code>');
	sys.exit(-1);
#}

lang = sys.argv[1];

istr1 = libhfst.HfstInputStream('../'+lang+'.automorf.hfst');
anal = istr1.read();
#anal.remove_epsilons();

istr2 = libhfst.HfstInputStream('../'+lang+'.autogen.hfst');
gene = istr2.read();
#gene.remove_epsilons();

testf = glob.glob('*.tsv');

print(testf);
err = 0;
corr = 0;
for f in testf: #{
	print(f + ':');
	tf = open(f).read().strip().split('\n');
	print('Generation:');
	for t in tf: #{
		row = t.strip().split('\t');
		g_res = gene.lookup(row[0]);

		if g_res[0][0] == row[1]: #{
			print('+\t%s\t%s' % (row[0], g_res[0][0]));
			corr += 1;
		else: #{	
			print('-\t%s\t%s\t%s' % (row[0], row[1], g_res[0][0]));
			err += 1;
		#}
	#}
	print('Analysis:');
	for t in tf: #{
		row = t.strip().split('\t');
		a_res = anal.lookup(row[1]);
		found = False;
		for r in a_res: #{
			if row[0] == r[0]: found = True;
		#}
		if found: #{
			print('+\t%s\t%s' % (row[1], row[0]));
			corr += 1;
		else: #{	
			print('-\t%s\t%s\t%s' % (row[1], row[0], a_res));
			err += 1;
		#}
	#}
	print('');
#}

print('PASS:\t%.2f%%' % ((corr/(err+corr))*100.0));
print('%d\t%d\t%d' % (err+corr, corr, err));
