# xiaomi 4 bestOS 0.1-dev

为小米 4 LTE 定制的独立系统，以 AOSP Android 10（API 29）为基础。更新日期：**2026-10-26**。

**当前完成：需求记录、初始产品配置、原厂刷机包下载与提取、字标素材上传、镜像和 APK 本地打包。尚未完成 Android / Linux 6.1 编译或实机验证，没有可刷入的 bestOS。**

## 全部已确认需求

| 项目 | 最新约定 |
| --- | --- |
| 设备 | 小米 4 LTE / mi4lte / cancro 系列，3 GB RAM、16 GB 存储；具体板号、分区和硬件组合待实机核对 |
| 当前手机系统 | 用户报告 MIUI 10、8.9.13 开发版、Android 5.0.5，尚未读取实机验证；不与下载的 Android 6.0.1 原厂包混淆 |
| 系统 | bestOS 0.1，开发标识 0.1-dev；基于 AOSP Android 10，桌面、SystemUI、自带应用、设置和默认配置全面定制 |
| 内核 | 目标 Linux 6.1 系列，需 ARM32 设备移植；原厂提取内核为 3.4.0-g6231d51，尚无可启动的 6.1 产物 |
| Root | 6.1 与 KernelSU 均在此机验证通过后以 KSU 替换 Alpha；Alpha 30700 仅保留原候选。KSU 路线交付匹配的 KSU boot，不再要求 Alpha 修补；不能仅安装管理 APK 就视为 root 已集成 |
| 刷机 | Windows 小米 MiFlash fastboot 线刷包；最终镜像必须适配真实分区，不以卡刷包替代 |
| 体积 | 尽量控制系统内容在 3 GB 内，仍需满足真实分区容量；Google 组件加入后实测，不承诺已达到 |
| 通信 | 保留电话、短信、SIM 蜂窝数据、Wi-Fi、蓝牙 |
| 显示与导航 | 默认竖屏；全面屏手势导航、上滑解锁，保留正常应用方向请求 |
| 基础应用 | 保留电话、联系人、短信、相机、图库、时钟、计算器、录音机、中文输入法等基础应用，进行独立设计 |
| 文件管理 | 唯一预装文件管理器为用户提供的 MT 共存版；可自行更新，禁止普通用户卸载/停用，保留系统文件选择器；卸载保护尚未实现 |
| Google | 加入 Play 商店、Play 服务及常用 Google 应用；具体兼容版本和清单待验证，不额外预装 Google Files |
| 账号与更新 | 基础系统本地运行，无 Google 登录激活，无 bestOS 系统账号；Google 仅在设置中可选绑定。无系统 OTA，保留应用更新，不据此移除 USB OTG |
| 全局语言 | 仅简体中文、繁体中文（香港）、繁体中文（台湾）、English；对应 zh-CN、zh-HK、zh-TW、en-US |
| 地区 | 仅中国大陆、香港、美国，独立于语言；普通第三方应用不能修改受保护的系统地区 |
| 设备身份 | 可改本机名称，普通应用不可修改真实型号；用户明确授权 root 的应用属于例外 |
| 解锁 | 密码输入支持滑动选数字及点击数字；用户要求指纹和面容，但本机无指纹传感器，不能实现内置指纹；前摄 2D 面容待评估 |
| 防盗拍照 | 用户要求密码连续错误两次触发前摄拍照、触发时不弹提示；实施方案为明确告知后单独启用、本地受保护保存，默认关闭，不绕过摄像头隐私机制 |
| 开机画面 | 使用用户提供的 bestOS 启动动画；已收到字标包及第二屏定格帧，完整第一屏和动画帧/时序仍缺失 |

Root 逐应用授权；玩机工具的定向预授权须核验具体 APK 和用户确认的组件清单，不自动向所有应用授予 root。

## 首次开机与本地基础设置

语言 → 地区 → 本地基础设置 → 隐私设置 → 免责声明 → 确认安装所选组件（如有）→ 完成/进入桌面。全程不强制联网或登录账号。

- **个性化广告**：用户期望开启显示 Google 相关推广，关闭隐藏。实现范围是可识别的推广通知和系统推荐入口，不能承诺控制所有 Google 应用内广告；必要通知保留。默认关闭为当前设计值。
- **预装玩机工具箱**：开启后安装用户准备的模块与软件，完成告知和安装确认后执行；指定工具软件的 root 预授权待包名、签名与兼容性核验。模块附件尚未提供。
- **游戏模块**：进入“选择你想玩的游戏：”页面，选项三角洲、和平精英、王者荣耀、其他。前三项安装各自模块和软件；“其他”仅装对应模块，不装软件。当前按可跳过的单选设计，具体附件尚未提供。
- 隐私设置和免责声明放在基础设置与桌面之间；模块安装必须可报告失败、重试、跳过和恢复，不把失败显示为成功。

