# blog formatter
# july 3rd 2021
# oscar yu
# a tool to reformat text files into html paragraphs that are also readable

import os
import sys

file = open(os.path.join(sys.path[0],"input.txt"), "r", encoding="utf8")
output = open(os.path.join(sys.path[0],"output.txt"), "w")

print()
for line in file:
  if line.strip() == "":
      continue
  checker = ""
  output.write("<p>\n")
  while len(line) > 80:
      lineSplit = line[80:].split(" ", 1)
      firstHalf = line[:80] + lineSplit[0]
      output.write("\t" + firstHalf + "\n")
      #print("HALFDONE")
      checker = firstHalf
      if len(lineSplit) == 1:
          break
      line = lineSplit[1]
  if checker != line:
      output.write("\t" + line)
  output.write("</p>\n\n")
  #print("FINAL LINE")

print("DONE")
input()
file.close()
output.close()


