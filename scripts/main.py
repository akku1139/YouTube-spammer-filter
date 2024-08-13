import urllib.parse

outfile = open("./filter.txt", mode="w")

def out(text):
  outfile.write(text + "\n")

out("! YouTube spam comment filter for Japanese")

def make(filename, comment, func):
  out("\n! " + comment)
  with open("./src/" + filename) as src:
    for line in src:
      out(func(line))

make("channels.txt", "spammer channels", lambda line: ("www.youtube.com##a[href=\"/" + urllib.parse.quote(line.removeprefix("/").removesuffix("\n"), safe="@") + "\"]:upward(6)"))

make("words.txt", "spam words", lambda line: ("###content-text>span:has-text(/" + line + "/):upward(5)"))

make("templates.txt", "template comments", lambda line: ("###content-text>span:has-text(" + line + "):upward(5)"))

outfile.close()
