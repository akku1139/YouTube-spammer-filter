import urllib.parse
import urllib.request
import urllib.error
import json
import re
import logging
logging.basicConfig(level=0)
from bs4 import BeautifulSoup

# データを読み込む

with open("./cache/channel_id.json") as fp:
  channel_id = json.load(fp)

with open("./cache/handle.json") as fp:
  handle = json.load(fp)

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
  if comment != "":
    out("\n! " + comment)
  logger = logging.getLogger("make")
  with open("./src/" + filename) as src:
    line_count = 0
    for line in src:
      line_count += 1
      line = line.strip()
      if line == "":
        continue
      if line.startswith("#"):
        continue
      ret = func(line)
      if ret == "" or ret == None:
        logger.info(f'{filename}:{line_count}: {line} was ignored')
        continue
      out("www.youtube.com###sections " + ret)

make("channels.txt", "Spammer channels", lambda line: ("a[href=\"/" + encodeURI(line) + "\"]:upward(6)"))

make("channels-prefix.txt", "spammer channels (with prefix)", lambda line: ("a[href^=\"/@" + encodeURI(line) + "\"]:upward(6)"))

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

  return "a[href=\"/channel/"+channel_id[line]+"\"]:upward(8)"

logger = logging.getLogger("reply")
make("channels.txt", "Reply to spammers", make_reply_filter)

make("channels-id.txt", "", lambda line: ("a[href=\"/channel/"+line+"\"]:upward(8)"))

re_ytInitialData = re.compile("var ytInitialData = (.+?);")
def make_id_filter(line):
  if line not in handle:
    try:
      # 429とかのエラーが起きない前提のコード
      res = fetch("https://youtube.com/channel/"+line)
      handle[line] = json.loads(re_ytInitialData.search(res).group(1))["header"]["pageHeaderRenderer"]["content"]["pageHeaderViewModel"]["metadata"]["contentMetadataViewModel"]["metadataRows"][0]["metadataParts"][0]["text"]["content"]
    except urllib.error.HTTPError as e:
      if e.code == 404:
        logger.warning("Channel not found: "+line)
      else:
        raise # if not 404 (eを再度投げる必要はない)
      return

  return "a[href=\"/" + encodeURI(handle[line]) + "\"]:upward(6)"

logger = logging.getLogger("id")
make("channels-id.txt", "Spammer channels (2)", make_id_filter)

make("words.txt", "Spam words", lambda line: ("#content-text>span:has-text(/" + line + "/):upward(5)"))

make("templates.txt", "Template comments", lambda line: ("#content-text>span:has-text(\"" + line + "\"):upward(5)"))

# データを書き出す

with open('./cache/channel_id.json', 'wt') as fp:
    json.dump(channel_id, fp, indent=2, ensure_ascii=False)

with open('./cache/handle.json', 'wt') as fp:
    json.dump(handle, fp, indent=2, ensure_ascii=False)

outfile.close()
