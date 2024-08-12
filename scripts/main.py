import urllib.parse

out = open("./filter.txt", mode="w")

with open("./src/channels.txt") as src:
  for line in src:
    l = "www.youtube.com##a[href=\"/" + urllib.parse.quote("@純白の天使ラフメシア_3".removeprefix("/"), safe="@") + "\"]:upward(ytd-comment-view-model)"
    print(line, ":", l)
    out.write(l + "\n")

out.close()
