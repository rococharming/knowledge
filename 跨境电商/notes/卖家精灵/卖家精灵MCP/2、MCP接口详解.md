# 一、产品与竞品分析

核心目标：了解某个商品是什么、卖得怎么样，以及竞争对手有哪些。

| 序号  | MCP Code                        | 中文名称         | 核心作用                 |
| --- | ------------------------------- | ------------ | -------------------- |
| 1   | `product_node`                  | 查产品类目        | 查询类目 ID、类目路径和产品数量    |
| 2   | `product_research`              | 选产品          | 按销量、销售额、价格等条件筛选商品    |
| 3   | `competitor_lookup`             | 查竞品          | 查询 ASIN 的销量、销售额等竞争数据 |
| 4   | `asin_competitor`               | ASIN 竞品查询    | 查找与目标 ASIN 具有竞争关系的商品 |
| 5   | `asin_detail`                   | ASIN 详情      | 查询商品标题、价格、BSR、评分等信息  |
| 6   | `asin_coupon_trend`             | ASIN 优惠趋势    | 查询商品历史优惠变化           |
| 7   | `asin_detail_with_coupon_trend` | ASIN 详情及优惠趋势 | 同时获取商品详情与优惠趋势        |
| 8   | `asin_sales_trend`              | ASIN 销量趋势    | 查询父体、子体的历史销量和销售额     |
| 9   | `asin_prediction`               | ASIN 销量预测    | 根据 ASIN 查询估算销量       |
| 10  | `bsr_prediction`                | BSR 销量预测     | 根据大类 BSR 排名估算销量      |
| 11  | `keepa_info`                    | 商品历史趋势       | 查询价格、BSR、评分、评论等历史变化  |

## product_node（查产品类目）

`product_node`是卖家精灵 MCP 提供的产品类目查询接口，主要用于查询亚马逊的类目 ID、类目名称、类目层级路径以及类目下的产品数量。

### 请求参数

| 参数            | 类型     | 必填  | 作用                   | 示例                   |
| ------------- | ------ | --- | -------------------- | -------------------- |
| `marketplace` | String | 是   | 指定亚马逊站点              | `US`                 |
| `nodeIdPath`  | String | 否   | 指定类目节点路径             | `2619525011:3741271` |
| `keyword`     | String | 否   | 通过类目关键词/节点 ID/类目名称搜索 | `Dishwashers`        |
| `month`       | String | 否   | 指定查询的历史月份，格式yyyyMM   | `202507`             |
- `marketplace`是必填参数，用于指定查询哪个亚马逊站点。因为亚马逊不同站点的商品分类体系可能存在差异，同一类商品在不同站点对应的类目节点也不一定相同。
- `nodeIdPath` 不是一个普通数字，而是由多个类目节点 ID 组成的路径字符串。例如

```text
2619525011:3741271 
```

对应：

```text
Appliances（家电）
    │
    └── Dishwashers（洗碗机）
```

如果继续往下一级：

```text
2619525011:3741271:3741281
```

则表示：

```text
Appliances
    └── Dishwashers
            └── Built-In Dishwashers
```

- `keyword`是搜索关键词，用于根据类目关键词/节点ID/类目名称搜索类目。
- `month`是查询月份，用于指定历史月份。

>MCP 可以通过 returnFields 参数选择性的返回某些字段，可以大幅降低上下文 的 Token 量

### 返回参数

| 参数                    | 类型      | 含义           | 示例                       |
| --------------------- | ------- | ------------ | ------------------------ |
| `nodeIdPath`          | String  | 完整类目节点 ID 路径 | `2619525011:3741271`     |
| `nodeLabelPath`       | String  | 完整英文类目路径     | `Appliances:Dishwashers` |
| `products`            | Integer | 类目下的产品数量     | `42`                     |
| `nodeLabelLocale`     | String  | 当前类目的中文名称    | 洗碗机                      |
| `nodeLabelPathLocale` | String  | 完整中文类目路径     | 大家电:洗碗机                  |

## product_research（选产品）

`product_research` 是卖家精灵 MCP 提供的**产品筛选接口**，主要用于根据销量、销售额、价格、评分、上架时间、品牌等条件，从亚马逊商品数据库中筛选符合要求的产品。

### 请求参数

`product_research` 请求参数比较多，但不需要一次全部使用。

为了便于理解，按照参数的实际作用整理。

#### 基础查询与类目

这组参数决定：**你想从哪个站点、哪个类目、哪个时间范围寻找商品。**

| 参数                | 类型      | 必填  | 含义                                                               | 示例                   |
| ----------------- | ------- | --- | ---------------------------------------------------------------- | -------------------- |
| `marketplace`     | String  | 是   | 指定亚马逊站点                                                          | `US`                 |
| `month`           | String  | 否   | 查询月份，格式为 `yyyyMM`                                                | `202609`             |
| `keyword`         | String  | 否   | 商品搜索关键词                                                          | `dining chairs`      |
| `matchType`       | Integer | 否   | 关键词匹配方式，1词组匹配，2模糊匹配，3精准匹配。默认 2                                   | `2`                  |
| `excludeKeywords` | String  | 否   | 排除指定关键词                                                          | `folding`            |
| `nodeIdPaths`     | List    | 否   | 指定一个或多个类目节点路径                                                    | 通过 `product_node` 获取 |
| `nodeIdPathEqual` | Boolean | 否   | 若为false，查询包含指定类目及其子类亩；若为true，查询直接归属于当前类目的商品，不自动包含下级目录。默认为 false。 | `true`               |
| `filterSub`       | String  | 否   | 是否启用子类目排名筛选，`Y`：是                                                | 只有在指定类目时才会生效         |

这里有几个需要重点理解的参数。

- `keyword`：通过**产品标题**中的关键词进行匹配，添加后的筛选结果中仅展示包含该关键词的产品。

- `matchType`：匹配模式。

