pcrefuzz is designed to generate all (or some random) strings which should be matched by a given regular expression. If you need to fuzz the regex engine, then maybe try [regfuzz](http://code.google.com/p/regfuzz/).

Intended usage:
```
#python pcreFuzz.py [options] -r <regular expression>
#
#Options:
#  --version             show program's version number and exit
#  -h, --help            show this help message and exit
#  -b INT, --breadth=INT
#                        Maximum fuzzing string length - used to fuzz pcre
#                        commands: '*' or '+' or '{0,}' or '{1,}'. (Default:
#                        10000)
#  -c FLOAT, --breadthCoverage=FLOAT
#                        Percentage coverage of fuzzing string lengths. In
#                        range 0.0 to 1.0. Example: For '--breadth=1000 -c 0.5'
#                        would mean 500 of the possible 1000 string lengths
#                        will randomly selected and tested. (Default: 0.1)
#  -d FLOAT, --depthCoverage=FLOAT
#                        Percentage coverage of available characters within a
#                        set - used to fuzz commands: [a-zA-Z]. In range 0.0 to
#                        1.0. Example: For '-d 0.5' used on set [a-zA-Z] would
#                        result in a random sample of 23 letters would be
#                        tested. (Default: 0.5)
#  -e, --edgeConditions  Test the edge conditions. (Default: True)
#  -m, --minimalCoverage
#                        Ensure all possible strings are covered by the fuzzer.
#                        Example: m/(bob|joe)/ produces test cases 'bob' and
#                        'joe'. (Default: true)
#  -r STRING, --regexp=STRING
#                        Regular expression to be fuzzed.
#  -u FLOAT, --utf8Coverage=FLOAT
#                        Percentage coverage of available characters within a
#                        UTF-8 set. In range 0.0 to 1.0. (Default: 0.01)
```