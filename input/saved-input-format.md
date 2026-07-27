# 保存形式 (saved-input JSON)

このドキュメントは、入力アプリが保存/エクスポートする JSON の形式を説明します。
機械検証には `saved-input.schema.json` を使用してください。

- スキーマ: `./saved-input.schema.json`
- ストレージキー: `homeenergycodes.savedInput`

## トップレベル構造

保存データは次の7キーを持つ1つのオブジェクトです。

```json
{
  "input": {},
  "room": {},
  "products": {},
  "energy": {},
  "energycost": {},
  "repairlog": {},
  "picture": {}
}
```

## エンティティ概要

- input
  - キー: `i***` (診断項目ID)
  - 値: 数値 または 数値配列
- room
  - キー: `r***`
  - 値: `{ name, area, connected_room_ids }`
- products
  - キー: `e***`
  - 値: `{ name, equip_id, purchaseyear, purchasemonth, method, manufactureyear, room_id, watt, usagetime, frequency, enduseyear, favorite, repairlog_ids, picture_ids, memory }`
- energy / energycost
  - キー: `yyyymm` (例: `202612`)
  - 値: コードをキーにした数値マップ
- repairlog
  - キー: `l***`
  - 値: `{ year, month, day, equip_id, about, picture_ids, created_at }`
- picture
  - キー: `p***`
  - 値: `{ picdata, memo, created_at }`（`picdata` はリサイズ・JPEG圧縮済みのdata URL。詳細は `docs/superpowers/specs/2026-07-27-photo-capture-design.md` 参照）

## マスタ参照

- `products.equip_id` は `/api/v1/equip.json` の `id` を参照
- `energy` は `/api/v1/energy.json` の `code` を参照
- `energycost` は `/api/v1/energycost.json` の `code` を参照

## バリデーション例

Node.js (AJV) の例:

```js
import Ajv from "ajv";
import schema from "./saved-input.schema.json" assert { type: "json" };
import data from "./saved-input.json" assert { type: "json" };

const ajv = new Ajv({ allErrors: true });
const validate = ajv.compile(schema);
if (!validate(data)) {
  console.error(validate.errors);
}
```
