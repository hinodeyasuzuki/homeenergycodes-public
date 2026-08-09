# Home Energy Codes Public

　このリポジトリは、家庭のエコライフ情報を記録するための情報定義として利用できる、読み取り専用の静的 JSON API です。

　省エネ診断に関する項目以外に、家庭のエネルギー消費量・光熱費の保存項目、修理・中古品購入などを評価するための機器分類、など、家庭のエコ生活に関する定義を取得できます。

## 概要

- 診断項目や省エネ対策項目などの基本マスタデータを公開します。
- GitHub Pages などの静的ホスティング環境でそのまま利用できます。
- 認証不要で、CORS 許可済みのため、ブラウザから直接取得できます。

## 提供データ

主なデータソースは以下のとおりです。

- 省エネ診断入力項目: `api/v1/input.json`
- 省エネ対策項目: `api/v1/measures.json`
- 省エネ分野カテゴリ: `api/v1/cons.json`
- エネルギー種別: `api/v1/energy.json`
- エネルギー料金項目: `api/v1/energycost.json`
- 機器カテゴリ: `api/v1/applianceCategory.json`
- 機器マスタ: `api/v1/equip.json`
- メタ情報: `api/v1/meta.json`

## 追加資料

- 保存データの JSON Schema: `input/saved-input.schema.json`
- 保存データの形式説明: `input/saved-input-format.md`

## 使い方

```bash
curl https://hinodeyasuzuki.github.io/homeenergycodes-public/api/v1/input.json
```

サンプルプログラムは https://hinodeyasuzuki.github.io/myecoliferecords/ で公開されています。

または、JavaScript から次のように取得できます。

```javascript
fetch("https://hinodeyasuzuki.github.io/homeenergycodes-public/api/v1/input.json")
  .then((res) => res.json())
  .then((data) => console.log(data));
```


