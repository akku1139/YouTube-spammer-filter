import urllib.parse

outfile = open("./filter.txt", mode="w")

def out(text):
  return outfile.write(text + "\n")

def encodeURI(text, safe=""):
  # Pythonは '_.-~' をデフォルトでエンコードしません
  return urllib.parse.quote(text, safe=";,/?:@&=+$!*'()#"+safe)

out("! Homepage: https://github.com/akku1139/YouTube-spammer-filter")
out("! Title: YouTube spam comment filter for Japanese")

def make(filename, comment, func):
  out("\n! " + comment)
  with open("./src/" + filename) as src:
    for line in src:
      if line.strip() == "":
        continue
      if line.startswith("#"):
        continue
      out("www.youtube.com###sections " + func(line.strip()))

make("channels.txt", "spammer channels", lambda line: ("a[href=\"/" + encodeURI(line.removeprefix("/")) + "\"]:upward(6)"))

make("channel-regex.txt", "spammer channels (with regex)", lambda line: ("a[href=/\/" + encodeURI(line.removeprefix("/"), safe="^\\") + "/]:upward(6)"))

make("words.txt", "spam words", lambda line: ("#content-text>span:has-text(/" + line + "/):upward(5)"))

make("templates.txt", "template comments", lambda line: ("#content-text>span:has-text(\"" + line + "\"):upward(5)"))

outfile.close()