| 参数值 | 匹配方式    | **说明**                                                         |
| --- | ------- | -------------------------------------------------------------- |
| `1` | 词组匹配    | 从产品标题中匹配完全包含查询词组的产品。关键词词组没有特定顺序，支持无序匹配。  <br>如果输入词组，结果匹配其中一个词组 |
| `2` | 模糊匹配，默认 | 从产品标题中匹配包含部分查询关键词的产品。<br>如果输入多个关键词或词组，结果匹配其中一个关键词              |
| `3` | 精准匹配    | 从产品标题中匹配与查询关键词或词组完全一致的产品。关键词顺序不能调换。                            |
详见：[关键词匹配](https://www.sellersprite.com/v3/knowledge/feature/how-to-match-keywords)

- `nodeIdPaths`：指定商品类目

假设你只想研究 Dining Chairs，而不是全部包含 `chairs` 的商品。

可以先使用：

`product_node` → 找到 Dining Chairs 的节点路径 → 再传入 `product_research`。

这样能够更准确地限制产品范围。

- `nodeIdPathEqual`

	- `nodeIdPathEqual = true`：精确查询指定类目。
	- `nodeIdPathEqual = false`：查询指定类目及其子类目，默认值。

#### 价格与利润参数

| 参数          | 类型    | 含义    | 示例    |
| ----------- | ----- | ----- | ----- |
| `minPrice`  | Float | 最低售价  | `80`  |
| `maxPrice`  | Float | 最高售价  | `150` |
| `minProfit` | Float | 最低毛利率 | `20`  |
| `maxProfit` | Float | 最高毛利率 | `40`  |

>产品毛利率指的是从商品售价中扣除亚马逊佣金和 FBA 费用后，剩余金额占商品售价的比例。

例如，你想筛选美国站价格在 80～150 美元之间的吧椅。可以使用 `minPrice` 和 `maxPrice`。

#### 销量与销量额参数

这组参数是选品时最重要的部分之一。

| 参数             | 类型      | 含义        | 示例       |
| -------------- | ------- | --------- | -------- |
| `minUnits`     | Integer | 最低月销量（父体） | `500`    |
| `maxUnits`     | Integer | 最高月销量（父体） | `2000`   |
| `minAmzUnit`   | Integer | 最低月子体销量   | `100`    |
| `maxAmzUnit`   | Integer | 最高月子体销量   | `1000`   |
| `minRevenue`   | Float   | 最低月销售额    | `50000`  |
| `maxRevenue`   | Float   | 最高月销售额    | `200000` |
| `minUnitsCr`   | Float   | 最低月销量增长率  | `20`     |
| `maxUnitsCr`   | Float   | 最高月销量增长率  | `50`     |
| `minRevenueCr` | Float   | 最低月销售额增长率 | `10`     |
| `maxRevenueCr` | Float   | 最高月销售额增长率 | `40`     |
#### BSR排名参数

| 参数              | 类型      | 含义                | 示例      |
| --------------- | ------- | ----------------- | ------- |
| `minBsr`        | Integer | 大类 BSR 最高排名（数值下界） | `1`     |
| `maxBsr`        | Integer | 大类 BSR 最低排名（数值上界） | `10000` |
| `minBsrCv`      | Integer | BSR 最低增长数         | `3`     |
| `maxBsrCv`      | Integer | BSR 最高增长数         | `100`   |
| `minBsrCr`      | Float   | BSR 最低增长率         | `10`    |
| `maxBsrCr`      | Float   | BSR 最高增长率         | `50`    |
| `minSubBsrRank` | Integer | 子类目排名范围下界         | `1`     |
| `maxSubBsrRank` | Integer | 子类目排名范围上界         | `100`   |
注意`minSubBsrRank`和`maxSubBsrRank`只有在参数 filterSub=Y 时才生效。

#### 评分与评分参数

| 参数             | 类型      | 含义       | 示例    |
| -------------- | ------- | -------- | ----- |
| `minRating`    | Float   | 最低星级评分   | `3`   |
| `maxRating`    | Float   | 最高星级评分   | `4.5` |
| `minRatings`   | Integer | 最低评分数量   | `10`  |
| `maxRatings`   | Integer | 最高评分数量   | `200` |
| `minRatingsCv` | Integer | 最低月新增评分数 | `5`   |
| `maxRatingsCv` | Integer | 最高月新增评分数 | `30`  |
#### 品牌与卖家参数

| 参数               | 类型      | 含义        | 示例       |
| ---------------- | ------- | --------- | -------- |
| `includeBrands`  | String  | 包含指定品牌    | `COLAMY` |
| `excludeBrands`  | String  | 排除指定品牌    | `COLAMY` |
| `includeSellers` | String  | 包含指定卖家    | 卖家名称或标识  |
| `excludeSellers` | String  | 排除指定卖家    | 卖家名称或标识  |
| `minSellers`     | Integer | 最低卖家数量    | `1`      |
| `maxSellers`     | Integer | 最高卖家数量    | `5`      |
| `sellerNation`   | String  | 卖家所属国家或地区 | 依官方枚举    |
| `fulfillment`    | String  | 配送方式      | `FBA`    |
#### 商品属性与 Listing 参数

| 参数               | 类型      | 含义                     | 示例      |
| ---------------- | ------- | ---------------------- | ------- |
| `availableMonth` | Integer | 上架月份范围条件               | 依官方枚举   |
| `dimensionType`  | String  | 商品尺寸类型筛选               | 依官方枚举   |
| `weightUnit`     | String  | 重量单位，默认 g              | `g`     |
| `minWeights`     | Float   | 最低重量                   | `1000`  |
| `maxWeights`     | Float   | 最高重量                   | `10000` |
| `minVariations`  | Integer | 最少变体数量                 | `1`     |
| `maxVariations`  | Integer | 最多变体数量                 | `5`     |
| `minFba`         | Float   | 最低 FBA 运费              | `10`    |
| `maxFba`         | Float   | 最高 FBA 运费              | `30`    |
| `minLqs`         | Float   | 最低 Listing 质量得分        | `60`    |
| `maxLqs`         | Float   | 最高 Listing 质量得分        | `100`   |
| `badgeBS`        | String  | 是否有 Best Seller 标识     | `Y`     |
| `badgeAC`        | String  | 是否有 Amazon's Choice 标识 | `Y`     |
| `badgeNR`        | String  | 是否有 New Release 标识     | `Y`     |
| `variation`      | String  | 是否包含变体 ASIN            | `N`     |
>特别注意`variation`，N标识含变体，Y才表示不含变体。

#### 分页与排序参数

| 参数            | 类型      | 含义        | 默认值           |
| ------------- | ------- | --------- | ------------- |
| `page`        | Integer | 查询第几页     | `1`           |
| `size`        | Integer | 每页返回多少条商品 | `50`          |
| `order`       | Object  | 排序配置      | —             |
| `order.field` | String  | 排序字段      | `total_units` |
| `order.desc`  | Boolean | 是否降序排列    | `true`        |
其中：

- `size` 最大为 100。
- 单组查询结果最多可获取 2,000 条。
- 若需要更多商品，需要细分筛选条件。

### 返回参数

`product_research` 返回的是一批符合筛选条件的商品，而不是单个商品。

返回数据主要包括：

1. 查询结果的分页信息。
2. 每个商品的详细数据。

#### 查询结果信息

| 返回参数          | 类型      | 含义         |
| ------------- | ------- | ---------- |
| `total`       | Integer | 符合条件的商品总数  |
| `pages`       | Integer | 查询结果总页数    |
| `page`        | Integer | 当前页码       |
| `size`        | Integer | 每页商品数量     |
| `items`       | List    | 当前页返回的商品列表 |
| `took`        | Integer | 查询耗时       |
| `order`       | Object  | 排序信息       |
| `order.field` | String  | 排序字段       |
| `order.desc`  | Boolean | 是否降序排序     |

#### 商品基本信息

| 返回参数            | 类型     | 中文含义         |
| --------------- | ------ | ------------ |
| `asin`          | String | 商品 ASIN      |
| `title`         | String | 商品标题         |
| `brand`         | String | 商品品牌         |
| `brandUrl`      | String | 品牌链接         |
| `imageUrl`      | String | 商品图片         |
| `parent`        | String | 父 ASIN       |
| `nodeId`        | Long   | 类目节点 ID      |
| `nodeIdPath`    | String | 完整类目节点路径     |
| `nodeLabelPath` | String | 商品所属类目路径     |
| `availableDate` | Long   | 商品上架日期，时间戳格式 |

#### 销量、销售额与BSR

| 返回参数          | 类型      | 中文含义       |
| ------------- | ------- | ---------- |
| `units`       | Integer | 父体月销量      |
| `unitsGr`     | Float   | 月销量增长率     |
| `amzUnit`     | Integer | 子体近 30 日销量 |
| `amzUnitDate` | Date    | 子体销量数据更新日期 |
| `revenue`     | Float   | 父体月销售额     |
| `bsrId`       | String  | BSR 所属类目标识 |
| `bsr`         | Integer | 大类 BSR 排名  |
| `bsrCv`       | Integer | BSR 排名变化数  |
| `bsrCr`       | Float   | BSR 排名变化率  |
| `symbol`      | String  | 是否畅销标识     |

#### 价格、利润与物流

| 返回参数               | 类型     | 中文含义               |
| ------------------ | ------ | ------------------ |
| `price`            | Float  | 商品售价               |
| `primePrice`       | Float  | Prime 价格，`-1` 表示没有 |
| `profit`           | Float  | 卖家精灵计算的利润率         |
| `fba`              | Float  | FBA 配送费用           |
| `deliveryPrice`    | Float  | 卖家运费，`-1` 表示没有     |
| `fulfillment`      | String | 配送方式               |
| `weight`           | String | 商品重量               |
| `dimension`        | String | 商品尺寸               |
| `dimensionsType`   | String | 商品尺寸类型             |
| `pkgDimensions`    | String | 包装尺寸               |
| `pkgDimensionType` | String | 包装尺寸类型             |
| `pkgWeight`        | String | 包装重量               |

#### 评分、评论及Listing信息

| 返回参数          | 类型      | 中文含义          |
| ------------- | ------- | ------------- |
| `rating`      | Float   | 商品星级评分        |
| `ratings`     | Integer | 评分数量          |
| `ratingsRate` | Float   | 留评率           |
| `ratingsCv`   | Integer | 月度新增评分数       |
| `ratingDelta` | Integer | 近 30 天新增评论数   |
| `lqs`         | Float   | Listing 质量得分  |
| `variations`  | Integer | 变体数量          |
| `sku`         | String  | SKU 属性，如颜色、尺寸 |

#### 卖家信息

| 返回参数           | 类型      | 中文含义              |
| -------------- | ------- | ----------------- |
| `sellers`      | Integer | 卖家数量              |
| `sellerId`     | String  | Buy Box 卖家 ID     |
| `sellerName`   | String  | Buy Box 卖家名称      |
| `sellerNation` | String  | Buy Box 卖家所属国家或地区 |
#### 商品标识与子类目

| 返回参数                    | 类型      | 中文含义               |
| ----------------------- | ------- | ------------------ |
| `badge`                 | Object  | 商品标识集合             |
| `badge.bestSeller`      | String  | Best Seller 标识     |
| `badge.amazonChoice`    | String  | Amazon's Choice 标识 |
| `badge.newRelease`      | String  | New Release 标识     |
| `badge.ebc`             | String  | 是否具有 A+ 页面         |
| `badge.video`           | String  | 是否具有视频             |
| `subcategories`         | List    | 子类目排名列表            |
| `subcategories[].code`  | String  | 子类目代码              |
| `subcategories[].rank`  | Integer | 子类目 BSR 排名         |
| `subcategories[].label` | String  | 子类目名称              |

## competitor_lookup（查竞品）

`competitor_lookup`是卖家精灵 MCP 提供的竞品数据查询接口，主要用于根据 ASIN、品牌、类目或关键词，查询亚马逊商品销量、销售额、价格、BSR排名、评分及其他竞争数据。

简单理解：**当你已经找到一批竞品 ASIN，想批量获取它们的销售表现时，就可以使用 `competitor_lookup`。**

它支持一次传入最多 40 个 ASIN。

`competitor_lookup`主要解决三个问题：

- 批量查询竞品：一次查询多个 ASIN 的商品数据
-  查询销量表现：获取父体销量、子体销量及销售额
- 研究品牌和卖家：按品牌、卖家、类目等条件查找商品

例如，你已经收集了 20 款 Dining Chairs 的 ASIN，希望比较它们的：

- 月销量和月销售额
- 价格
- BSR 排名
- 星级评分及评分数
- 上架时间
- FBA 配送费用

这种情况下，可以使用 `competitor_lookup` 一次获取多个商品的信息，而不需要逐个调用 `asin_detail`。

**需要注意：`competitor_lookup` 不是自动寻找相似竞品的接口。**

如果你只有一个 ASIN，希望 AI 自动寻找与它竞争关系较强的其他 ASIN，应该使用 `asin_competitor`。

#### 请求参数

`competitor_lookup` 包含 **13 个顶层请求参数**，其中 `order` 对象还有两个子参数。

| 参数                | 类型      | 必填  | 中文含义        | 示例或取值                     |
| ----------------- | ------- | --- | ----------- | ------------------------- |
| `marketplace`     | String  | 是   | 亚马逊站点       | `US`                      |
| `month`           | String  | 否   | 查询月份        | `202609`、`nearly`         |
| `brand`           | String  | 否   | 品牌筛选        | `COLAMY`                  |
| `sellerName`      | String  | 否   | 卖家筛选        | 卖家名称                      |
| `asins`           | List    | 否   | 批量查询 ASIN   | 最多 40 个                   |
| `nodeIdPath`      | String  | 否   | 指定商品类目节点    | 类目节点路径                    |
| `nodeIdPathEqual` | Boolean | 否   | 是否精确匹配类目    | `true`、`false`，默认`false`  |
| `keyword`         | String  | 否   | 商品关键词       | `dining chairs`           |
| `matchType`       | Integer | 否   | 关键词匹配方式     | 1：词组匹配，2：模糊匹配，3：精准匹配；默认：2 |
| `variation`       | String  | 否   | 是否包含变体 ASIN | `N`：含变体、`Y`：不含变体          |
| `page`            | Integer | 否   | 页码          | 默认 `1`                    |
| `size`            | Integer | 否   | 每页返回数量      | 默认 `50`，最大 `100`          |
| `order`           | Object  | 否   | 排序配置        | 包含 `field`、`desc`         |

`order` 的子参数：

| 参数            | 类型      | 含义   | 默认值           |
| ------------- | ------- | ---- | ------------- |
| `order.field` | String  | 排序字段 | `total_units` |
| `order.desc`  | Boolean | 是否降序 | `true`        |

field 的常见值如下：

| 参数值                    | 中文名称          | 参数描述                        |
| ---------------------- | ------------- | --------------------------- |
| `total_units`          | 月销量           | 按商品预估月销量排序，通常为父体销量          |
| `total_amount`         | 月销售额          | 按商品预估月销售额排序                 |
| `bsr_rank`             | BSR 排名        | 按商品所属大类的 BSR 排名排序，数值越小排名越靠前 |
| `price`                | 价格            | 按商品售价排序                     |
| `rating`               | 评分            | 按商品平均星级评分排序，最高为 5 分         |
| `reviews`              | 评分数           | 按商品累计星级评分数量排序               |
| `profit`               | 毛利率           | 按卖家精灵估算的商品毛利率排序             |
| `reviews_rate`         | 留评率           | 按商品估算留评率排序                  |
| `available_date`       | 上架时间          | 按商品首次上架日期排序                 |
| `questions`            | Q&A 数量        | 按商品买家问答数量排序                 |
| `total_units_growth`   | 月销量增长率        | 按商品月销量增长比例排序                |
| `total_amount_growth`  | 月销售额增长率       | 按商品月销售额增长比例排序               |
| `reviews_increasement` | 月新增评分数        | 按商品月度新增评分数量排序               |
| `bsr_rank_cv`          | 近 7 天 BSR 变化数 | 按商品近 7 天 BSR 排名的数值变化排序      |
| `bsr_rank_cr`          | 近 7 天 BSR 变化率 | 按商品近 7 天 BSR 排名的变化比例排序      |
| `amz_unit`             | 子体销量          | 按具体子 ASIN 近 30 天的预估销量排序     |
#### 返回参数

`competitor_lookup` 返回的数据与 `product_research` 高度相似，主要包含商品信息、销量、销售额、BSR、评分、价格及物流数据。

## asin_competitor

`asin_competitor`（ASIN竞品查询）

`asin_competitor` 是卖家精灵 MCP 提供的**竞品发现接口**。输入一个亚马逊商品的 ASIN，卖家精灵会返回与该商品具有较强竞争关系的其他商品，以及这些竞品的销量、销售额、价格、BSR、评分等数据。

简单理解：**你已经找到一款餐椅，但不知道它的直接竞争对手有哪些，就可以使用 `asin_competitor` 自动寻找相关竞品。**

这个接口与上面介绍的 `competitor_lookup` 不同：

- **`asin_competitor`：** 已知一个 ASIN，寻找它的竞争对手。
- **`competitor_lookup`：** 已知一批 ASIN，查询这些商品的销售数据。
#### 请求参数

该接口只有 3 个请求参数，其中 2 个必填。

| 参数            | 类型      | 必填  | 参数名称    | 参数描述                 |
| ------------- | ------- | --- | ------- | -------------------- |
| `marketplace` | String  | 是   | 亚马逊站点   | 指定查询哪个亚马逊站点，例如 `US`  |
| `asin`        | String  | 是   | 目标 ASIN | 输入需要寻找竞品的商品 ASIN     |
| `size`        | Integer | 否   | 返回数量    | 控制返回多少个竞品，官方示例为 `20` |
注意：`size = 20`不是保证一定返回 20 个竞品，实际返回数量取决于卖家精灵是否有足够的匹配数据。

#### 返回参数

该接口返回的是一个竞品列表。每个竞品包含商品基础信息、销量、销售额、价格、评分、BSR、卖家及物流信息。

#####  商品基本信息

| 返回参数            | 类型     | 参数名称    | 参数描述          |
| --------------- | ------ | ------- | ------------- |
| `asin`          | String | ASIN    | 竞品的商品标识       |
| `title`         | String | 商品标题    | 竞品 Listing 标题 |
| `brand`         | String | 品牌      | 商品所属品牌        |
| `brandUrl`      | String | 品牌链接    | 品牌相关页面地址      |
| `imageUrl`      | String | 商品图片    | 商品主图 URL      |
| `parent`        | String | 父 ASIN  | 商品所属父体        |
| `nodeId`        | Long   | 类目节点 ID | 商品所属类目节点      |
| `nodeIdPath`    | String | 类目节点路径  | 完整类目 ID 路径    |
| `nodeLabelPath` | String | 类目名称路径  | 商品所属类目层级      |
| `availableDate` | Long   | 上架时间    | 商品上架日期，以时间戳表示 |
##### 销量、销售额及 BSR

| 返回参数          | 类型      | 参数名称     | 参数描述                |
| ------------- | ------- | -------- | ------------------- |
| `units`       | Integer | 父体月销量    | 整个父体 Listing 的预估月销量 |
| `unitsGr`     | Float   | 月销量增长率   | 父体月销量的增长比例          |
| `amzUnit`     | Integer | 子体销量     | 子 ASIN 近 30 日预估销量   |
| `amzSales`    | Float   | 子体销售额    | 子体的预估销售金额           |
| `amzUnitDate` | Date    | 子体销量更新日期 | 子体销量数据的更新时间         |
| `revenue`     | Float   | 父体月销售额   | 整个父体的预估月销售额         |
| `bsrId`       | String  | BSR 类目标识 | 商品 BSR 所属类目的标识      |
| `bsr`         | Integer | BSR 排名   | 商品的大类 BSR 排名        |
| `bsrCv`       | Integer | BSR 变化数  | BSR 排名变化的数值         |
| `bsrCr`       | Float   | BSR 变化率  | BSR 排名的变化比例         |
注意：这里的销量、销售额均属于卖家精灵提供的估算数据，不是竞争对手后台的真实订单记录

##### 价格、利润与物流

| 返回参数               | 类型     | 参数名称     | 参数描述                 |
| ------------------ | ------ | -------- | -------------------- |
| `price`            | Float  | 商品价格     | 商品售价                 |
| `primePrice`       | Float  | Prime 价格 | Prime 相关价格，`-1` 表示没有 |
| `profit`           | Float  | 利润率      | 卖家精灵估算的利润率           |
| `fba`              | Float  | FBA 配送费  | 预估 FBA 配送费用          |
| `deliveryPrice`    | Float  | 卖家运费     | 卖家运费，`-1` 表示没有       |
| `fulfillment`      | String | 配送方式     | `AMZ`、`FBA` 或 `FBM`  |
| `weight`           | String | 商品重量     | 商品重量信息               |
| `dimension`        | String | 商品尺寸     | 商品尺寸信息               |
| `dimensionsType`   | String | 商品尺寸类型   | 亚马逊尺寸分段              |
| `pkgDimensions`    | String | 包装尺寸     | 商品包装尺寸               |
| `pkgDimensionType` | String | 包装尺寸类型   | 包装对应的尺寸分段            |
| `pkgWeight`        | String | 包装重量     | 商品包装重量               |

##### 评分与 Listing 信息

| 返回参数          | 类型      | 参数名称         | 参数描述        |
| ------------- | ------- | ------------ | ----------- |
| `rating`      | Float   | 星级评分         | 商品平均星级      |
| `ratings`     | Integer | 评分数          | 累计星级评分数量    |
| `ratingsRate` | Float   | 留评率          | 卖家精灵估算的留评比例 |
| `ratingsCv`   | Integer | 月新增评分数       | 评分数量的月度变化   |
| `ratingDelta` | Integer | 近 30 天新增评论数  | 新增评论数量      |
| `lqs`         | Float   | Listing 质量得分 | 商品页面质量评分    |
| `variations`  | Integer | 变体数量         | 商品变体数量      |
| `sku`         | String  | SKU 属性       | 商品颜色、尺寸等属性  |
| `symbol`      | String  | 是否畅销         | 商品畅销标识字段    |

##### 卖家信息

| 返回参数           | 类型      | 参数名称          | 参数描述              |
| -------------- | ------- | ------------- | ----------------- |
| `sellers`      | Integer | 卖家数量          | 销售该商品的卖家数量        |
| `sellerId`     | String  | Buy Box 卖家 ID | 获得主要购买入口的卖家标识     |
| `sellerName`   | String  | Buy Box 卖家    | 获得主要购买入口的卖家名称     |
| `sellerNation` | String  | 卖家所属地         | Buy Box 卖家所属国家或地区 |

##### 商品标识及子类目排名

| 返回参数                    | 类型      | 参数名称            | 参数描述          |
| ----------------------- | ------- | --------------- | ------------- |
| `badge`                 | Object  | 商品标识            | 商品标识集合        |
| `badge.bestSeller`      | String  | Best Seller     | 畅销商品标识        |
| `badge.amazonChoice`    | String  | Amazon's Choice | 亚马逊推荐标识       |
| `badge.newRelease`      | String  | New Release     | 新品标识          |
| `badge.ebc`             | String  | A+ 页面           | 是否有 A+ 内容     |
| `badge.video`           | String  | 视频              | 是否有商品视频       |
| `subcategories`         | List    | 子类目排名           | 商品的子类目 BSR 数据 |
| `subcategories[].code`  | String  | 子类目代码           | 子类目节点标识       |
| `subcategories[].rank`  | Integer | 子类目 BSR         | 对应子类目的 BSR 排名 |
| `subcategories[].label` | String  | 子类目名称           | 对应排名的类目名称     |

## asin_detail（ASIN详情）

`asin_detail`是卖家精灵 MCP 提供的商品详情查询接口，主要用于根据一个 ASIN 获取亚马逊商品的基本信息，包括商品标题、品牌、价格、上架日期、BSR排名、评论数、评分、配送方式、变体信息等。

### 请求参数

| 参数            | 类型     | 必填  | 含义             | 示例           |
| ------------- | ------ | --- | -------------- | ------------ |
| `marketplace` | String | 是   | 指定亚马逊站点        | `US`         |
| `asin`        | String | 是   | 指定需要查询的商品 ASIN | `B0GYWDDJPD` |

需要查询商品基本信息，需要制定亚马逊站点和ASIN。

### 返回参数

#### 商品基本信息

|返回参数|类型|中文含义|说明|
|---|---|---|---|
|`asin`|String|ASIN|商品的唯一识别编号|
|`asinUrl`|String|商品链接|对应的亚马逊商品详情页|
|`title`|String|商品标题|Listing 的标题|
|`brand`|String|品牌|商品所属品牌|
|`brandUrl`|String|品牌链接|品牌相关页面地址|
|`imageUrl`|String|商品图片|商品图片 URL|
|`zoomImageUrl`|String|商品大图|更高分辨率的图片 URL|
|`dimensions`|String|商品尺寸|商品尺寸信息|
|`weight`|String|商品重量|商品重量信息|
|`availableDate`|Long|上架日期|商品上架时间|
|`createdTime`|Long|创建时间|Listing 相关记录的创建时间|
|`updatedTime`|Long|更新时间|数据记录的更新时间|
#### 类目与 BSR 信息

| 返回参数                  | 类型      | 中文含义     | 说明                                        |
| --------------------- | ------- | -------- | ----------------------------------------- |
| `nodeId`              | String  | 类目节点 ID  | 当前商品所属类目的节点标识                             |
| `nodeIdPath`          | String  | 类目节点路径   | 完整的类目 ID 路径                               |
| `nodeLabelPath`       | String  | 英文类目路径   | 商品所属类目的英文层级                               |
| `nodeLabelPathLocale` | String  | 中文类目路径   | 对应的中文类目层级                                 |
| `bsrId`               | String  | BSR 类目标识 | BSR 所属的类别标识                               |
| `bsrLabel`            | String  | BSR 类目名称 | 对应的 BSR 排名类目                              |
| `bsrRank`             | Integer | BSR 排名   | 商品在对应类目中的畅销排名                             |
| `subcategories`       | Object  | 子类目排名信息  | 包含rank（子类目排名）、code（子类目 code）、label（子类目标签） |

`subcategories` 中还包含以下字段：

| 子字段     | 类型      | 含义         |
| ------- | ------- | ---------- |
| `rank`  | Integer | 子类目 BSR 排名 |
| `code`  | String  | 子类目代码      |
| `label` | String  | 子类目名称      |

这里最重要的是 `bsrRank`以及子类`subcategories` 的`rank`。

#### 价格与促销信息

| 返回参数            | 类型     | 中文含义     | 说明                    |
| --------------- | ------ | -------- | --------------------- |
| `price`         | Float  | 商品价格     | 接口获取的商品售价             |
| `primePrice`    | Float  | Prime 价格 | Prime 相关售价，`-1` 表示没有  |
| `deliveryPrice` | Float  | 卖家运费     | 卖家运费字段，`-1` 表示没有      |
| `coupon`        | String | 优惠券      | 商品优惠券信息，如 \[save $20] |
`coupon`还包含以下字段`amazonChoice`：

| 子字段          | 类型     | 含义                   |
| ------------ | ------ | -------------------- |
| amazonChoice | String | amzon choice 标识，Y或者N |
#### 评分与评论信息

| 返回参数              | 类型      | 中文含义   | 说明              |
| ----------------- | ------- | ------ | --------------- |
| `rating`          | Float   | 星级评分   | 例如 4.5 分        |
| `ratings`         | Integer | 评分数量   | 参与星级评分的数量       |
| `reviews`         | Integer | 评论数量   | 文字评论等 Review 数量 |
| `variantRatings`  | Integer | 子体评分数  | 与子体相关的评分统计      |
| `variantReviews`  | Integer | 子体评论数  | 与子体相关的评论统计      |
| `firstRatingDate` | Long    | 首次评分日期 | 首次评分记录时间        |
| `questions`       | Integer | 商品问答数  | 买家问答数量          |

#### 卖家与配送方式

| 返回参数          | 类型      | 中文含义  | 说明         |
| ------------- | ------- | ----- | ---------- |
| `sellerId`    | String  | 卖家 ID | 亚马逊卖家的识别编号 |
| `sellerName`  | String  | 卖家名称  | 销售商品的卖家    |
| `fulfillment` | String  | 配送方式  | 例如 FBA     |
| `sellers`     | Integer | 卖家数量  | 同一商品的卖家数量  |
| `marketplace` | String  | 亚马逊站点 | 例如 US      |
#### Listing内容与变体信息

| 返回参数            | 类型      | 中文含义         | 说明              |
| --------------- | ------- | ------------ | --------------- |
| `features`      | List    | 五点描述         | 商品的主要卖点描述       |
| `overviews`     | String  | 商品详情         | JSON 格式的详情信息字符串 |
| `lqs`           | Integer | Listing 质量得分 | 卖家精灵的页面质量评分     |
| `parent`        | String  | 父 ASIN       | 商品所属父体 ASIN     |
| `variationList` | List    | 变体列表         | 变体 ASIN 及属性信息   |
| `variations`    | Integer | 变体数量         | 商品变体数量          |
| `skuList`       | List    | SKU 属性信息     | 如颜色、尺寸属性        |
#### 商品标识信息

官方还提供 `badge` 对象，其中包含五个字段。

| 返回参数                 | 类型     | 中文含义               | 说明         |
| -------------------- | ------ | ------------------ | ---------- |
| `badge.bestSeller`   | String | Best Seller 标识     | 是否有畅销商品标识  |
| `badge.amazonChoice` | String | Amazon's Choice 标识 | 是否具有该推荐标识  |
| `badge.newRelease`   | String | New Release 标识     | 是否有新品标识    |
| `badge.ebc`          | String | A+ 页面              | 是否具有 A+ 内容 |
| `badge.video`        | String | 商品视频               | 是否具有视频介绍   |

### 示例

```text
请仅调用一次卖家精灵 MCP 的 product_research，查询美国站最近 30 天的数据。

目标类目为 Home & Kitchen → Furniture → Dining Room Furniture → Chairs，节点路径为 1055398:1063306:3733781:3733821。类目参数使用 nodeIdPaths 数组，并启用类目精确匹配。

启用“只看该子类目排名”（filterSub 为 Y），筛选子类目排名 1–100，不设置大类 BSR 的数值范围。设置不含变体（variation 为 Y），按 BSR 升序排序，排序字段使用 bsr_rank，desc 为 false。
```

**目前这个接口不能直接保证得到“100 个互不重复父体的 Top100 产品”。** 根据这次实际返回。

## asin_coupon_trend（ASIN优惠趋势）

`asin_coupon_trend` 是卖家精灵 MCP 提供的**商品优惠券历史趋势查询接口**，主要用于查询指定 ASIN 在不同日期的 Coupon（优惠券）信息，包括商品原价、优惠金额、优惠类型以及优惠后的价格。

简单理解：**你想知道某款竞品过去有没有设置 Coupon、优惠了多少钱、优惠后的实际价格是多少，就可以使用这个接口。**

需要注意：**Coupon 优惠趋势不是完整的历史价格趋势。**

这个接口主要记录 Coupon 相关信息。如果你希望研究历史售价、BSR、评分等更多趋势，应考虑 `keepa_info`。

例如，一款餐椅长期标价 $129.99，但经常提供 $20 Coupon。

那么它的优惠后价格可能只有 $109.99。

### 请求参数

该接口只有2 个请求参数，均为必填。

| 参数            | 类型     | 必填  | 参数名称    | 参数描述                          |
| ------------- | ------ | --- | ------- | ----------------------------- |
| `marketplace` | String | 是   | 亚马逊站点   | 指定查询站点，例如 `US`                |
| `asin`        | String | 是   | 商品 ASIN | 指定需要查询优惠趋势的商品，例如 `B0DXTMS9NF` |

### 返回参数

| #   | 参数            | 类型     | 参数名称    | 参数描述                         |
| --- | ------------- | ------ | ------- | ---------------------------- |
| 1   | `marketplace` | String | 亚马逊站点   | 商品所属站点，例如 `US`               |
| 2   | `asin`        | String | 商品 ASIN | 当前查询的商品编号                    |
| 3   | `date`        | String | 日期      | 对应的优惠记录日期，例如 `2025-09-09`    |
| 4   | `type`        | String | 优惠类型    | `M`：固定金额减免；`P`：百分比折扣         |
| 5   | `asinPrice`   | Float  | 商品价格    | 该日期记录的 ASIN 商品价格             |
| 6   | `couponPrice` | Float  | 优惠金额    | Coupon 对应的优惠数值，需结合 `type` 理解 |
| 7   | `finalPrice`  | Float  | 优惠后价格   | 卖家精灵计算或记录的 Coupon 抵扣后价格      |

## asin_detail_with_coupon_trend（ASIN 详情及优惠趋势）

`asin_detail_with_coupon_trend` 是卖家精灵 MCP 提供的**商品详情与历史 Coupon 优惠数据组合查询接口**。

它相当于将之前介绍的两个接口合并：

- `asin_detail`：查询商品的基础信息。
- `asin_coupon_trend`：查询商品的历史 Coupon 优惠记录。

**核心价值：只需调用一个 MCP 接口，就可以同时获取商品详情和历史优惠券数据。**

### 请求参数

| #   | 参数            | 类型     | 必填  | 参数名称    | 参数描述                      |
| --- | ------------- | ------ | --- | ------- | ------------------------- |
| 1   | `marketplace` | String | 是   | 亚马逊站点   | 指定查询站点，例如 `US`            |
| 2   | `asin`        | String | 是   | 商品 ASIN | 指定需要查询的商品，例如 `B0DXTMS9NF` |
### 返回参数

官方返回结果包含两个主要对象：

| #   | 参数             | 类型     | 参数名称        | 参数描述                   |
| --- | -------------- | ------ | ----------- | ---------------------- |
| 1   | `asin`         | Object | 商品详情        | 包含商品基础信息、价格、BSR、评分、变体等 |
| 2   | `couponTrends` | List   | Coupon 优惠趋势 | 包含不同日期的历史优惠记录          |
**注意：这里顶层的 `asin` 是一个对象，而不是普通的 ASIN 字符串。**

真正的商品编号位于 `asin.asin`。

对于商品详情，与之前介绍的 `asin_detail` 高度一致，因此不再重复解释所有基础概念。

couponTrends 是历史 Coupon 优惠数据。

|#|参数|类型|参数名称|参数描述|
|---|---|---|---|---|
|1|`couponTrends[].marketplace`|String|亚马逊站点|例如 `US`|
|2|`couponTrends[].asin`|String|商品 ASIN|对应的商品编号|
|3|`couponTrends[].date`|String|日期|优惠记录对应的日期|
|4|`couponTrends[].type`|String|优惠类型|`M`：固定金额；`P`：百分比|
|5|`couponTrends[].asinPrice`|Float|商品价格|对应日期的商品价格|
|6|`couponTrends[].couponPrice`|Float|Coupon 优惠值|优惠金额或比例对应的数值|
|7|`couponTrends[].finalPrice`|Float|优惠后价格|Coupon 抵扣后的商品价格|

## asin_sales_trend（ASIN 销量趋势）

`asin_sales_trend` 是卖家精灵 MCP 提供的**商品历史销量趋势查询接口**，主要用于查询指定 ASIN 的父体、子体在不同月份的销量、销售额和价格变化。

简单理解：**你想知道某款餐椅过去几个月卖了多少件、销售额如何变化，以及哪个颜色变体贡献了更多销量，就可以使用这个接口。**

这个接口更适合研究**父体与子体的月度销售表现**。

### 请求参数

|#|参数|类型|必填|参数名称|参数描述|
|---|---|---|---|---|---|
|1|`marketplace`|String|是|亚马逊站点|指定查询的站点，例如 `US`|
|2|`asin`|String|是|商品 ASIN|指定查询销量趋势的商品，例如 `B0GYWDDJPD`|
### 返回参数

返回数据主要分为两个部分：

|返回参数|类型|参数名称|参数描述|
|---|---|---|---|
|`asin`|Object|商品详情|包含商品标题、品牌、售价、评分等基础信息|
|`salesTrendPoints`|List|销量趋势数据|包含各月份父体、子体的销量、销售额和价格|
asin 为商品详情，这部分与之前介绍的 `asin_detail` 基本一致，不再重复解释基础概念。

| #   | 返回参数                 | 类型      | 参数名称   | 参数描述                |
| --- | -------------------- | ------- | ------ | ------------------- |
| 1   | `month`              | String  | 月份     | 数据所属月份，例如 `2025-09` |
| 2   | `price`              | Float   | 商品价格   | 对应月份记录的商品售价         |
| 3   | `averagePrice`       | Float   | 平均价格   | 对应月份的平均售价           |
| 4   | `parentUnitSales`    | Integer | 父体月销量  | 整个父体的预估月销量          |
| 5   | `childUnitSales`     | Integer | 子体月销量  | 当前 ASIN 对应子体的预估月销量  |
| 6   | `parentSalesRevenue` | Float   | 父体月销售额 | 整个父体的预估销售金额         |
| 7   | `childSalesRevenue`  | Float   | 子体月销售额 | 当前子体的预估销售金额         |

**`salesTrendPoints` 是这个接口最重要的返回字段**。
## asin_prediction（ASIN销量预测）

`asin_prediction` 是卖家精灵 MCP 提供的**ASIN 销量预测接口**。输入一个亚马逊商品的 ASIN，就可以获取该商品的日销量、月销量、销售额、价格以及 BSR 排名等估算数据。

需要特别注意：虽然接口名称包含 Prediction（预测），但官方返回示例中也包含**历史日期的销量估算数据**，不能简单理解为预测未来销量。

### 请求参数

|参数|类型|必填|作用|示例|
|---|---|---|---|---|
|`marketplace`|String|是|指定亚马逊站点|`US`|
|`asin`|String|是|指定查询的商品 ASIN|`B07Z82895W`|

### 返回参数

`asin_prediction` 的返回结果主要由三部分组成：

| 返回字段            | 类型     | 含义       |
| --------------- | ------ | -------- |
| `asinDetail`    | Object | 商品基本信息   |
| `dailyItemList` | List   | 每日销量预测明细 |
| `monthItemList` | List   | 每月销量预测明细 |

接下来分别介绍。

#### asinDetail：商品基本信息

| 返回参数            | 类型      | 中文含义    | 说明         |
| --------------- | ------- | ------- | ---------- |
| `asin`          | String  | 商品 ASIN | 商品标识       |
| `title`         | String  | 商品标题    | Listing 标题 |
| `brand`         | String  | 商品品牌    | 商品所属品牌     |
| `availableDate` | Long    | 上架日期    | 商品的上架时间    |
| `category`      | String  | 类目名称    | 商品所属类目     |
| `categoryId`    | String  | 类目 ID   | 类目节点标识     |
| `imageUrl`      | String  | 商品图片    | 图片 URL     |
| `ratings`       | Integer | 评分数量    | 商品累计评分数    |
| `rating`        | Float   | 星级评分    | 例如 4.6 分   |
#### dailyItemList：每日销量预测明细

| 返回参数     | 类型      | 中文含义     | 示例           |
| -------- | ------- | -------- | ------------ |
| `date`   | String  | 日期       | `2025-07-01` |
| `bsr`    | Integer | BSR 排名   | `137656`     |
| `sales`  | Integer | 日销量（估算）  | `9`          |
| `amount` | Float   | 日销售额（估算） | `126`        |
| `price`  | Float   | 商品单价     | `14`         |
#### monthItemList：每月销量预测明细

| 返回参数     | 类型      | 中文含义     | 示例        |
| -------- | ------- | -------- | --------- |
| `date`   | String  | 月份       | `2026-01` |
| `sales`  | Integer | 月销量（估算）  | `14`      |
| `amount` | Float   | 月销售额（估算） | `200`     |
| `price`  | Float   | 商品单价     | `20`      |

## bsr_prediction（BSR销量预测）

`bsr_prediction` 是卖家精灵 MCP 提供的**根据亚马逊大类 BSR 排名估算商品销量的接口**。

简单理解：**你只需要知道商品所属的亚马逊大类及其 BSR 排名，就可以估算该排名对应的日销量和近 30 天销量，不需要提供 ASIN。**

### 请求参数

| #   | 参数            | 类型      | 必填  | 参数名称      | 参数描述                                      |
| --- | ------------- | ------- | --- | --------- | ----------------------------------------- |
| 1   | `marketplace` | String  | 是   | 亚马逊站点     | 指定查询站点，例如 `US`                            |
| 2   | `bsr`         | Integer | 是   | 大类 BSR 排名 | 输入商品在所属大类中的排名，例如 `1000`                   |
| 3   | `categoryId`  | String  | 是   | 一级类目节点 ID | 指定 BSR 所属的一级类目，例如 `11260432011`，需要查产品类目获取 |

注意，`categoryId` 要求的是单个节点 ID，而不是用冒号连接的完整 `nodeIdPath`。实际使用中，可以先通过 `product_node` 查找对应的一级类目节点 ID。

### 返回参数

该接口返回的字段比较少，主要包括销量估算结果及附近 BSR 排名的销量估算明细。


## keepa_info（商品历史趋势）

`keepa_info` 是卖家精灵 MCP 提供的**商品历史数据查询接口**，主要用于查询指定 ASIN 上架以来的价格、BSR 排名、评分、评分数、卖家数量等指标的历史变化。

`asin_detail` 让你了解商品当前是什么情况，而 `keepa_info` 让你了解这个商品过去发生了什么变化。

例如，你正在研究一款美国站吧椅，想知道：

- 过去 6 个月有没有降价？
- 什么时候出现过 Deal 优惠？
- 大类和小类 BSR 排名是否持续提升？
- 评分数增长是否明显？
- 商品是否从一个卖家变成多个卖家？

这些问题都可以通过 `keepa_info` 的历史记录辅助分析。

### 请求参数

**5 个请求参数，其中 2 个必填、3 个选填**。

| #   | 参数               | 类型      | 必填  | 参数名称    | 参数描述           |
| --- | ---------------- | ------- | --- | ------- | -------------- |
| 1   | `marketplace`    | String  | 是   | 亚马逊站点   | 指定查询站点，例如 `US` |
| 2   | `asin`           | String  | 是   | 商品 ASIN | 指定需要查询历史趋势的商品  |
| 3   | `startTimestamp` | Long    | 否   | 开始时间戳   | 指定历史数据的起始时间    |
| 4   | `endTimestamp`   | Long    | 否   | 结束时间戳   | 指定历史数据的结束时间    |
| 5   | `dailyLatest`    | Boolean | 否   | 每日最新数据  | 是否只返回每天最新的一条记录 |
startTimestamp 与 endTimestamp 用于控制 需要查询的历史时间范围。

例如：

你想了解某款餐椅从 2026 年 7 月 1 日到 9 月 30 日的价格变化。

可以让 AI 将这两个日期转换为对应的 Unix 时间戳，分别传给：

- `startTimestamp`
- `endTimestamp`

dailyLatest：只保留每天最新的数据。这个参数非常实用。假设某款吧椅一天之内的价格多次变化，如果`dailyLatest = false`，通常表示不启用「每天只保留最新记录」的限制，可能返回一天中的多条历史数据。如果`dailyLatest = true`，则请求只保留每天最新的记录。

### 返回参数

**42 个顶层返回字段**。为了避免混淆，我将它们分成四组。

#### 商品及类目信息

| #   | 参数                          | 类型     | 参数名称       | 参数描述              |
| --- | --------------------------- | ------ | ---------- | ----------------- |
| 1   | `marketplace`               | String | 亚马逊站点      | 商品所属站点            |
| 2   | `asin`                      | String | 查询 ASIN    | 请求查询的 ASIN        |
| 3   | `dataAsin`                  | String | 实际数据 ASIN  | 实际返回历史数据的 ASIN    |
| 4   | `parentAsin`                | String | 父体 ASIN    | 商品所属父体            |
| 5   | `variationAsins`            | List   | 变体 ASIN 列表 | 商品相关变体            |
| 6   | `rootCategory`              | String | 大类节点 ID    | 商品 BSR 大类节点       |
| 7   | `rootCategoryLabel`         | String | 大类名称       | 例如 Home & Kitchen |
| 8   | `salesRankReference`        | String | 排名类目节点 ID  | 商品 BSR 对应的排名节点    |
| 9   | `salesRankReferenceHistory` | List   | 排名节点变化历史   | 记录 BSR 所属排名节点的变化  |
| 10  | `nodeIdPath`                | String | 商品类目路径     | 完整类目 ID 路径        |
| 11  | `nodeLabelPath`             | String | 类目名称路径     | 完整英文类目路径          |
| 12  | `productStatus`             | String | 商品状态       | 标识商品数据是否可访问       |
| 13  | `availabilityAmazon`        | String | 亚马逊销售状态    | 与亚马逊自身销售该商品的状态相关  |

#### 商品基础信息与物流

| #   | 参数                  | 类型      | 参数名称     | 参数描述               |
| --- | ------------------- | ------- | -------- | ------------------ |
| 14  | `title`             | String  | 商品标题     | Listing 标题         |
| 15  | `brand`             | String  | 品牌       | 商品所属品牌             |
| 16  | `asinUrl`           | String  | 商品链接     | Amazon Listing URL |
| 17  | `brandUrl`          | String  | 品牌链接     | 品牌相关页面             |
| 18  | `salesRankUrl`      | String  | BSR 榜单链接 | 对应的类目排名页面          |
| 19  | `imageUrl`          | String  | 商品缩略图    | 约 200×200 的图片      |
| 20  | `zoomImageUrl`      | String  | 商品大图     | 约 600×600 的图片      |
| 21  | `imageUrls`         | List    | 商品图片列表   | 多张商品图片             |
| 22  | `dimensions`        | String  | 商品尺寸     | 商品净尺寸              |
| 23  | `weight`            | String  | 商品重量     | 商品净重量              |
| 24  | `weightGram`        | Integer | 商品净重     | 单位为克               |
| 25  | `pkgDimensions`     | String  | 包装尺寸     | 商品包装长宽高            |
| 26  | `pkgDimensionsSize` | List    | 包装尺寸数值   | 长、宽、高，单位为厘米        |
| 27  | `pkgWeight`         | String  | 包装重量     | 商品打包重量             |
| 28  | `pkgWeightGram`     | Integer | 包装重量数值   | 单位为克               |
| 29  | `fbaFees`           | Float   | FBA 总费用  | 接口记录的 FBA 费用       |
| 30  | `fbaItems`          | String  | FBA 费用明细 | JSON 字符串形式的费用构成    |
| 31  | `numberOfPages`     | Integer | 页面页码     | 商品所在页面信息           |
| 32  | `numberOfItems`     | Integer | 页面位置     | 商品所在位置             |

#### 价格历史趋势

这是该接口最重要的一组数据。

| #   | 参数                      | 类型   | 参数名称         | 参数描述             |
| --- | ----------------------- | ---- | ------------ | ---------------- |
| 33  | `price`                 | List | 价格趋势         | 历史商品价格记录         |
| 34  | `dealPrice`             | List | Deal / 成交价趋势 | 历史 Deal 相关价格记录   |
| 35  | `buyBox`                | List | Buy Box 价格趋势 | 历史黄金购物车价格        |
| 36  | `priceList`             | List | 划线价格趋势       | 历史参考标价           |
| 37  | `buyBoxSellerIdHistory` | List | Buy Box 卖家变化 | 历史 Buy Box 卖家 ID |
price、dealPrice、buyBox、priceList 的区别

| 字段          | 主要表示          | 应该怎样理解            |
| ----------- | ------------- | ----------------- |
| `price`     | 商品价格历史        | 商品在各个采集时间点记录的售价   |
| `dealPrice` | Deal 价格历史     | 商品在部分促销活动中的优惠价格记录 |
| `buyBox`    | Buy Box 价格历史  | 获得主要购买入口的报价变化     |
| `priceList` | List Price 历史 | 商品展示的参考标价或划线价格    |
#### BSR、评分和卖家数量趋势

| #   | 参数             | 类型   | 参数名称      | 参数描述          |
| --- | -------------- | ---- | --------- | ------------- |
| 38  | `bsr`          | List | 大类 BSR 历史 | 商品大类畅销排名的历史变化 |
| 39  | `subSalesRank` | List | 小类 BSR 历史 | 各子类目中的历史排名    |
| 40  | `reviews`      | List | 评分数历史     | 累计评分数量的历史变化   |
| 41  | `rating`       | List | 评分值历史     | 商品平均星级的历史变化   |
| 42  | `sellers`      | List | 卖家数量历史    | 销售该商品的卖家数量变化  |

# 二、关键词研究

核心目标：了解消费者搜索什么，以及哪些关键词值得研究。

| 序号  | MCP Code                  | 中文名称   | 核心作用                 |
| --- | ------------------------- | ------ | -------------------- |
| 12  | `keyword_research`        | 关键词选品  | 根据搜索量、购买率等指标寻找关键词机会  |
| 13  | `keyword_research_trends` | 关键词趋势  | 查询关键词的历史搜索趋势         |
| 14  | `keyword_miner`           | 关键词挖掘  | 挖掘相关词、衍生词和长尾关键词      |
| 15  | `keyword_conversion`      | 关键词转化率 | 分析关键词转化表现            |
| 16  | `keyword_order`           | 出单词反查  | 反查竞品的主要出单关键词         |
| 17  | `google_trend`            | 谷歌趋势   | 查询关键词在 Google 上的搜索趋势 |

## keyword_research（关键词选品）

`keyword_research`是卖家精灵 MCP 提供的关键词选品接口，主要用于通过亚马逊买家的搜索行为，分析关键词对应的细分市场需求、增长趋势和竞争情况，从而发现潜在的选品机会。

它的核心逻辑：

一个关键词可以代表一个潜在的细分市场，通过分析关键词数据，判断这个市场是否值得进入。

例如，在美国站家具类目中：

- `dining chairs`：餐椅市场
- `upholstered dining chairs`：软包餐椅细分市场
- `swivel dining chairs`：旋转餐椅细分市场
- `bar stools`：吧椅市场
- `adjustable bar stools`：可调节高度吧椅细分市场

通过该接口，可以了解这些关键词对应市场的搜索需求、购买情况、竞争程度以及增长趋势。

### 请求参数

| 参数                     | 类型      | 必填  | 参数名称        | 参数描述                              |
| ---------------------- | ------- | --- | ----------- | --------------------------------- |
| `marketplace`          | String  | 是   | 站点          | 亚马逊站点编码，例如 `US`                   |
| `month`                | String  | 否   | 查询月份        | `yyyyMM` 格式，例如 `202609`；支持近 24 个月 |
| `departments`          | List    | 否   | 商品类目        | 使用关键词选品类目接口返回的 `code`             |
| `keywords`             | String  | 否   | 包含关键词       | 根据指定关键词筛选，例如 `dining chairs`      |
| `excludeKeywords`      | String  | 否   | 排除关键词       | 排除包含指定词的结果                        |
| `minSearches`          | Integer | 否   | 最小月搜索量      | 例如 `10000`                        |
| `maxSearches`          | Integer | 否   | 最大月搜索量      | 例如 `50000`                        |
| `minSearchesCr`        | Float   | 否   | 最小月搜索量增长率   | 例如 `10`，表示 10%                    |
| `maxSearchesCr`        | Float   | 否   | 最大月搜索量增长率   | 例如 `50`，表示 50%                    |
| `minProducts`          | Integer | 否   | 最小商品数       | 对应关键词下的最小相关商品数量                   |
| `maxProducts`          | Integer | 否   | 最大商品数       | 对应关键词下的最大相关商品数量                   |
| `minPurchases`         | Integer | 否   | 最小月购买量      | 例如 `300`                          |
| `maxPurchases`         | Integer | 否   | 最大月购买量      | 例如 `2000`                         |
| `minPurchaseRate`      | Float   | 否   | 最小月购买率      | 例如 `3.2`，表示 3.2%                  |
| `maxPurchaseRate`      | Float   | 否   | 最大月购买率      | 例如 `10.5`，表示 10.5%                |
| `withYearlyGrowth`     | Boolean | 否   | 新细分市场       | 筛选符合新细分市场定义的关键词                   |
| `minSearchMonthCv`     | Integer | 否   | 最小同比增长值     | 月搜索量同比增长数量下限                      |
| `maxSearchMonthCv`     | Integer | 否   | 最大同比增长值     | 月搜索量同比增长数量上限                      |
| `minSearchMonthCr`     | Float   | 否   | 最小同比增长率     | 月搜索量同比增长率下限                       |
| `maxSearchMonthCr`     | Float   | 否   | 最大同比增长率     | 月搜索量同比增长率上限                       |
| `minSearchNearlyCv`    | Integer | 否   | 最小近 3 个月增长值 | 近 3 个月搜索量增长数量下限                   |
| `maxSearchNearlyCv`    | Integer | 否   | 最大近 3 个月增长值 | 近 3 个月搜索量增长数量上限                   |
| `minSearchNearlyCr`    | Float   | 否   | 最小近 3 个月增长率 | 例如 `10`，表示 10%                    |
| `maxSearchNearlyCr`    | Float   | 否   | 最大近 3 个月增长率 | 例如 `30`，表示 30%                    |
| `marketPeriod`         | String  | 否   | 市场周期        | 例如 `N`、`I`、`D`、`S1,S2,S3`         |
| `minAvgPrice`          | Float   | 否   | 最低平均价格      | 例如 `50`，美国站单位为美元                  |
| `maxAvgPrice`          | Float   | 否   | 最高平均价格      | 例如 `150`                          |
| `minRatings`           | Integer | 否   | 最小平均评分数     | 对应关键词市场的平均评分数量下限                  |
| `maxRatings`           | Integer | 否   | 最大平均评分数     | 对应关键词市场的平均评分数量上限                  |
| `minRating`            | Float   | 否   | 最小平均评分值     | 例如 `3.5`                          |
| `maxRating`            | Float   | 否   | 最大平均评分值     | 例如 `4.5`                          |
| `minBid`               | Float   | 否   | 最低 PPC 竞价   | 广告建议竞价下限                          |
| `maxBid`               | Float   | 否   | 最高 PPC 竞价   | 广告建议竞价上限                          |
| `minAraClickRate`      | Float   | 否   | 最小点击集中度     | 例如 `20`，表示 20%                    |
| `maxAraClickRate`      | Float   | 否   | 最大点击集中度     | 例如 `50`，表示 50%                    |
| `minGoodsValue`        | Float   | 否   | 最小货流值       | 货流值下限，按百分比设置                      |
| `maxGoodsValue`        | Float   | 否   | 最大货流值       | 货流值上限，按百分比设置                      |
| `minSupplyDemandRatio` | Float   | 否   | 最小供需比       | 关键词搜索需求与相关商品数量的比值下限               |
| `maxSupplyDemandRatio` | Float   | 否   | 最大供需比       | 关键词搜索需求与相关商品数量的比值上限               |
| `minWordCount`         | Integer | 否   | 最小单词数       | 关键词包含的最少单词数量                      |
| `maxWordCount`         | Integer | 否   | 最大单词数       | 关键词包含的最多单词数量                      |
| `page`                 | Integer | 否   | 页码          | 从 `1` 开始，默认 `1`                   |
| `size`                 | Integer | 否   | 每页数量        | 默认 `15`，最大 `15`                   |
| `order`                | Object  | 否   | 排序配置        | 包含排序字段和排序方向                       |
| `└field`               | String  | 否   | 排序字段        | 取值参见下表                            |
| `└desc`                | Boolean | 否   | 排序方向        | `true` 降序，`false` 升序，默认降序         |

### 返回参数

`keyword_research` 的返回结果以关键词为单位。

通常一条 `items` 记录对应一个关键词市场，而不是一个商品 ASIN。

#### 返回数据整体结构

|参数|类型|参数名称|参数描述|
|---|---|---|---|
|`code`|String|响应状态|示例为 `OK`|
|`message`|String|响应消息|例如“成功”|
|`data`|Object|数据主体|包含分页信息与关键词列表|
|`└pages`|Integer|总页数|符合条件的结果共多少页|
|`└page`|Integer|当前页|当前返回的页码|
|`└size`|Integer|每页数量|当前设置的分页大小|
|`└total`|Integer|总记录数|符合筛选条件的关键词记录总数|
|`└took`|Integer|处理耗时|官方示例返回数值，未注明时间单位|
|`└order`|Object|排序信息|包含 `field`、`desc`|
|`└items`|List|关键词列表|每个元素代表一条关键词数据|

#### 关键词数据完整字段

以下字段位于 `data.items[]` 内。

| #   | 参数                     | 类型      | 参数名称         | 参数描述                             |
| --- | ---------------------- | ------- | ------------ | -------------------------------- |
| 1   | `marketplace`          | String  | 站点           | 例如 `US`                          |
| 2   | `keywords`             | String  | 关键词          | 例如 `dining chairs`               |
| 3   | `searches`             | Integer | 月搜索量         | 关键词对应的搜索次数                       |
| 4   | `clicks`               | Integer | 点击量          | 该关键词搜索结果页产生的总点击次数，并非某个 ASIN 的点击量 |
| 5   | `impressions`          | Long    | 展示量          | 该关键词搜索结果页中所有 ASIN 的总展示次数         |
| 6   | `purchases`            | Integer | 月购买量         | 搜索该关键词后产生购买的次数                   |
| 7   | `growth`               | Float   | 增长率          | 关键词搜索量增长指标                       |
| 8   | `purchaseRate`         | Float   | 月购买率         | 月购买量与月搜索量的比值                     |
| 9   | `products`             | Integer | 商品数          | 该关键词对应的相关商品数量                    |
| 10  | `supplyDemandRatio`    | Float   | 供需比          | 搜索量与商品数的比值                       |
| 11  | `searchDepartments`    | List    | 关联类目         | 关键词关联的商品类目信息                     |
| 12  | `└code`                | String  | 类目代码         | 例如 `electronics`                 |
| 13  | `└label`               | String  | 类目名称         | 例如 `Electronics`                 |
| 14  | `└total`               | Integer | 类目总计         | 官方未明确给出完整统计定义                    |
| 15  | `└ratio`               | Float   | 类目占比         | 该关联类目的占比                         |
| 16  | `month`                | String  | 查询月份         | 例如 `2025.07`                     |
| 17  | `supplement`           | String  | 补充关键词标记      | 示例为 `N`                          |
| 18  | `searchMonthlyCv`      | Integer | 搜索量同比增长值     | 与上一年同期相比的搜索量变化值                  |
| 19  | `searchMonthlyCr`      | Float   | 搜索量同比增长率     | 同比搜索量变化百分比                       |
| 20  | `searchNearlyCv`       | Integer | 近 3 个月增长值    | 近 3 个月搜索量的增长值                    |
| 21  | `searchNearlyCr`       | Float   | 近 3 个月增长率    | 近 3 个月搜索量增长百分比                   |
| 22  | `currency`             | String  | 货币符号         | 美国站为 `$`                         |
| 23  | `avgPrice`             | Float   | 平均价格         | 对应关键词市场的商品均价                     |
| 24  | `avgRatings`           | Integer | 平均评分数        | 对应关键词市场的商品平均评分数量                 |
| 25  | `avgRating`            | Float   | 平均评分值        | 例如 `4.5`，表示平均星级                  |
| 26  | `relationAsinList`     | List    | 关联 ASIN 列表   | 与该关键词关联的商品                       |
| 27  | `└price`               | Float   | 商品价格         | 关联 ASIN 的价格                      |
| 28  | `└ratings`             | Integer | 评分数          | 关联 ASIN 的评分数量                    |
| 29  | `└rating`              | Float   | 评分值          | 关联 ASIN 的星级评分                    |
| 30  | `bidMin`               | Float   | 最低建议竞价       | PPC 建议竞价区间下限                     |
| 31  | `bidMax`               | Float   | 最高建议竞价       | PPC 建议竞价区间上限                     |
| 32  | `bid`                  | Float   | PPC 建议竞价     | 关键词广告建议竞价                        |
| 33  | `araClickRate`         | Float   | 点击集中度        | 点击量排名前三的 ASIN 点击份额总和             |
| 34  | `araShareRate`         | Float   | 前三 ASIN 转化份额 | 前三 ASIN 的转化共享总占比                 |
| 35  | `araAsinList`          | List    | 点击前三 ASIN    | 该关键词下点击份额排名前三的商品                 |
| 36  | `└asin`                | String  | ASIN         | 商品标识                             |
| 37  | `└title`               | String  | 商品标题         | 该 ASIN 的 Listing 标题              |
| 38  | `└imageUrl`            | String  | 商品图片         | 商品图片链接                           |
| 39  | `└clickRate`           | Double  | 点击份额         | 单个 ASIN 在该关键词下的点击占比              |
| 40  | `└conversionShareRate` | Double  | 转化共享         | 单个 ASIN 在该关键词下的购买份额              |
| 41  | `goodsValue`           | Float   | 货流值          | PPC 竞价与市场商品均价的比值                 |
| 42  | `brands`               | List    | TOP3 品牌      | 关键词关联的前三品牌                       |
| 43  | `categories`           | List    | TOP3 类目      | 关键词关联的前三类目                       |
| 44  | `titleDensityExact`    | String  | 标题密度         | 搜索首页标题包含该关键词的自然搜索商品数量            |
| 45  | `marketPeriod`         | String  | 市场周期         | 例如 `N`、`S9,S10`                  |
| 46  | `brand`                | String  | 品牌           | 官方示例为 `Fujifilm`                 |
| 47  | `hasBrandWord`         | Boolean | 是否包含品牌词      | `true` 或 `false`                 |
| 48  | `keywordCn`            | String  | 中文翻译         | 关键词对应的中文翻译                       |

## keyword_research_trends（关键词选品趋势数据）

`keyword_research_trends`是卖家精灵 MCP 提供的关键词历史趋势查询接口，用于查询指定关键词在不同月份的搜索量、购买量、购买率以及增长率等数据。

它的核心作用：

输入一个关键词，查看这个关键词过去每个月的市场需求变化。

例如，你想研究美国站的 `dining chairs`（餐椅），就可以通过这个接口了解：

- 过去每个月有多少人次搜索 `dining chairs`？
- 每个月产生了多少次购买？
- 哪些月份搜索需求较高？
- 搜索需求同比、环比增长了多少？
- 这个关键词的市场需求是持续增长、下降，还是存在明显季节性？

### 请求参数

|#|参数|参数类型|是否必填|参数名称|参数描述|
|---|---|---|---|---|---|
|1|`marketplace`|String|是|站点|指定亚马逊站点，例如 `US` 为美国站|
|2|`keyword`|String|是|关键词|要查询历史趋势的指定关键词，例如 `dining chairs`|

### 返回参数

#### 整体响应结构

该接口返回的 `data` 是一个数组，**数组中每条记录对应一个月份的关键词数据**。

|参数|参数类型|参数名称|参数描述|
|---|---|---|---|
|`code`|String|状态码|`OK` 表示请求成功|
|`message`|String|响应消息|例如“成功”|
|`data`|Array|历史趋势数据|包含该关键词多个历史月份的数据记录|
#### 每个月的返回字段

| #   | 参数                 | 参数类型       | 参数名称   | 参数描述                       |
| --- | ------------------ | ---------- | ------ | -------------------------- |
| 1   | `time`             | String     | 时间     | 数据对应的月份，例如 `2026年03月`      |
| 2   | `keywrod`          | String     | 关键词    | 被查询的关键词，例如 `dining chairs` |
| 3   | `keywrodCn`        | String     | 关键词中文  | 关键词的中文翻译，例如“餐椅”            |
| 4   | `keywrodJp`        | String     | 关键词日文  | 关键词的日文翻译                   |
| 5   | `search`           | Integer    | 搜索量    | 该关键词在对应月份的搜索次数             |
| 6   | `purchase`         | BigDecimal | 购买量    | 该关键词在对应月份产生的购买次数           |
| 7   | `purchaseRate`     | BigDecimal | 购买率    | 当月购买次数相对于搜索次数的比例           |
| 8   | `yearlyGrowth`     | BigDecimal | 同比增长率  | 当月搜索量相对于去年同月的增长率           |
| 9   | `chainGrowth`      | BigDecimal | 环比增长率  | 当月搜索量相对于上月的增长率             |
| 10  | `threeMonthGrowth` | BigDecimal | 三个月增长率 | 官方未完整说明具体计算基期和方法           |
## keyword_miner（关键词挖掘）

`keyword_miner`是卖家精灵 MCP 提供的关键词挖掘接口，用于根据一个核心关键词，挖掘与其相关的衍生词、长尾关键词，并查询每个关键词的搜索量、购买量、竞争程度等数据。

它的核心作用：

输入一个核心关键词，找到更多相关关键词，为 Listing 优化、PPC 广告投放和关键词市场分析提供数据。

### 请求参数

| #   | 参数                     | 类型      | 必填  | 参数名称                | 参数描述                          |
| --- | ---------------------- | ------- | --- | ------------------- | ----------------------------- |
| 1   | `marketplace`          | String  | 是   | 站点                  | 亚马逊站点，例如 `US`                 |
| 2   | `historyDate`          | String  | 否   | 历史日期                | `yyyyMM` 格式；不传或传空字符串表示最近 30 天 |
| 3   | `keyword`              | String  | 是   | 核心关键词               | 用于挖掘的种子词，例如 `dining chairs`   |
| 4   | `keywordList`          | List    | 否   | 批量查询关键词             | 关键词列表，例如 `["dining chairs"]`  |
| 5   | `minSearch`            | Integer | 否   | 最小搜索量               | 搜索量下限                         |
| 6   | `maxSearch`            | Integer | 否   | 最大搜索量               | 搜索量上限                         |
| 7   | `minPurchases`         | Integer | 否   | 最小购买量               | 月购买量下限                        |
| 8   | `maxPurchases`         | Integer | 否   | 最大购买量               | 月购买量上限                        |
| 9   | `minPurchasesRate`     | Float   | 否   | 最小购买率               | 例如 `5` 表示 5%                  |
| 10  | `maxPurchasesRate`     | Float   | 否   | 最大购买率               | 购买率上限                         |
| 11  | `minSPR`               | Integer | 否   | 最小 SPR              | SPR 下限                        |
| 12  | `maxSPR`               | Integer | 否   | 最大 SPR              | SPR 上限                        |
| 13  | `minTitleDensity`      | Integer | 否   | 最小标题密度              | 标题密度下限                        |
| 14  | `maxTitleDensity`      | Integer | 否   | 最大标题密度              | 标题密度上限                        |
| 15  | `minRelevancy`         | Float   | 否   | 最小相关度               | 最小为 0                         |
| 16  | `maxRelevancy`         | Float   | 否   | 最大相关度               | 最大为 100                       |
| 17  | `minSearchRank`        | Integer | 否   | 最小搜索排名              | ABA 搜索频率排名下限                  |
| 18  | `maxSearchRank`        | Integer | 否   | 最大搜索排名              | ABA 搜索频率排名上限                  |
| 19  | `minProducts`          | Integer | 否   | 最小商品数               | 相关商品数量下限                      |
| 20  | `maxProducts`          | Integer | 否   | 最大商品数               | 相关商品数量上限                      |
| 21  | `minSupplyDemandRatio` | Float   | 否   | 最小供需比               | 供需比下限                         |
| 22  | `maxSupplyDemandRatio` | Float   | 否   | 最大供需比               | 供需比上限                         |
| 23  | `minAdProducts`        | Integer | 否   | 最小广告竞品数             | 广告竞品数量下限                      |
| 24  | `maxAdProducts`        | Integer | 否   | 最大广告竞品数             | 广告竞品数量上限                      |
| 25  | `minWordCount`         | Integer | 否   | 最小单词数               | 关键词的最少单词数量                    |
| 26  | `maxWordCount`         | Integer | 否   | 最大单词数               | 关键词的最多单词数量                    |
| 27  | `minMonopolyClickRate` | Float   | 否   | 最小点击集中度             | 例如 `20` 表示 20%                |
| 28  | `maxMonopolyClickRate` | Float   | 否   | 最大点击集中度             | 点击集中度上限                       |
| 29  | `minBid`               | Float   | 否   | 最低 PPC 竞价           | 广告建议竞价下限                      |
| 30  | `maxBid`               | Float   | 否   | 最高 PPC 竞价           | 广告建议竞价上限                      |
| 31  | `minPrice`             | Float   | 否   | 最低平均价格              | 商品均价下限                        |
| 32  | `maxPrice`             | Float   | 否   | 最高平均价格              | 商品均价上限                        |
| 33  | `minRatings`           | Integer | 否   | 最小平均评分数             | 平均评分数量下限                      |
| 34  | `maxRatings`           | Integer | 否   | 最大平均评分数             | 平均评分数量上限                      |
| 35  | `minRating`            | Float   | 否   | 最小平均评分值             | 星级评分下限                        |
| 36  | `maxRating`            | Float   | 否   | 最大平均评分值             | 星级评分上限                        |
| 37  | `amazonChoice`         | Boolean | 否   | Amazon's Choice 推荐词 | `true` 表示仅筛选 AC 推荐词           |
| 38  | `filterRootWord`       | Integer | 否   | 词根过滤                | `0` 包含所有，`1` 只包含词根            |
| 39  | `matchType`            | Integer | 否   | 匹配方式                | `2` 广泛匹配，`3` 词组匹配             |
| 40  | `includeKeywords`      | List    | 否   | 包含关键词               | 进一步筛选包含指定词的结果                 |
| 41  | `excludeKeywords`      | List    | 否   | 排除关键词               | 排除包含指定词的结果                    |
| 42  | `page`                 | Integer | 否   | 页码                  | 默认 `1`                        |
| 43  | `size`                 | Integer | 否   | 每页数量                | 默认 `50`，最大 `100`              |
| 44  | `order`                | Object  | 否   | 排序配置                | 包含排序字段和方向                     |
| 45  | `└field`               | String  | 否   | 排序字段                | 官方排序字段说明存在问题，详见下文             |
| 46  | `└desc`                | Boolean | 否   | 排序方向                | `true` 降序，`false` 升序，默认降序     |

`keyword`是最重要的参数，例如希望挖掘美国站餐椅相关关键词，只需要填写：

| 参数            | 值               |
| ------------- | --------------- |
| `marketplace` | `US`            |
| `keyword`     | `dining chairs` |
| `page`        | `1`             |
| `size`        | `10`            |

从 `dining chairs` 出发，挖掘与其关联的关键词，返回第一页，最多 10 条。

`filterRootWord`这个参数用于决定是否只挖掘包含词根的关键词。

| 参数值 | 模式        | 作用            |
| --- | --------- | ------------- |
| `0` | 不限制必须包含词根 | 可以返回关联词及长尾词   |
| `1` | 仅包含词根     | 只保留包含输入词根的关键词 |
`matchType`模式需要结合`includeKeywords`，支持多个关键词或词组输入查询，多词用英文逗号隔开。


### 返回参数

`keyword_miner`返回的是关键词列表，不是商品列表。

整体结构如下：

| 参数        | 类型      | 参数名称  | 参数描述          |
| --------- | ------- | ----- | ------------- |
| `code`    | String  | 状态码   | `OK` 表示请求成功   |
| `message` | String  | 响应消息  | 例如“成功”        |
| `data`    | Object  | 数据主体  | 包含分页信息和关键词列表  |
| `└pages`  | Integer | 总页数   | 符合条件的关键词共有多少页 |
| `└page`   | Integer | 当前页码  | 当前返回的页码       |
| `└size`   | Integer | 每页数量  | 每页最多返回多少条关键词  |
| `└total`  | Integer | 总记录数  | 符合条件的关键词总数    |
| `└took`   | Integer | 处理耗时  | 官方未明确说明时间单位   |
| `└order`  | Object  | 排序信息  | 包含排序字段和方向     |
| `└items`  | List    | 关键词列表 | 每个元素对应一条关键词记录 |

关键词返回参数完整表格如下：

| #   | 参数                  | 类型      | 参数名称            | 参数描述                  |
| --- | ------------------- | ------- | --------------- | --------------------- |
| 1   | `marketplace`       | String  | 站点              | 例如 `US`               |
| 2   | `keyword`           | String  | 关键词             | 挖掘出的关键词               |
| 3   | `keywordCn`         | String  | 中文翻译            | 关键词对应的中文翻译            |
| 4   | `keywordJp`         | String  | 日文翻译            | 关键词对应的日文翻译            |
| 5   | `departments`       | List    | 关联类目            | 关键词关联的商品类目            |
| 6   | `└code`             | String  | 类目编码            | 例如 `electronics`      |
| 7   | `└label`            | String  | 类目名称            | 例如 `Electronics`      |
| 8   | `month`             | String  | 搜索月份            | 例如 `2025.07`          |
| 9   | `supplement`        | String  | 补充关键词标记         | 是否为无当前月搜索量的补充词        |
| 10  | `searches`          | Integer | 月搜索量            | 关键词当月的搜索次数            |
| 11  | `purchases`         | Integer | 月购买量            | 搜索该关键词后产生的购买次数        |
| 12  | `purchaseRate`      | Float   | 月购买率            | 月购买量与月搜索量的比值          |
| 13  | `monopolyClickRate` | Float   | 点击集中度           | 点击排名前三的 ASIN 点击份额总和   |
| 14  | `products`          | Integer | 商品数             | 关键词对应的相关商品数量          |
| 15  | `adProducts`        | Integer | 广告竞品数           | 与该关键词相关的广告商品数量        |
| 16  | `supplyDemandRatio` | Float   | 供需比             | 月搜索量与相关商品数的比值         |
| 17  | `avgPrice`          | Float   | 平均价格            | 关键词相关商品的平均价格          |
| 18  | `avgRatings`        | Integer | 平均评分数           | 关键词相关商品的平均评分数量        |
| 19  | `avgRating`         | Float   | 平均评分值           | 关键词相关商品的平均星级          |
| 20  | `bidMin`            | Float   | 最低 PPC 竞价       | 广告建议竞价区间下限            |
| 21  | `bidMax`            | Float   | 最高 PPC 竞价       | 广告建议竞价区间上限            |
| 22  | `bid`               | Float   | PPC 竞价          | 建议竞价                  |
| 23  | `cvsShareRate`      | Float   | 转化共享率           | 点击前三 ASIN 的转化共享总占比    |
| 24  | `wordCount`         | Integer | 单词数             | 关键词包含的单词数量            |
| 25  | `titleDensity`      | Integer | 标题密度            | 搜索结果首页标题包含该关键词的商品数    |
| 26  | `spr`               | Integer | SPR             | 关键词排名进入并维持搜索首页的预估单量指标 |
| 27  | `relevancy`         | Double  | 相关度             | 挖掘出的关键词与查询关键词的相关程度    |
| 28  | `amazonChoice`      | Boolean | Amazon's Choice | 是否属于 AC 推荐词           |
| 29  | `searchRank`        | Integer | 搜索排名            | ABA 搜索频率排名            |
| 30  | `└code`             | String  | 类目代码            | 官方表中重复出现，未明确所属对象      |
| 31  | `└label`            | String  | 类目名称            | 官方表中重复出现，未明确所属对象      |
| 32  | `clicks`            | Integer | 点击量             | 关键词对应的点击次数            |
| 33  | `impressions`       | Long    | 展示量             | 关键词对应的商品展示次数          |

`relevancy`为相关度，表示挖掘出的关键词，与输入的核心关键词有多大程度的商品关联。根据卖家精灵官方说明，其核心判断依据是：两个关键词在亚马逊自然搜索结果第一页中，出现了多少相同的商品 ASIN。

`spr`是指上首页所需的预估单量，全称 SellerSprite Product Rank，它用于估算：要让商品在某个关键词的亚马逊搜索结果中获得首页排名，大约需要达到怎样的订单表现。根据官方说明，它采用的是**8 天预估单量**。

`titleDensity`是标题密度，它表示亚马逊搜索该关键词时，搜索结果第一页中，有多少个商品的标题包含该关键词。

# 三、流量分析

核心目标：了解竞争对手通过哪些搜索词或关联位置获得流量。

| 序号  | MCP Code               | 中文名称   | 核心作用                          |
| --- | ---------------------- | ------ | ----------------------------- |
| 18  | `traffic_keyword`      | 关键词反查  | 查询 ASIN 近 30 天进入搜索结果前 3 页的流量词 |
| 19  | `traffic_extend`       | 拓展流量词  | 支持多个 ASIN 的搜索流量词拓展            |
| 20  | `traffic_listing`      | 关联流量列表 | 查询产品及其变体的关联流量来源               |
| 21  | `traffic_keyword_stat` | 流量词统计  | 查询 ASIN 的搜索流量词统计数据            |
| 22  | `traffic_listing_stat` | 关联流量统计 | 查询 ASIN 的关联流量统计数据             |
| 23  | `traffic_source`       | 流量来源分析 | 查询关键词和 ASIN 之间的曝光流向关系         |

## traffic_keyword（关键词反查）

`traffic_keyword`是卖家精灵 MCP 提供的关键词反查接口，主要通过一个 ASIN，查询该商品在哪些关键词的亚马逊搜索结果中获得曝光，并分析这些关键词的流量来源、流量占比、自然排名及广告排名。

官方将流量词定义为该 ASIN 在近 30 天内，曾进入亚马逊前台搜索结果前 3 页的关键词。

### 请求参数

| #   | 参数                       | 类型      | 必填  | 参数名称    | 参数描述                                |
| --- | ------------------------ | ------- | --- | ------- | ----------------------------------- |
| 1   | `marketplace`            | String  | 是   | 站点      | `US` 代表美国站                          |
| 2   | `asin`                   | String  | 是   | 商品 ASIN | 需要反查流量词的商品                          |
| 3   | `keyword`                | String  | 否   | 关键词     | 按指定关键词筛选流量词列表                       |
| 4   | `month`                  | String  | 否   | 历史月份    | `yyyyMM` 格式，例如 `202609`；不传默认最近 30 天 |
| 5   | `badges`                 | List    | 否   | 流量词类型   | 根据自然搜索、广告等曝光类型筛选                    |
| 6   | `trafficKeywordTypes`    | List    | 否   | 流量占比类型  | 主要流量词、精准流量词等                        |
| 7   | `conversionKeywordTypes` | List    | 否   | 流量转化类型  | 转化优质词、转化平稳词等                        |
| 8   | `page`                   | Integer | 否   | 页码      | 默认 `1`                              |
| 9   | `size`                   | Integer | 否   | 每页数量    | 默认 `50`，最大 `100`                    |
| 10  | `order`                  | Object  | 否   | 排序配置    | 包含排序字段和排序方向                         |
| 11  | `└field`                 | String  | 否   | 排序字段    | 默认 `rankPosition`，见下表               |
| 12  | `└desc`                  | Boolean | 否   | 排序方向    | `true` 降序，`false` 升序；默认 `false`     |

### 返回参数

一个商品 ASIN + 一份关键词列表 + 每个关键词对应的排名和流量数据。

## traffic_extend

`traffic_extend` 是卖家精灵 MCP 提供的批量关键词反查接口，主要用于同时查询多个 ASIN 的搜索流量词，并将关键词合并、去重，帮助卖家建立竞品关键词库。

输入多个竞品 ASIN → 获取这些商品覆盖的搜索流量词 → 合并去重 → 发现竞品共同覆盖的关键词及差异化关键词。

### 请求参数

#### 基础参数

| #   | 参数            | 类型      | 必填  | 参数名称    | 参数描述                               |
| --- | ------------- | ------- | --- | ------- | ---------------------------------- |
| 1   | `marketplace` | String  | 是   | 站点      | 美国站使用 `US`                         |
| 2   | `historyDate` | String  | 否   | 查询月份    | `yyyyMM` 格式，例如 `202608`；不传默认近 30 天 |
| 3   | `asinList`    | List    | 是   | ASIN 列表 | 输入 1～20 个 ASIN                     |
| 4   | `queryType`   | Integer | 否   | 查询变体方式  | `0` 全部变体、`1` 畅销变体、`2` 当前变体；默认 `2`  |

#### 关键词市场指标筛选

| #   | 参数                     | 类型      | 参数名称      | 参数描述           |
| --- | ---------------------- | ------- | --------- | -------------- |
| 5   | `minSearches`          | Integer | 最小月搜索量    | 关键词搜索量下限       |
| 6   | `maxSearches`          | Integer | 最大月搜索量    | 关键词搜索量上限       |
| 7   | `minSearchRank`        | Integer | 最小搜索排名    | ABA 搜索频率排名数值下限 |
| 8   | `maxSearchRank`        | Integer | 最大搜索排名    | ABA 搜索频率排名数值上限 |
| 9   | `minPurchases`         | Integer | 最小月购买量    | 月购买量下限         |
| 10  | `maxPurchases`         | Integer | 最大月购买量    | 月购买量上限         |
| 11  | `minPurchaseRate`      | Float   | 最小购买率     | 购买率下限          |
| 12  | `maxPurchaseRate`      | Float   | 最大购买率     | 购买率上限          |
| 13  | `minProducts`          | Integer | 最小商品数     | 相关商品数量下限       |
| 14  | `maxProducts`          | Integer | 最大商品数     | 相关商品数量上限       |
| 15  | `minSupplyDemandRatio` | Float   | 最小供需比     | 供需比下限          |
| 16  | `maxSupplyDemandRatio` | Float   | 最大供需比     | 供需比上限          |
| 17  | `minBid`               | Float   | 最低 PPC 竞价 | 建议竞价下限         |
| 18  | `maxBid`               | Float   | 最高 PPC 竞价 | 建议竞价上限         |
| 19  | `minAdProducts`        | Integer | 最小广告竞品数   | 广告竞品数量下限       |
| 20  | `maxAdProducts`        | Integer | 最大广告竞品数   | 广告竞品数量上限       |
| 21  | `minAvgPrice`          | Float   | 最低平均价格    | 相关商品均价下限       |
| 22  | `maxAvgPrice`          | Float   | 最高平均价格    | 相关商品均价上限       |

#### 关键词特征及竞争筛选

|#|参数|类型|参数名称|参数描述|
|---|---|---|---|---|
|23|`minWordCount`|Integer|最小单词数|关键词最少包含多少个单词|
|24|`maxWordCount`|Integer|最大单词数|关键词最多包含多少个单词|
|25|`includeKeywords`|List|包含关键词|筛选包含指定内容的关键词|
|26|`excludeKeywords`|List|排除关键词|排除包含指定内容的关键词|
|27|`minSPR`|Integer|最小 SPR|SPR 下限|
|28|`maxSPR`|Integer|最大 SPR|SPR 上限|
|29|`minTitleDensity`|Integer|最小标题密度|标题密度下限|
|30|`maxTitleDensity`|Integer|最大标题密度|标题密度上限|
|31|`minMonopolyClickRate`|Float|最小点击集中度|点击集中度下限|
|32|`maxMonopolyClickRate`|Float|最大点击集中度|点击集中度上限|
|33|`minTrafficPercentage`|Float|最小流量占比|流量占比筛选下限|
|34|`maxTrafficPercentage`|Float|最大流量占比|流量占比筛选上限|
|35|`minConversionRate`|Float|最小转化率|转化率筛选下限|
|36|`maxConversionRate`|Float|最大转化率|转化率筛选上限|
|37|`minCompetitors`|Integer|最小 ASIN 数|相关 ASIN 数量下限|
|38|`maxCompetitors`|Integer|最大 ASIN 数|相关 ASIN 数量上限|
|39|`amazonChoice`|Boolean|亚马逊推荐词|`true` 筛选 Amazon's Choice 相关关键词|

#### 分页与排序参数

|#|参数|类型|参数名称|参数描述|
|---|---|---|---|---|
|40|`page`|Integer|页码|从 `1` 开始，默认 `1`|
|41|`size`|Integer|每页数量|默认 `50`，最大 `50`|
|42|`order`|Object|排序配置|包含排序字段和排序方向|
|43|`└field`|String|排序字段|见下表|
|44|`└desc`|Boolean|排序方向|`true` 降序，`false` 升序，默认降序|

这里有一个比较重要的参数`queryType`，它是 `traffic_extend` 相比 `traffic_keyword` 最值得学习的功能。

|`queryType`|查询方式|实际含义|
|---|---|---|
|`0`|所有变体|查询 Listing 下全部变体的流量词并合并去重|
|`1`|畅销变体|使用系统识别出的主要引流变体进行拓词|
|`2`|当前变体|只查询传入的具体 ASIN，默认值|


# 四、ABA 数据分析

核心目标：基于 Amazon Brand Analytics 数据研究关键词需求与竞争。

| 序号  | MCP Code               | 中文名称        | 核心作用            |
| --- | ---------------------- | ----------- | --------------- |
| 24  | `aba_research_weekly`  | ABA 数据选品（周） | 按周度 ABA 指标筛选关键词 |
| 25  | `aba_research_monthly` | ABA 数据选品（月） | 按月度 ABA 指标筛选关键词 |
| 26  | `aba_research_trend`   | ABA 关键词趋势   | 查询 ABA 关键词历史趋势  |

# 五、市场分析

核心目标：判断某个类目市场有多大、竞争有多激烈，以及是否值得进入。

| 序号  | MCP Code                             | 中文名称    | 核心作用                |
| --- | ------------------------------------ | ------- | ------------------- |
| 27  | `market_research`                    | 选市场列表   | 根据筛选条件查找符合要求的细分类目市场 |
| 28  | `market_research_statistics`         | 市场统计    | 查询市场规模、销量、销售额等统计指标  |
| 29  | `market_product_demand_trend`        | 商品需求趋势  | 分析市场需求及其历史变化        |
| 30  | `market_product_concentration`       | 商品集中度   | 分析市场销量是否集中在少数头部商品   |
| 31  | `market_brand_concentration`         | 品牌集中度   | 分析头部品牌的市场份额和集中程度    |
| 32  | `market_seller_concentration`        | 卖家集中度   | 分析头部卖家的市场份额和集中程度    |
| 33  | `market_seller_type_concentration`   | 卖家类型分布  | 分析不同卖家类型的市场分布       |
| 34  | `market_seller_country_distribution` | 卖家所属地分布 | 分析卖家所属国家或地区的分布情况    |
| 35  | `market_listing_date_distribution`   | 上架时间分布  | 分析市场中不同上架时长商品的分布    |
| 36  | `market_listing_trend_distribution`  | 上架趋势分布  | 分析市场中商品的上架变化趋势      |
| 37  | `market_ratings_count_distribution`  | 评分数分布   | 分析不同评分数量区间的商品分布     |
| 38  | `market_rating_distribution`         | 评分值分布   | 分析不同星级评分区间的商品分布     |
| 39  | `market_price_distribution`          | 价格分布    | 分析不同价格区间的商品分布       |
| 40  | `market_ebc_distribution`            | A+ 视频分布 | 分析商品 A+ 页面和视频的配置情况  |

# 六、评论分析

核心目标：了解消费者对商品的真实反馈，挖掘产品改进机会。

| 序号  | MCP Code | 中文名称 | 核心作用                     |
| --- | -------- | ---- | ------------------------ |
| 41  | `review` | 查评论  | 查询商品评论数据，辅助分析好评、差评和消费者痛点 |


# 七、商标查询

核心目标：查询商标注册信息，辅助识别品牌商标风险。

| 序号  | MCP Code                 | 中文名称      | 核心作用         |
| --- | ------------------------ | --------- | ------------ |
| 42  | `trademark_country_list` | 全球商标库数据范围 | 查询支持检索的国家或地区 |
| 43  | `trademark_detail`       | 商标详情      | 获取指定商标的详细信息  |
| 44  | `trademark_list`         | 商标列表      | 根据条件检索商标记录   |
| 45  | `trademark_stats`        | 商标统计      | 查询商标相关统计数据   |