# Copyright (c) 2010, Igneous Networks Limited
# All rights reserved.

#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions
#are met:
#1. Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#2. Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#3. Neither the name of Igneous Networks Limited nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#POSSIBILITY OF SUCH DAMAGE.

from optparse import OptionParser
import re, sys

# Example of how could work: python pcreFuzz.py -r "m/BLAH/i" | testHarness

class pcreFuzz:

	# set global variables and initialise functions
	def __init__(self, options):
		self.options = options
		self.regexp = self.options.regexp

		
		
	def run(self):
		print "DEBUG Options: %s" % self.options
		
#		# validate the regular expression
#		if self.validatePCREStructure(self.regexp):
#			print "DEBUG: The regular expression is structured correctly: %s" % self.options.regexp
#		else:
#			print "DEBUG: Error in the structure of regular expression: %s" % self.options.regexp
#			sys.exit("Error...")

		# explode the regular expression
		self.explodeRegularExpression(self.regexp)

		
		

	def validatePCREStructure(self, regexp):
		print "This is where we validate the PCRE structure"
		return False

	def explodeRegularExpression(self, regexp):
		print "This is where the regexp explodes... into an NFA / graph"

		testList = ['\.', '\C', '\d', '\D', '\h', '\H', '\R', '\s', '\S', '\v', '\V', '\W']
		
		for charType in testList:
			print "DEBUG: Testing %s" % charType
			print "DEBUG: utf8..."
			utf8_result = self.expandCharacterTypes(charType, True, False)
			print "DEBUG: UTF-8 result - %s" % utf8_result
			
			print "DEBUG: ascii..."
			ascii_result = self.expandCharacterTypes(charType, False, False)
			print "DEBUG: ASCII result - %s" % ascii_result
		
	#def expandCharacterClasses(characterClass):
		
	# Input: Character Class e.g. <string>[a-zA-Z] 
	# Output: Array of byte ranges e.g. <array>(97,122,65,90)
		# [...]       positive character class
        # [^...]      negative character class
		# The character types \d, \D, \p, \P, \s, \S, \w, and \W may also appear in  a  character  class
        # [x-y]       range (can be used for hex characters)
        # [[:xxx:]]   positive POSIX named set
        # [[:^xxx:]]  negative POSIX named set

        # alnum       alphanumeric
        # alpha       alphabetic
        # ascii       0-127
        # blank       space or tab
        # cntrl       control character
        # digit       decimal digit
        # graph       printing, excluding space
        # lower       lower case letter
        # print       printing, including space
        # punct       printing, excluding alphanumeric
        # space       whitespace
        # upper       upper case letter
        # word        same as \w
        # xdigit      hexadecimal digit
	
	def expandCharacterTypes(self, characterType, utf8, dotall):
	# Input: CharacterType e.g. <string>\d, False, False
	# Output: Returns a list of UTF-8 code point ranges
	# Todo: Handle locale changes for \p, \P, \w,\W

		# .          any character except newline;
        #              in dotall mode, any character whatsoever
		if characterType == '\.':
			# TODO: check this is correct
			# the //m option enbles . to match newlines

			# Unicode as per RFC: 3629 - U+0 to U+10FFFF, excluding U+D800 to U+DFFF.
			# In  UTF-8 mode, characters with values greater than 128 never match \d,
			# \s, or \w, and always match \D, \S, and \W.
			if utf8:
				if dotall:
					return[0x000000,0x00d800,0x00dfff,0x10ffff]
				else:
					return[0x000000,0x000009,0x00000b,0x00d800,0x00dfff,0x10ffff]
			else:
				if dotall:
					return[0x000000,0x0000ff]
				else:
					return[0x000000,0x000009,0x00000b,0x0000ff]
        # \C         one byte, even in UTF-8 mode (best avoided)
		elif characterType == '\C':
			if utf8:
				return[0x000000,0x00d800,0x00dfff,0x10ffff]
			else:
				return[0x000000,0x0000ff]
        # \d         a decimal digit
		elif characterType == '\d':
			if utf8:
				return[0x000030,0x000039]
			else:
				return[0x000030,0x000039]
        # \D         a character that is not a decimal digit
		elif characterType == '\D':
			if utf8:
				return[0x000000,0x00002f,0x00003a,0x10ffff]
			else:
				return[0x000000,0x00002f,0x00003a,0x0000ff]
        # \h         a horizontal whitespace character
		elif characterType == '\h':
			if utf8:
				return[0x000009,0x000009,0x000020,0x000020,0x0000a0,0x0000a0,0x001680,0x001680,0x00180e,0x00180e,0x002000,0x00200a,0x00202f,0x00202f,0x00205f,0x00205f,0x003000,0x003000]
				# U+0009     Horizontal tab
				# U+0020     Space
				# U+00A0     Non-break space
		
				# U+1680     Ogham space mark
				# U+180E     Mongolian vowel separator
				# U+2000     En quad
				# U+2001     Em quad
				# U+2002     En space
				# U+2003     Em space
				# U+2004     Three-per-em space
				# U+2005     Four-per-em space
				# U+2006     Six-per-em space
				# U+2007     Figure space
				# U+2008     Punctuation space
				# U+2009     Thin space
				# U+200A     Hair space
				# U+202F     Narrow no-break space
				# U+205F     Medium mathematical space
				# U+3000     Ideographic space
			else:
				return[0x000009,0x000009,0x000020,0x000020,0x0000a0,0x0000a0]
		# \H         a character that is not a horizontal whitespace character
		elif characterType == '\H':
			if utf8:
				return[0x000000,0x000008,0x00000a,0x000019,0x000021,0x00009f,0x0000a1,0x00167f,0x001681,0x00180d,0x00180f,0x001fff,0x00200b,0x00202e,0x002030,0x00205e,0x002060,0x002fff,0x003001,0x10ffff]
			else:
				return[0x000000,0x000008,0x00000a,0x000019,0x000021,0x00009f,0x0000a1,0x0000ff]
        # \R         a newline sequence
		elif characterType == '\R':
			if utf8:
				return[0x00000a,0x00000d,0x000085,0x000085,0x002028,0x002029]
			else:
				return[0x00000a,0x00000d,0x000085,0x000085]
        # \s         a whitespace character
		elif characterType == '\s':
			if utf8:
				return[0x000009,0x00000a,0x00000c,0x00000d,0x000020,0x000020]
			else:
				return[0x000009,0x00000a,0x00000c,0x00000d,0x000020,0x000020]
        # \S         a character that is not a whitespace character
		elif characterType == '\S':
			if utf8:
				return[0x000000,0x000008,0x00000b,0x00000b,0x00000e,0x00001f,0x000021,0x10ffff]
			else:
				return[0x000000,0x000008,0x00000b,0x00000b,0x00000e,0x00001f,0x000021,0x0000ff]
		# \v         a vertical whitespace character
		elif characterType == '\v':
			if utf8:
				return[0x00000a,0x00000d,0x000085,0x000085,0x002028,0x002029]
				# U+000A     Linefeed
				# U+000B     Vertical tab
				# U+000C     Formfeed
				# U+000D     Carriage return
				# U+0085     Next line
				# U+2028     Line separator
				# U+2029     Paragraph separator
			else:
				return[0x00000a,0x00000d,0x000085,0x000085]
        # \V         a character that is not a vertical whitespace character
		elif characterType == '\V':
			if utf8:
				return[0x000000,0x000009,0x00000e,0x000084,0x000086,0x002027,0x00202a,0x10ffff]
			else:
				return[0x000000,0x000009,0x00000e,0x000084,0x000086,0x0000ff]
        # \w         a "word" character									# only across ASCII space
		elif characterType == '\w':
		#TODO: Work out which of the international locale below 255 are applicable
			if utf8:
				return[0x000030,0x000039,0x000041,0x00005a,0x00005f,0x00005f,0x000061,0x00007a]
			else:
				return[0x000030,0x000039,0x000041,0x00005a,0x00005f,0x00005f,0x000061,0x00007a]
        # \W         a "non-word" character								# only across ASCII space
		elif characterType == '\W':
		#TODO: Work out which of the international locale below 255 are applicable
			if utf8:
				return[0x000000,0x000029,0x00003a,0x000040,0x00005b,0x00005e,0x000060,0x000060,0x00007b,0x10ffff]
			else:
				return[0x000000,0x000029,0x00003a,0x000040,0x00005b,0x00005e,0x000060,0x000060,0x00007b,0x0000ff]
        # \p{xx}     a character with the xx property			- NOT SUPPORTED - TODO
        # \P{xx}     a character without the xx property		- NOT SUPPORTED - TODO
        # \X         an extended Unicode sequence				- NOT SUPPORTED - TODO

        # \a        alarm, that is, the BEL character (hex 07)
        # \cx       "control-x", where x is any character
        # \e        escape (hex 1B)
        # \f        formfeed (hex 0C)
        # \n        linefeed (hex 0A)
        # \r        carriage return (hex 0D)
        # \t        tab (hex 09)
        # \ddd      character with octal code ddd, or back reference
        # \xhh      character with hex code hh
        # \x{hhh..} character with hex code hhh..
	   

	def utf8CodeToHex(utf8Code):
		return

		
		
	
