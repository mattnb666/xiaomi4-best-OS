# 原厂包提取记录

报告正文见 `docs/stock-extraction-report.md`，硬件适配计划见 `docs/hardware-port.md`。

本目录提供归档来源和校验值、原厂镜像校验清单、boot 参数和驱动候选分类摘要。它们是静态提取结果，不代表已经完成 Android 10 适配。

原厂镜像和第三方二进制保留在本地 `downloads/stock-rom/`，不随 Git 仓库分发。

## 重现工具

在仓库根目录使用 Python 3，并准备 curl：

1. `python3 tools/download_stock_rom.py` 下载、合并并校验指定原厂包。
2. 将归档安全解出至 `downloads/stock-rom/extracted/`，保留归档内顶层目录；禁止执行其中的刷机脚本。
3. `python3 tools/unpack_stock_images.py` 展开 system 镜像并分离 boot 组件。此解析器针对该原厂版本，不适用于任意 boot 格式。
4. 安装 `dissect.extfs==3.14`，执行 `python3 tools/extract_stock_system.py` 提取系统普通文件并记录符号链接。

完整文件清单在运行后的 `analysis/system-file-manifest.json`，权限和链接仅记录、不在宿主机恢复。此处没有安装或刷写手机的命令。
