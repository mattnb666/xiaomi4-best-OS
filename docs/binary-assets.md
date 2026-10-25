# 镜像、驱动与 APK 附件状态

文档核对日期：2026-10-25。项目总体状态见 [README](../README.md)。

更新日期：2026-10-25。用户已明确要求上传以下二进制。当前状态：**本地打包和校验完成，GitHub Release 上传未完成**。

目录：`out/github-assets/`。可用 `python3 tools/package_binary_assets.py` 从现有本地提取结果重新打包；压缩文件元数据可能使重打包后的哈希变化，须重新生成清单。

| 文件 | 字节数 | 内容 |
| --- | ---: | --- |
| `cancro-stock-images.tar.gz` | 1,238,999,871 | 原厂 images 目录，含 system/boot/recovery、基带及其他固件 |
| `cancro-system-files.tar.gz` | 726,994,902 | 提取的系统普通文件，含驱动候选、HAL、库及配置；附权限/链接和校验清单 |
| `cancro-boot-components.tar.gz` | 22,556,595 | 分离的内核、ramdisk、设备树及检查记录 |
| `MTManager-clone-2.26.8.apk` | 32,070,086 | 用户提供的 MT 管理器共存版，原签名保留 |

## SHA-256

```text
319ddbfa949956ef0ab317b79a2bede24fb6b42276a7e9811b321d092a50242d  cancro-stock-images.tar.gz
0d8b95317d5a678a0f891c3619a86f5baf6336498d4efc5eab7010208dddf977  cancro-system-files.tar.gz
bef7978024856139a841550ae1a33fcabbc129682b76032738d4840c826e1f46  cancro-boot-components.tar.gz
caa2d74e218ae3162fbef38836a4190fea1276576461d358e0d3681d40f3e3bb  MTManager-clone-2.26.8.apk
```

三个归档已经逐文件读回验证；APK 哈希与原文件一致。校验值同时保存在本地 SHA256SUMS 和 asset-manifest.json。system.raw.img 是稀疏 system.img 的展开副本，可重建，未重复打包；下载缓存及残缺下载未打包。

## 上传阻碍与后续

当前连接器没有 Release 附件上传接口。浏览器发布页反复超时；用户反馈已登录，但最后可观察的应用内浏览器页面仍是登录页，未确认是同一登录会话。宿主机没有 gh 或已配置的 GitHub 命令行凭据。待可操作的已登录上传通道恢复后，上传附件与校验清单，再记录实际 Release URL、附件大小和远端验证结果。没有发布成功的下载链接。

这些是原厂适配材料，不是 Android 10 / Linux 6.1 bestOS 可刷机包，也不表示驱动已经完成移植。
