use strict;
use warnings;

print "What is you favorite sport? ";
my $favoriteSport = <STDIN>;
chomp $favoriteSport;
$favoriteSport =~ s/^\s+|\s+$//g;
print "Thank you for telling me your favorite sport is " . lc($favoriteSport) . "!\n";

# if (uc($favoriteSport) eq "FOOTBALL") {
#     print("Now I know you must know a great deal about the gameplay of football, please explain all of the rules to me!\n");
#     my $footballExplanation = <STDIN>;

# }

unless (uc($favoriteSport) eq "FOOTBALL") {
    # So clearly the person does not love football the most,
    # So I cannot assume the person would know too much about all of the rule,
    # So then I have to go find all of the rules of football all by myself,
    # So then I should go straight to the official source, the NFL:
    # https://operations.nfl.com/media/5427/2021-nfl-rulebook.pdf

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

    # Scrape https://www.nfl.com/teams/ for my home team:
    # *My local football team is...*
    # Go to my local football team's home page, does my local team have its own rule page?

    # https://uhcougars.com/sports/football
    # I can even look up my local college football team if I want to be a Cougar fan

}
