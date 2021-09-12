my $file = 'KLLN_salience_june2020_wordcount.pdf';
my $wordcount = `wc -w pdftotext $file`;

system("python", "../python/emailWordCount.py", $file, $wordcount) == 0 or die "emailWordCount.py script returned error $?";
