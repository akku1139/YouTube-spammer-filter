import urllib.parse
import urllib.request
import urllib.error
import json
import logging
logging.basicConfig(level=0)
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
  logger = logging.getLogger("make")
  with open("./src/" + filename) as src:
    line_count = 0
    for line in src:
      line_count += 1
      if line.strip() == "":
        continue
      if line.startswith("#"):
        continue
      ret = func(line.strip())
      if ret == "" or ret == None:
        logger.info(f'{filename}:{line_count}: {line} was ignored')
        continue
      out("www.youtube.com###sections " + ret)

make("channels.txt", "Spammer channels", lambda line: ("a[href=\"/" + encodeURI(line.removeprefix("/")) + "\"]:upward(6)"))

# 多分 querySelector() の属性Selectorでは正規表現が使えない
# 無駄に正規表現使うのは重いので前方一致とかで良いと思う
# make("channel-regex.txt", "spammer channels (with regex)", lambda line: ("a[href=/\/" + encodeURI(line.removeprefix("/"), safe="^\\") + "/]:upward(6)"))

def make_reply_filter(line):
  if line not in channel_id:
    try:
      # 429とかのエラーが起きない前提のコード
      res = fetch("https://youtube.com/"+encodeURI(line))
      soup = BeautifulSoup(res, 'html.parser')
      channel_id[line] = soup.find("meta", itemprop="identifier")["content"]
    except urllib.error.HTTPError as e:
      if e.code == 404:
        logger.warning("Channel not found: "+line)
      else:
        raise # if not 404 (eを再度投げる必要はない)
      return

  return "##a[href=\"/channel/"+channel_id[line]+"\"]:upward(8)"

logger = logging.getLogger("reply")
make("channels.txt", "Reply to spammers", make_reply_filter)

make("words.txt", "Spam words", lambda line: ("#content-text>span:has-text(/" + line + "/):upward(5)"))

make("templates.txt", "Template comments", lambda line: ("#content-text>span:has-text(\"" + line + "\"):upward(5)"))

# データを書き出す

with open('./cache/channel_id.json', 'wt') as fp:
    json.dump(channel_id, fp, indent=2, ensure_ascii=False)

outfile.close()
