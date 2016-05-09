#!/usr/bin/env python

import sys

chars_per_group = 2
groups_per_line = 16

try:
    if len(sys.argv) == 1 or sys.argv[1] == "-":
        fp = sys.stdin
    else:
        fp = open(sys.argv[1], 'rb')
except KeyboardInterrupt as e:
    raise e
except Exception:
    print ""
    print "Utility to extract hex dump lines from a text file and convert them to binary data."
    print "Easily configured to support nearly any hex dump format."
    print ""
    print "Usage: %s [input file] [characters per group] [groups per line]" % sys.argv[0]
    print ""
    print "If no input file is provided, or if input file is '-' (no quotes), ASCII hex data is read from stdin."
    print "Binary data will be printed to stdout."
    print ""
    print "Default characters per group: %d" % chars_per_group
    print "Default groups per line: %d" % groups_per_line
    print ""
    print "For example, if you have a file named 'file.txt' that contains ASCII hex data formatted like:"
    print ""
    print "\t 00000000:  0001 0203"
    print "\t 00000008:  0405 0607"
    print "\t 00000010:  0809 0A0B"
    print ""
    print "Then that's 4 characters per group, and 2 groups per line; so %s usage would be:" % sys.argv[0]
    print ""
    print "\t %s file.txt 4 2" % sys.argv[0]
    print ""
    print "All lines and characters before and after the ASCII hex will be ignored."
    print ""
    sys.exit(1)

try:
    chars_per_group = int(sys.argv[2], 0)
    groups_per_line = int(sys.argv[3], 0)
except KeyboardInterrupt as e:
    raise e
except Exception:
    pass

line_count = 0
byte_count = 0
sys.stderr.write("Searching %s for ASCII hex characters...\n" % (fp.name))

for line in fp.readlines():
    hexvals = []
    hexwords = []
    line_count += 1

    line = line.strip()
    words = line.split()
    words.reverse()

    for word in words:
        if len(word) == chars_per_group:
            hexwords.append(word)

    if len(hexwords) >= groups_per_line:
        hexwords = hexwords[:groups_per_line]
        hexwords.reverse()

        hexline = ''.join(hexwords)
        hexbytes = [hexline[i:i+2] for i in range(0, len(hexline), 2)]

        for byte in hexbytes:
            try:
                val = int(byte, 16)
                hexvals.append(chr(val))
                if len(hexvals) == (groups_per_line * chars_per_group):
                    break
            except Exception as e:
                continue

    if hexvals:
        sys.stdout.write("".join(hexvals))
        byte_count += len(hexvals)

sys.stderr.write("Found %d lines of text containing ASCII hex codes; created %d binary bytes.\n" % (line_count, byte_count))
fp.close()
