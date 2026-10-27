# 当前电脑项目同步与迁移

日期：2026-10-28。同步范围为本 bestOS 工作目录；不读取或上传其他无关个人目录。

## GitHub 核对

对 main 提交 0c25ba16835cb0c8cb1062166e42d3b6436b1f27 的远端文件树进行 Git blob 哈希比对：本地正式代码、配置、文档、完整 AOSP manifest 和字标素材没有遗漏或差异。远端共 61 个文件。

原厂镜像、系统文件/驱动与 MT APK 尚未上传。连接器未提供 Release 附件接口，本机没有 gh 或已配置的命令行 GitHub 登录凭据；不能把目录清单同步说成大文件上传完成。

## 完整本地迁移包

运行 `python3 tools/package_workspace.py` 生成：

- `out/migration/bestOS-workspace.tar.gz`：项目源码配置、素材、MT APK、原厂下载包、解出的 images、system.raw.img、系统文件、驱动候选及 boot 分量。
- `out/migration/workspace-manifest.json`：归档源文件路径、字节数与 SHA-256。
- `out/migration/SHA256SUMS`：完整归档的 SHA-256。

排除 out 生成物（包含重复打包的 Release 附件）、下载分片缓存、残缺下载、Python 缓存、Git/Repo 管理目录及密钥/环境变量文件。原厂完整下载包及所有有效提取结果保留；Release 附件可由 `tools/package_binary_assets.py` 重建。这不是完整 AOSP 源码或可刷机 bestOS。

先对迁移包核对 SHA-256，再在另一台电脑的新目录解压，避免覆盖已有工程。可以离线搬运这一个归档继续工作；需保留权限/链接语义的原厂系统条目以提取清单为准，宿主普通文件不是已重建的 ROM 文件系统。

本地迁移包不等于 GitHub Release 已发布。大附件上传仍需可用的上传通道；进度见 [二进制附件](binary-assets.md)。Linux 环境入口见 [接手说明](linux-start.md)。
