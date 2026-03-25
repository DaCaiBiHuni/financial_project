# 投资组合追踪桌面应用
## 技术设计文档 v1.0

---

# 1. 文档目标

本文档用于定义“投资组合追踪桌面应用”的技术实现方案，确保产品从需求阶段顺利进入开发阶段，并满足以下目标：

- 支持追踪特定投资产品走势
- 支持展示当前投资组合详情
- 支持快速添加新的产品
- 支持后续功能扩展
- 具备良好的桌面应用结构和可维护性

本文档聚焦于**技术选型、系统架构、模块设计、数据设计、扩展设计、开发边界**。

---

# 2. 技术目标

本项目的技术目标如下：

1. **构建桌面级应用**
2. **采用本地数据持久化**
3. **具备模块化结构**
4. **支持多产品类型扩展**
5. **支持多数据源扩展**
6. **便于后续增加图表、提醒、交易记录等功能**

---

# 3. 技术选型

## 3.1 推荐选型
### 桌面框架
**Python + PySide6**

### 本地数据库
**SQLite**

### ORM / 数据访问层
可选两种路线：

- 轻量路线：`sqlite3`
- 结构化路线：`SQLAlchemy`

### 图表组件
可选：
- `PySide6 Qt Charts`
- `pyqtgraph`
- `matplotlib`

### 配置管理
- Python `dataclasses`
- 或 `pydantic-settings`

---

## 3.2 选型理由

### 选择 Python
- 当前环境已就绪
- 开发速度快
- 生态成熟
- 适合快速构建桌面原型和业务逻辑

### 选择 PySide6
- 更像真正桌面软件
- UI 结构清晰
- 支持表格、图表、菜单栏、侧边栏、弹窗
- 比 tkinter 更适合做正式产品原型

### 选择 SQLite
- 本地部署简单
- 不依赖额外数据库服务
- 适合个人桌面工具
- 后续支持复杂查询

### 选择模块化架构
因为产品未来要支持：
- 新资产类型
- 新数据源
- 新分析模块
- 新页面  
所以不能做成单文件、小脚本式项目。

---

# 4. 总体架构设计

## 4.1 架构原则

系统设计遵循以下原则：

- **分层**
- **模块化**
- **可替换**
- **可扩展**
- **本地优先**

---

## 4.2 分层结构

建议采用以下分层：

### 1. 表现层（UI Layer）
负责：
- 窗口
- 页面
- 表格
- 图表
- 菜单栏
- 用户交互

### 2. 应用层（Application Layer）
负责：
- 页面行为编排
- 功能流程控制
- 调用服务模块
- 汇总数据给 UI

### 3. 领域层（Domain Layer）
负责：
- 产品模型
- 持仓模型
- 组合计算逻辑
- 业务规则

### 4. 数据层（Data Layer）
负责：
- SQLite 读写
- 仓储层（Repository）
- 历史价格存储
- 配置持久化

### 5. 数据源层（Provider Layer）
负责：
- 获取外部行情
- 标准化不同来源的数据格式
- 支持未来替换或新增数据源

---

# 5. 项目目录结构建议

建议项目结构如下：

```text
investment_tracker/
├─ app/
│  ├─ main.py
│  ├─ ui/
│  │  ├─ main_window.py
│  │  ├─ pages/
│  │  │  ├─ dashboard_page.py
│  │  │  ├─ products_page.py
│  │  │  ├─ portfolio_page.py
│  │  │  └─ settings_page.py
│  │  ├─ widgets/
│  │  │  ├─ product_table.py
│  │  │  ├─ portfolio_table.py
│  │  │  └─ chart_widget.py
│  ├─ application/
│  │  ├─ controllers/
│  │  │  ├─ product_controller.py
│  │  │  ├─ portfolio_controller.py
│  │  │  └─ dashboard_controller.py
│  │  └─ services/
│  │     ├─ product_service.py
│  │     ├─ portfolio_service.py
│  │     └─ market_service.py
│  ├─ domain/
│  │  ├─ models/
│  │  │  ├─ product.py
│  │  │  ├─ position.py
│  │  │  ├─ price_point.py
│  │  │  └─ portfolio_summary.py
│  │  └─ enums/
│  │     └─ asset_type.py
│  ├─ infrastructure/
│  │  ├─ db/
│  │  │  ├─ database.py
│  │  │  ├─ repositories/
│  │  │  │  ├─ product_repository.py
│  │  │  │  ├─ position_repository.py
│  │  │  │  └─ price_repository.py
│  │  ├─ providers/
│  │  │  ├─ base_provider.py
│  │  │  ├─ mock_provider.py
│  │  │  └─ future_market_provider.py
│  │  └─ config/
│  │     └─ settings.py
│  └─ utils/
│     ├─ logger.py
│     └─ time_utils.py
├─ data/
│  └─ app.db
├─ docs/
│  ├─ PRD.md
│  └─ TECH_DESIGN.md
├─ tests/
│  ├─ test_product_service.py
│  ├─ test_portfolio_service.py
│  └─ test_repository.py
├─ requirements.txt
└─ README.md
```

