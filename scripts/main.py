import urllib.parse
import urllib.request
import json
from bs4 import BeautifulSoup

# データを読み込む

with open("./cache/channel_id.json") as fp:
  channel_id = json.load(fp)

outfile = open("./filter.txt", mode="w")

def out(text):
  return outfile.write(text + "\n")

def encodeURI(text, safe=""):
  # Pythonは '_.-~' をデフォルトでエンコードしません
  return urllib.parse.quote(text, safe=";,/?:@&=+$!*'()#"+safe)

def fetch(url):
  with urllib.request.urlopen(url) as res:
    return res.read().decode()

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

make("channels.txt", "Spammer channels", lambda line: ("a[href=\"/" + encodeURI(line.removeprefix("/")) + "\"]:upward(6)"))

# 多分 querySelector() の属性Selectorでは正規表現が使えない
# make("channel-regex.txt", "spammer channels (with regex)", lambda line: ("a[href=/\/" + encodeURI(line.removeprefix("/"), safe="^\\") + "/]:upward(6)"))

def make_reply_filter(line):
  if line not in channel_id:
    # エラーが起きない前提のコード
    res = fetch("https://youtube.com/"+line)
    soup = BeautifulSoup(res, 'html.parser')
    channel_id[line] = soup.find("meta", itemprop="identifier")["content"]

  return "##a[href=\"/channel/"+channel_id[line]+"\"]:upward(8)"

make("channels.txt", "Reply to spammers", make_reply_filter)

make("words.txt", "Spam words", lambda line: ("#content-text>span:has-text(/" + line + "/):upward(5)"))

make("templates.txt", "Template comments", lambda line: ("#content-text>span:has-text(\"" + line + "\"):upward(5)"))

# データを書き出す

with open('./cache/channel_id.json', 'wt') as f:
    json.dump(channel_id, fp, indent=2)

outfile.close()
