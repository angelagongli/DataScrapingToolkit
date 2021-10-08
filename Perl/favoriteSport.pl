use strict;
use warnings;

print "What is you favorite sport? ";
my $favoriteSport = <STDIN>;
chomp $favoriteSport;
$favoriteSport =~ s/^\s+|\s+$//g;
print "Thank you for telling me your favorite sport is " . lc($favoriteSport) . "!\n";

unless (uc($favoriteSport) eq "FOOTBALL") {
    # So clearly the person does not love football the most,
    # So I cannot assume the person would know too much about all of the rule,
    # So then I have to go find all of the rules of football all by myself,
    # So then I should go straight to the official source, the NFL:
    # https://operations.nfl.com/media/5427/2021-nfl-rulebook.pdf

    use LWP::Simple 'getstore';
    my $res = getstore('https://operations.nfl.com/media/5427/2021-nfl-rulebook.pdf', '2021NFLRulebook.pdf');
    print $res, "\n";

    my @args = ("pdftotext", "2021NFLRulebook.pdf");
    system(@args) == 0
        or die "system @args failed: $?";

    my $file = '2021NFLRulebook.txt';
    open(FH, $file)
        or die("File $file not found");

    # *The first rule of football is...*
    # Ideally I can pull and condense the rules of football from the official rulebook PDF
    # (RULE \d+, SECTION \d+ and ARTICLE \d+\. should not otherwise appear, so by RegEx on the heading?)
    # Presented in the following format:

    # RULE 1 THE FIELD
    # SECTION 1 DIMENSIONS
    # ARTICLE 1. PLAYING LINES.
    # ARTICLE 2. FIELD.
    # SECTION 2 MARKINGS
    # ARTICLE 1. LINE MARKINGS.
    # ARTICLE 2. INBOUND LINES.
    # ARTICLE 3. GOAL LINE.
    # ARTICLE 4. GROUND RULES.
    # ... Etc.
    # + Item under Article when it exists

    while (my $String = <FH>) {
        # *The first rule of football is...*
        if ($String =~ /RULE 1\s+/) {
            print "Expecting: RULE 1 THE FIELD\n";
            print "$String \n";
        } elsif ($String =~ /SECTION \d+/) {
            print "Start of Section\n";
            print "$String \n";
        } elsif ($String =~ /ARTICLE \d+\./) {
            print "Start of Article\n";
            print "$String \n";
        } elsif ($String =~ /RULE \d+/) {
            last;
        }
    }
    close(FH);

    # Scrape https://www.nfl.com/teams/ for my home team:
    # *My local football team is...*
    # Go to my local football team's home page, does my local team have its own rule page?
    use LWP::Simple qw(get);
    use HTML::TreeBuilder 5 -weak;

    my $url = "https://www.nfl.com/teams/";
    my $html = get $url;
    my $tree = HTML::TreeBuilder->new;
    $tree->parse($html);

    # TODO: Look for "Houston Texan" and then go to the home page

}