## 已完成与待完成

| 工作 | 状态及证据 |
| --- | --- |
| 初始 Android 配置 | 已写 common.mk、语言/电话短信等资源覆盖、竖屏与 Wi-Fi 默认值、MT PRESIGNED 预装声明；未编译 |
| 原厂线刷包 | V10.1.1.0.MXDCNFI 已下载、gzip 校验并解出；约 1.21 GB，完整哈希见提取报告 |
| 原厂系统与驱动材料 | 已提取 2,485 个普通文件，记录 2,673 个文件/链接条目；驱动分类仅为候选，未验证 Android 10 / 6.1 兼容 |
| boot 分析 | 已分离内核、ramdisk、DT；确认原厂 Android 6.0.1 / Linux 3.4.0-g6231d51 |
| MT APK | 本地保留 2.26.8-clone，32,070,086 字节；已静态检查，未实机运行或完整签名验证 |
| 字标素材 | 11 张 PNG、原说明和生成脚本及校验清单已上传；原 ZIP 897,791 字节也已上传 |
| 大附件 | 原厂镜像、系统文件/驱动、boot 组件和 APK 共约 2.02 GB 已打包校验；Release 上传仍未完成 |
| AOSP | 已取得官方/镜像地址，r47 为候选标签；已取得完整 manifest（741 个 project），完整源码未同步 |
| 内核与 Root | Linux 6.1 / KSU 为移植与兼容性目标，尚无编译、boot 镜像或 root 实机验证 |
| 系统界面与功能 | 桌面、设置、锁屏、引导、Google、模块安装、卸载保护等主要为规格，尚未实现 |
| 最终交付 | 无 bestOS MiFlash 包，无 Android 10 整机启动或功能验证 |

## 文件与文档入口

- [产品规格](docs/product-spec.md)、[全面定制范围](docs/customization.md)、[设备适配记录](docs/bringup.md)、[硬件适配矩阵](docs/hardware-port.md)。
- [Linux 6.1 移植](docs/kernel-6.1-port.md)、[KSU / Alpha Root 方案](docs/root-integration.md)。
- [首次引导与账号](docs/accounts-and-setup.md)、[基础选项与游戏模块](docs/setup-options.md)、[Google 应用](docs/google-apps.md)。
- [语言](docs/languages.md)、[地区](docs/regions.md)、[设备身份](docs/device-identity.md)、[导航](docs/navigation.md)、[密码与防盗拍照](docs/lockscreen-password.md)。
- [MT 管理器](docs/mt-manager.md)、[开机素材](docs/boot-visuals.md)、[素材目录](assets/branding)、[原始 ZIP](assets/branding/bestOS-wordmark-original.zip)。
- [原厂提取报告](docs/stock-extraction-report.md)、[提取校验记录](reports/stock-rom/README.md)、[二进制附件及上传状态](docs/binary-assets.md)。
- `vendor/bestos/`：当前产品配置、资源覆盖和 MT 预装定义。
- `tools/`：原厂下载、镜像拆解、系统提取与附件打包工具。
- `downloads/stock-rom/`：本地原厂包及提取结果；`out/github-assets/`：待上传大附件。两者不是已发布的下载地址。

## 构建接入与验收

本仓库不是完整 Android 源码树。先固定并验证 cancro 设备构建目标，再将 `vendor/bestos` 放入源码树对应目录，由设备产品 makefile 继承：

```make
$(call inherit-product, vendor/bestos/config/common.mk)
```

MT 模块需要 `vendor/bestos/prebuilt/MTManager/MTManager.apk`；本地已有该文件，但仓库尚无 APK 附件。Google、Root 组件及各模块仍需匹配版本并验证。

编译通过不等于能启动；内核启动不等于 Android 启动；进入桌面不等于整机可用。最终须验证显示/触摸、音频/相机、电话/短信/LTE、Wi-Fi/蓝牙、充电/休眠、首次引导、root 授权及恢复路径，之后才制作并验证 MiFlash 包。保留真实设备身份和安全补丁信息，不把原厂镜像标成 bestOS。

## AOSP 准备进度（2026-10-25）

已取得 Android 10 r47 完整 manifest，并准备 Linux 同步脚本。当前 Mac 约 58 GiB 可用；用户确认 Windows 电脑尚未安装 WSL2 / Ubuntu，完整同步尚未开始。步骤和证据见 [AOSP 源码基底](docs/aosp-base.md)。

## Windows 接手入口

环境脚本、磁盘/内存安排、源码同步和后续助手交接，统一见 [Windows 接手与环境准备](docs/windows-handoff.md)。尚未在目标 Windows 主机执行安装或验证编译。
