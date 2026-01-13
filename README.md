### 记录与展示上海房地网数据

本项目包含两个脚本：
- `fangdi_crawler.py`：使用 Playwright 抓取房地网数据并追加保存到 `fangdi_data.csv`。
- `fangdi_report.py`：读取 `fangdi_data.csv`，可按日/周/月/季度汇总展示。

#### 环境准备
```bash
pip install -r requirements.txt
```

#### 爬虫采集
```bash
python fangdi_crawler.py
```
运行后会在当前目录生成/追加 `fangdi_data.csv`。

#### 数据展示（切换时间维度）
```bash
# 按日（默认），展示前 20 行
python fangdi_report.py --freq daily

# 按周，展示前 8 行
python fangdi_report.py --freq weekly --top 8

# 按月，限定日期范围
python fangdi_report.py --freq monthly --start 2025-11-01 --end 2025-12-31

# 按季度
python fangdi_report.py --freq quarterly
```
参数说明：
- `--csv`：指定 CSV 路径，默认 `fangdi_data.csv`
- `--freq`：`daily|weekly|monthly|quarterly` 及其缩写
- `--start` / `--end`：筛选日期范围（可选）
- `--top`：输出前 N 行（默认 20）

#### 页面直接查看（可切换时间范围）
- 打开 `report_viewer.html`（双击或拖到浏览器）。
- 点击“选择 CSV”，选中 `fangdi_data.csv`。
- 选择时间维度（日/周/月/季度）以及开始/结束日期，点击“生成表格”即可在页面展示汇总结果（纯前端，不依赖服务端）。
