# YouTube spam comment filter for Japanese

日本語圏の迷惑YouTubeコメントを一掃したいフィルター

誤ブロックの保証はしません

## 使い方

`filter.txt` を [uBlock Origin (推奨)](https://github.com/gorhill/uBlock) なり [AdGuard](https://adguard.com/ja/adguard-browser-extension/overview.html) なりに追加してください。

AdBlock Plus や AdBlocker Ultimate 等は絶対に使わないでください。 (詳しくは [Yuki2718/adblock2/wiki/よくある質問](https://github.com/Yuki2718/adblock2/wiki/%E3%82%88%E3%81%8F%E3%81%82%E3%82%8B%E8%B3%AA%E5%95%8F) を参照)

`https://raw.githubusercontent.com/akku1139/YouTube-spammer-filter/main/filter.txt`

<details>
<summary>AdBlock Plus style filter subscribe link</summary>

`abp:subscribe?location=https%3A%2F%2Fraw.githubusercontent.com%2Fakku1139%2FYouTube-spammer-filter%2Fmain%2Ffilter.txt&title=YouTube%20spam%20comment%20filter%20for%20Japanese`
</details>


## TODOs

- [ ] 部分一致フィルター (ラフレシア対策)
- [ ] 迷惑コメントにリプライする人も迷惑なので消す
- [ ] 自動通報?
- [ ] チャンネル名フィルター (難しい)
- [ ] チャンネルIDキャッシュ もしくは登録をチャンネルIDで行う
- [ ] ハンドルを変えて逃げられないようにチャンネルidで管理する
- [ ] 時々チャンネルの生存確認を行ってルールの無駄を減らす
