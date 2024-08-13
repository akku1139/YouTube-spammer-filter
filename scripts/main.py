import urllib.parse

outfile = open("./filter.txt", mode="w")

def out(text):
  outfile.write(text + "\n")

out("! spammer channels")

with open("./src/channels.txt") as src:
  for line in src:
    out("www.youtube.com##a[href=\"/" + urllib.parse.quote(line.removeprefix("/").removesuffix("\n"), safe="@") + "\"]:upward(6)")

out("\n! spam words")

with open("./src/words.txt") as src:
  for line in src:
    out("###content-text>span:has-text(/" + line + "/):upward(5)")

outfile.close()
