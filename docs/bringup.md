# 小米 4 LTE / Android 10 适配记录

文档核对日期：2026-10-25。项目总体状态见 [README](../README.md)。

更新日期：2026-10-25。以下社区来源为前期检索记录，不表示本次重新核验或已选定。

## 已查到的来源

1. LineageOS 官方历史设备树：
   https://github.com/LineageOS/android_device_xiaomi_cancro
   当前页面默认分支 cm-14.1。不能将它直接视为 Android 10 设备树。
2. 官方历史设备说明：
   https://lineageos.github.io/lineage_wiki/devices/cancro/variant2/
   标明小米 4 使用 cancro 代号；历史支持列出 14.1 / Android 7.1。
3. vasishath 的 AndroidFileHost 开发者页面：
   https://prd.androidfilehost.com/?uid=24052804347827467&w=profile
   搜索结果列出 Aosp-10-cancro-20190915.zip。仅作为 Android 10 底包线索，未下载、未校验、未验证启动及 LTE。
4. 后续社区设备树线索：
   https://github.com/Mi3-4-Dev/android_device_xiaomi_cancro
   搜索可见 lineage-18.1 内容；Android 11 分支不能直接作为 Android 10 构建依据。

## 当前构建环境

- 用户的另一台电脑：Windows，8 GB RAM，500 GB 硬盘总容量可用于项目；尚未安装 Ubuntu 或 WSL2。实际空闲容量、磁盘数据和可用编译环境待核实，尚未执行安装或分区操作。

- 当前工作站：macOS / x86_64。
- 宿主机空闲空间随下载及打包变化，不能把早期约 70 GiB 的检查值当作当前剩余容量。
- PATH 中找到 git，未找到 repo 或 docker。
- 原厂镜像、系统文件及专有库候选已提取；尚无验证可用的 Android 10 vendor 配置、设备树或完整内核源码。
- AOSP 官方 manifest 地址为 https://android.googlesource.com/platform/manifest ，GitHub 参考镜像为 https://github.com/aosp-mirror/platform_manifest 。
- 已查到 android-10.0.0_r47 标签，尚未最终锁定；已取得完整 default.xml 并解析 741 个项目，旧 default.xml.partial 仅保留失败记录；尚未同步完整源码。
- Linux 6.1 移植和条件优先 KSU 方案见 `kernel-6.1-port.md`、`root-integration.md`。
- 完整源码构建应另行准备容量充足的 Linux x86_64 环境，具体工具链由选定源码版本决定。

## 需要先确认

用户已确认：基于 AOSP 原生 Android 10 源码定制，没有现成 Android 10 底包；要求使用小米 MiFlash 线刷工具安装。

- 手机准确型号（含 LTE 变种）、当前系统和 recovery 版本。
- 查找已在该手机上运行的 Android 10 适配项目及其源码、构建说明和已知问题，作为移植参考。
- 确定 AOSP Android 10 标签，以及设备树、公共设备树、内核、vendor blobs 与上游 manifest 的匹配提交。
- 实际分区布局与容量、所需固件版本、安装脚本的机型断言。

## 制作顺序

1. 核实基础 Android 10 在目标设备上的启动、触摸、显示、电话、短信和 LTE。
2. 固定 AOSP 标签、设备适配提交及专有文件校验值，记录许可及修改范围。
3. 接入 bestOS 品牌属性、设置中的版本信息、开机动画和默认壁纸。
4. 在设备资源允许范围内定制桌面和系统界面，不预先承诺相机、VoLTE 等驱动能力。
5. 构建、检查镜像大小和签名，在保留可恢复原系统的条件下进行实机验证。
6. 验证 Wi-Fi、蓝牙、音频、相机、充电、休眠及重启，最后交付有校验值和已知问题记录的安装包。

## 当前验收边界

项目已完成初始配置、原厂包提取、素材归档和大附件打包；仍未进行 Android / Linux 6.1 编译或实机测试。自定义属性不等于完整系统改名，也不代表刷机包已经可用。保留上游真实安全补丁日期和设备身份，不伪造版本安全状态。

## MiFlash 交付要求

完整硬件适配矩阵和原厂文件用途见 `hardware-port.md`；屏幕、触摸、相机、处理器相关驱动与内核编译均属于本项目交付范围，当前尚未实现。

- 目标为 Windows MiFlash 使用的 fastboot 线刷包，不能以 recovery 卡刷 ZIP 替代。
- 先获取并检查对应 LTE 变种的可信原厂线刷包，核对分区名、镜像格式、机型检查与固件依赖。
- 构建的 boot/system 等镜像必须与该设备分区容量及 Android 10 启动方案一致；实际刷写列表以验证结果为准。
- 不猜测分区表，不使用其他机型的引导链、基带或分区镜像。
- 不默认提供重新锁定引导程序的脚本；自定义系统是否可刷需验证实际设备状态。
- 记录清除用户数据的具体步骤，并在执行刷机前确认备份及恢复方式。
- 最终包应包含验证后的镜像、适用于目标 MiFlash 版本的脚本、SHA-256 清单、安装说明及已知问题。
- 未核对上述条件之前，不生成可执行刷写脚本，避免把示例脚本误当作已验证安装工具。

## AOSP 准备进度（2026-10-25）

已取得 Android 10 r47 完整 manifest，并准备 Linux 同步脚本。当前 Mac 约 58 GiB 可用；用户确认 Windows 电脑尚未安装 WSL2 / Ubuntu，完整同步尚未开始。步骤和证据见 [AOSP 源码基底](aosp-base.md)。
