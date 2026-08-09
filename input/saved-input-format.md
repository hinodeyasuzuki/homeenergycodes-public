# 保存形式 (saved-input JSON)

このドキュメントは、入力アプリが保存/エクスポートする JSON の形式を説明します。
機械検証には `saved-input.schema.json` を使用してください。

- スキーマ: `./saved-input.schema.json`
- ストレージキー: `homeenergycodes.savedInput`(localStorage。写真の画像データ本体は含まない)
- 写真の画像データ本体はIndexedDB(`homeenergycodes-pictures`)に保存され、localStorageには含まれない。JSONエクスポート時のみ`pictureBlobs`として同梱される。

## トップレベル構造

保存データ(localStorage)は次の8キーを持つ1つのオブジェクトです。

```json
{
  "input": {},
  "inputCounts": {},
  "room": {},
  "products": {},
  "energy": {},
  "energycost": {},
  "repairlog": {},
  "picture": {}
}
```

JSONエクスポート時は、これに加えて`pictureBlobs`(IndexedDBの内容のスナップショット)が同梱されます。詳細は「写真データの保存先」の節を参照。

保存データのキーごとの概要

- input: 省エネ診断のための情報
- inputCounts: 省エネ診断における、機器数
- room: 部屋
- products: 製品
- energy: 月別エネルギー消費量
- energycost: 月別光熱費
- repairlog: 修理履歴
- picture: 写真

## エンティティ概要

- input
  - キー: `i***` (診断項目ID input.jsonのid)
  - 値: 数値 または 数値配列(input.jsonのoptions.val)
- inputCounts
  - キー: cons.jsonの`countgroup`(なければcons自身のcode)。例 `RM`, `LI`, `TV`, `RF`, `CR`, `TR`
  - 値: 0以上の整数(そのグループに属する入力項目の入力欄の数)
- room
  - キー: `r***`
  - 値: `{ name, area, connected_room_ids }`
  - area : 部屋面積（畳）
  - connected_room_ids: キー(r***)
- products
  - キー: `e***`
  - 値: `{ name, equip_id, purchaseyear, purchasemonth, method, manufactureyear, room_id, watt, usagetime, frequency, maker, modelnumber, seller, enduseyear, favorite, repairlog_ids, picture_ids, memory, public_info }`
  - キーは本来は p***であるが、pictureで使われているので、equipmentのeをキーに使用
  - equip_id: equip.jsonのid
  - purchaseyear: 購入年
  - purchasemonth: 購入月(1-12,-1:月は不明,0:頃)
  - method: 入手方法 [
    { val: 1, label: "新品購入" },
    { val: 2, label: "新品プレゼント" },
    { val: 3, label: "中古購入" },
    { val: 4, label: "中古譲り受け" },
    { val: 5, label: "ごみを再利用" },
    { val: 6, label: "手作り" },
  ];
  - manufactureyear:　製造年
  - room_id: 部屋 roomのキー
  - watt: 消費電力(W)
  - usagetime: 使用時間（時間/回）
  - frequency: 使用頻度（回/年）
  - maker: 製造者
  - modelnumber: 製品ID
  - seller: 販売者
  - enduseyear: 使用終了年
  - favorite: 愛用品 (true/false)
  - repairlog_ids:修理履歴 repairlogのキーの配列[] 
  - picture_ids:写真 pictureのキー配列[] 
  - memory: 思い出
- energy / energycost
  - キー: `yyyymm` (例: `202612`)
  - 値: energy.jsonおよびenergycost.json の code をキーにした数値マップ
- repairlog
  - キー: `l***`
  - 値: `{ year, month, day, product_id, about, public_info, picture_ids, created_at }`
  - year: 年
  - month: 月
  - day: 日
  - product_id: 機器（productsのキー）
  - about: 概要
  - picture_ids: 写真 pictureのキー配列[] 
  - created_at: 作成日時
- picture
  - キー: `p***`
  - 値: `{ memo, created_at, sourceUrl }`（画像データURL本体はここには含まれず、IndexedDBに`p***`をキーとして保存される。`sourceUrl` はGoogle Photos等から取り込んだ場合の参照元URLで、未入力時は空文字列・期限切れの可能性あり。詳細は `docs/superpowers/specs/2026-07-27-photo-capture-design.md` および下記「写真データの保存先」参照）

## 写真データの保存先(IndexedDB)

- localStorageの容量(オリジンあたり5MB程度)を圧迫しないよう、写真の画像データURL本体は `homeenergycodes-pictures` というIndexedDBデータベース(オブジェクトストア `pictures`)に、`picture` のキー(`p***`)をそのままキーとして保存する。
- `data.picture[id]` (localStorage側)はメタデータ(`memo`/`created_at`/`sourceUrl`)のみを持ち、画像バイト列は持たない。
- **JSONエクスポート時**: `exportJson()` がIndexedDBの全件を読み出し、エクスポートするJSONに `pictureBlobs: { "p001": "data:image/jpeg;base64,...", ... }` という形で同梱する。単一ファイルでバックアップ・復元できるようにするための措置。
- **JSONインポート時**: `importJson()` がインポートしたJSONの `pictureBlobs` をIndexedDBへ書き戻す(既存のIndexedDBの内容は一旦クリアしてから書き込む)。`pictureBlobs` を持たない古い形式のエクスポートファイル(`picture[id].picdata` に直接画像データが入っている旧形式)をインポートした場合も、読み込み時に自動でIndexedDBへ移行する。
- `pictureBlobs` はlocalStorageの`data`には含まれない。JSONエクスポート/インポートの受け渡し時にのみ使われる一時的なキーである。

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
