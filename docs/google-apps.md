# Google 服务与应用集成需求

## 用户要求

保留 bestOS 独立设计和基础应用，额外加入 Google 全家桶（明确包含 Play 商店）。不以 Google 电话、短信、图库等替换 bestOS 基础软件。

首次开机不要求 Google 登录或在线激活。仅在设置中提供可选 Google 账号添加入口，用于服务登录及同步，不作为 bestOS 设备账号；暂不提供 bestOS 系统账号。详见 `accounts-and-setup.md`。

## 初步清单

- 不预装 Google Files 或其他额外文件管理器；文件管理使用用户提供的 MT 管理器共存版。

- 核心：Google Play 商店、Google Play 服务，以及所选合法来源组件包所需的账号和服务框架依赖。
- 常用应用候选：Google 搜索、Chrome、Gmail、Maps、YouTube、Drive、Photos、Calendar、Keep。
- 候选清单用于明确“全家桶”的范围，并非宣称这些应用的当前最新版均支持 Android 10 或目标 CPU 架构。逐项确认兼容版本、来源、依赖及更新支持后再接入。
- Google 闭源应用保留其自身界面，不作为可任意修改源码的 bestOS 自研应用。

## 集成与验证

- 先固定 Android 10 和 cancro 构建，再核对 ABI、组件版本、权限白名单、签名及安装分区。
- GMS 不属于 AOSP 开源源码。预装和再分发须核对来源及适用许可，不能将下载到 APK 视为自动获得分发授权。
- 自定义 ROM 不自动获得 Play Protect 认证；不承诺所有商店应用、支付或完整性检查均可用。
- 实测离线首次启动直接完成本地引导、设置中添加/移除账号、商店下载/更新、通知与同步；基础本地应用无需 Google 登录即可使用。
- 系统 OTA 保持不接入；Google 应用与服务的更新单独处理。
- 保留系统内容 3 GB 目标，但加入 Google 组件后的大小尚未知。分别测量展开镜像、分区容量、首次启动后数据占用和下载包大小。若超出，报告实际结果后确定预装取舍，不静默删减用户要求。

## 当前状态与来源

仅记录需求，尚未下载、预装或测试 Google 组件。

- Google GMS 说明：https://www.android.com/intl/en_uk/gms/
- Play Protect 认证说明：https://support.google.com/android/answer/7165974?hl=en
