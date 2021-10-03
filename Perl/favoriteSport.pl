use strict;
use warnings;

print "What is you favorite sport? ";
my $favoriteSport = <STDIN>;
chomp $favoriteSport;
$favoriteSport =~ s/^\s+|\s+$//g;
print "Thank you for telling me your favorite sport is " . lc($favoriteSport) . "!\n";

if (uc($favoriteSport) eq "FOOTBALL") {
    print("Now I know you must know a great deal about the gameplay of football, please explain all of the rules to me!\n");
    my $footballExplanation = <STDIN>;

}