---

# 6. 核心模块设计

# 6.1 产品模块（Products）

## 目标
管理所有被追踪的投资产品。

## 职责
- 新增产品
- 编辑产品
- 删除产品
- 查询产品
- 获取产品详情
- 获取产品历史价格

## 核心对象
### Product
建议字段：
- id
- name
- symbol
- asset_type
- source
- current_price
- currency
- note
- created_at
- updated_at

---

# 6.2 投资组合模块（Portfolio）

## 目标
展示用户当前持仓和组合整体状态。

## 职责
- 管理持仓
- 计算当前市值
- 计算收益
- 计算组合汇总

## 核心对象
### Position
建议字段：
- id
- product_id
- quantity
- average_cost
- current_price
- market_value
- profit_loss
- profit_loss_rate
- updated_at

### PortfolioSummary
建议字段：
- total_cost
- total_market_value
- total_profit_loss
- total_profit_loss_rate

---

# 6.3 行情数据模块（Market Data）

## 目标
统一处理外部价格数据。

## 职责
- 获取产品当前价格
- 获取历史价格
- 标准化不同数据源格式

## 设计建议
定义统一 Provider 接口：

```python
class BaseMarketProvider:
    def get_current_price(self, symbol: str) -> dict:
        ...
    def get_price_history(self, symbol: str, period: str) -> list:
        ...
```

后续每新增一个数据源，只需要新增一个实现类，而不是改动上层业务逻辑。

---

# 6.4 仪表盘模块（Dashboard）

## 目标
展示打开应用后的全局摘要。

## 职责
- 显示组合总览
- 展示重点产品变化
- 汇总收益信息
- 后续展示图表和统计卡片

---

# 6.5 设置模块（Settings）

## 目标
集中管理应用配置。

## 职责
- 数据源配置
- 显示配置
- 刷新频率配置
- 本地化配置
- 后续账户级配置

---

# 7. 数据模型设计

# 7.1 产品表 `products`

建议字段：

| 字段名 | 类型 | 说明 |
|---|---|---|
| id | INTEGER | 主键 |
| name | TEXT | 产品名称 |
| symbol | TEXT | 产品代码 |
| asset_type | TEXT | 产品类型 |
| source | TEXT | 数据来源 |
| currency | TEXT | 货币 |
| current_price | REAL | 当前价格 |
| note | TEXT | 备注 |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

---

# 7.2 持仓表 `portfolio_positions`

| 字段名 | 类型 | 说明 |
|---|---|---|
| id | INTEGER | 主键 |
| product_id | INTEGER | 关联产品 |
| quantity | REAL | 持仓数量 |
| average_cost | REAL | 平均成本 |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

---

# 7.3 历史价格表 `price_history`

| 字段名 | 类型 | 说明 |
|---|---|---|
| id | INTEGER | 主键 |
| product_id | INTEGER | 关联产品 |
| price | REAL | 价格 |
| timestamp | TEXT | 时间戳 |

---

# 7.4 配置表 `settings`

| 字段名 | 类型 | 说明 |
|---|---|---|
| key | TEXT | 配置键 |
| value | TEXT | 配置值 |

---

# 8. 扩展性设计

这是本项目最关键的技术点之一。

