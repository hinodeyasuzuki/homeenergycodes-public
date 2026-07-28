# Home Energy Codes Public

このリポジトリは、家庭の省エネ診断アプリ向けに利用できる、読み取り専用の静的 JSON API です。

## 概要

- 診断項目や省エネ対策項目などの基本マスタデータを公開します。
- GitHub Pages などの静的ホスティング環境でそのまま利用できます。
- 認証不要で、CORS 許可済みのため、ブラウザから直接取得できます。

## 提供データ

主なデータソースは以下のとおりです。

- 入力項目: `api/v1/input.json`
- 省エネ対策項目: `api/v1/measures.json`
- 消費量カテゴリ: `api/v1/cons.json`
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

または、JavaScript から次のように取得できます。

```javascript
fetch("https://hinodeyasuzuki.github.io/homeenergycodes-public/api/v1/input.json")
  .then((res) => res.json())
  .then((data) => console.log(data));
```

## 特色

- 静的ファイルのみで構成
- 追加サーバー構築不要
- API の利用・閲覧が容易