#Parses CLI arguments
def parseArguments():
	parser = OptionParser(usage="usage: python %prog [options] -r <regular expression>", version="%prog 0.0.0")
	parser.add_option("-b", "--breadth", dest="maxFuzzStringLength",
					help="Maximum fuzzing string length - used to fuzz pcre commands: '*' or '+' or '{0,}' or '{1,}'. (Default: 10000)",
					metavar="INT", type="int")
	parser.add_option("-c", "--breadthCoverage", dest="percentBreadthCoverage",
					help="Percentage coverage of fuzzing string lengths. In range 0.0 to 1.0. Example: For '--breadth=1000 -c 0.5' would mean 500 of the possible 1000 string lengths will randomly selected and tested. (Default: 0.1)",
					metavar="FLOAT", type="float")
	parser.add_option("-d", "--depthCoverage", dest="percentDepthCoverage",
					help="Percentage coverage of available characters within a set - used to fuzz commands: [a-zA-Z]. In range 0.0 to 1.0. Example: For '-d 0.5' used on set [a-zA-Z] would result in a random sample of 23 letters would be tested. (Default: 0.5)",
					metavar="FLOAT", type="float")
	parser.add_option("-e", "--edgeConditions", dest="edgeConditions",
					help="Test the edge conditions. (Default: True)",
					action="store_true")
	#parser.add_option("-f", "--pcreFormat", dest="pcreFormat",
	#				help="Format for regular expression and list of valid modifiers. Example: For Snort 2.8.5.1: (/<regex>/|m<delim><regex><delim>)[ismxAEGRUBPHMCO]")
			#  modifier              description               Perl corresponding

			#  PCRE_CASELESS         case insensitive match      /i
			#  PCRE_MULTILINE        multiple lines match        /m
			#  PCRE_DOTALL           dot matches newlines        /s
			#  PCRE_DOLLAR_ENDONLY   $ matches only at end       N/A
			#  PCRE_EXTRA            strict escape parsing       N/A
			#  PCRE_EXTENDED         ignore whitespaces          /x
			#  PCRE_UTF8             handles UTF8 chars          built-in
			#  PCRE_UNGREEDY         reverses * and *?           N/A
			#  PCRE_NO_AUTO_CAPTURE  disables capturing parens   N/A (*)
	parser.add_option("-m", "--minimalCoverage", dest="minCoverage",
					help="Ensure all possible strings are covered by the fuzzer. Example: m/(bob|joe)/ produces test cases 'bob' and 'joe'. (Default: true)",
					action="store_true")
	
	parser.add_option("-r", "--regexp", dest="regexp",
					help="Regular expression to be fuzzed.", metavar="STRING", type="string")
	parser.add_option("-u", "--utf8Coverage", dest="percentUTF8Coverage",
					help="Percentage coverage of available characters within a UTF-8 set. In range 0.0 to 1.0. (Default: 0.01)",
					metavar="FLOAT", type="float")

	parser.set_defaults(maxFuzzStringLength=10000,percentBreadthCoverage=0.1,percentDepthCoverage=0.5,percentUTF8Coverage=0.01,edgeConditions=True,minCoverage=True)
	
	(options, args) = parser.parse_args()
	
	# Ensure there is a pcre rule included
	if not options.regexp:
		parser.error("Please specify the a PCRE rule.")
	
	pcreFuzzer = pcreFuzz(options)
	pcreFuzzer.run()

		
if __name__ == "__main__":
	parseArguments()