## 8.1 产品类型扩展
不要写死为“股票”应用，而要抽象为“资产产品”。

通过：
- `asset_type`
- 通用字段
- 可选扩展字段  
来支持未来扩展。

---

## 8.2 数据源扩展
采用 Provider 模式：

- `BaseMarketProvider`
- `MockProvider`
- `RealProviderA`
- `RealProviderB`

UI 和业务层只面向统一接口，不直接耦合某个 API。

---

## 8.3 页面扩展
UI 页面尽量按模块拆分，不把所有页面逻辑堆到主窗口。

后续新增：
- AlertsPage
- TransactionsPage
- AnalyticsPage  
都能自然接进去。

---

## 8.4 分析模块扩展
组合收益、占比分析、趋势分析等最好拆到 service 层，不直接写死在 UI 中。

---

# 9. 页面设计建议

# 9.1 主窗口布局
建议结构：

- **顶部：菜单栏 / 工具栏**
- **左侧：导航栏**
- **右侧：主内容区**

---

# 9.2 页面划分

## Dashboard
展示：
- 总成本
- 总市值
- 总收益
- 收益率
- 最近更新情况

## Products
展示：
- 产品列表
- 添加按钮
- 搜索框
- 产品详情
- 产品走势图

## Portfolio
展示：
- 当前持仓
- 市值
- 盈亏
- 汇总信息

## Settings
展示：
- 数据源设置
- 刷新配置
- 显示偏好

---

# 10. 业务流程设计

# 10.1 添加产品流程
1. 用户点击“添加产品”
2. 输入基础信息
3. 保存到数据库
4. 调用数据源获取价格
5. 更新产品详情页和列表

# 10.2 添加持仓流程
1. 用户选择一个产品
2. 输入持仓数量和成本
3. 保存到数据库
4. 重新计算组合汇总

# 10.3 查看组合流程
1. 读取持仓信息
2. 读取当前产品价格
3. 计算每个持仓市值和收益
4. 汇总得到组合数据
5. 返回 UI 展示

---

# 11. 开发阶段建议

## 阶段 1：项目基础搭建
- 初始化项目结构
- 建立主窗口
- 建立导航框架
- 建立数据库连接
- 建立基础数据模型

## 阶段 2：产品模块
- 产品列表
- 添加产品
- 产品详情
- 当前价格展示

## 阶段 3：投资组合模块
- 持仓录入
- 持仓列表
- 组合汇总计算

## 阶段 4：图表与体验优化
- 价格趋势图
- 页面交互优化
- 基础设置页

## 阶段 5：扩展预留
- Provider 抽象
- 交易记录结构预留
- 警报系统接口预留

---

# 12. 测试策略

## 12.1 单元测试
覆盖：
- 产品 service
- 组合计算逻辑
- 数据仓储层

## 12.2 集成测试
覆盖：
- 数据存取流程
- 添加产品到组合的完整链路

## 12.3 UI 测试
初期可人工验证为主，后续再考虑自动化 UI 测试。

---

# 13. 风险与技术注意点

## 13.1 数据源不稳定
解决方式：
- 抽象 provider
- 支持 mock provider
- 为真实 provider 留重试与错误处理

## 13.2 模型设计过早固化
解决方式：
- 保持产品模型通用
- 用 asset_type + provider 扩展

## 13.3 UI 和业务逻辑耦合
解决方式：
- UI 只展示
- Service 层做业务计算
- Repository 层管数据

---

# 14. 当前建议的最终实现路线

## 推荐技术栈
- **Python**
- **PySide6**
- **SQLite**
- **SQLAlchemy（推荐）**
- **pyqtgraph / Qt Charts**

## 推荐开发方式
- 先做 **MVP 桌面原型**
- 再逐步增强数据源和分析能力
- 优先保证结构合理，而不是一开始追求功能过多

---

# 15. 下一步输出建议

现在文档层已经足够进入真正开发前准备。  
接下来最合理的下一步是：

## **一期开发计划（Implementation Plan）**

它会比技术文档更具体，直接告诉你：

- 第一版先做哪些页面
- 每个页面要完成什么
- 任务按什么顺序开发
- 哪些是必须，哪些可以后补
