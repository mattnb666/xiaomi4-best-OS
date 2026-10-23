# xiaomi 4 bestOS 0.1-dev

为小米 4 LTE 制作的 bestOS 0.1 系统项目。

**当前状态：定制层初始配置，尚未接入完整 Android 10 源码、设备树、内核及专有驱动；没有可刷机产物。**

## 仓库内容与外部文件

本仓库保存当前需求规格、Android 产品配置和资源覆盖，不是完整 Android 源码树。第三方 APK、Google 组件、Magisk、驱动及系统镜像不随本仓库分发。

MT 管理器预装模块需要自行提供匹配的 APK，放到 `vendor/bestos/prebuilt/MTManager/MTManager.apk`；版本与 SHA-256 见 `docs/mt-manager.md`。缺少该文件时不能构建此预装模块。

## 已确定需求

- 系统名称：bestOS 1.0
- Android 版本：10（API 29）
- 系统基底：AOSP 原生 Android 10 源码；在此基础上开发 bestOS 品牌与系统定制。
- 定制深度：桌面、系统界面、自带应用、设置与默认行为全面定制；具体设计待确定，不限定原生外观。
- 目标设备：小米 4 LTE；设备系列代号 cancro，具体硬件版本待实机核对
- 初始开发版本：0.1-dev
- 交付形式：使用小米 MiFlash 刷写的 fastboot 线刷包。
- Root：用户要求 Magisk Alpha（优先 30700），交付匹配 bestOS 构建的已修补 boot.img；当前未获取修补工具或生成镜像。
- 用户没有可用的 Android 10 底包，需要寻找并验证适配基础。
- 社区项目仅作为设备适配代码与硬件兼容性参考，具体代码须核对版本、依赖和许可后移植。

## 当前文件

- `vendor/bestos/config/common.mk`：供 Android 10 产品配置继承的品牌属性。
- `docs/bringup.md`：适配依据、未解决问题和交付条件。
- `docs/product-spec.md`：已确认的硬件、默认竖屏、Wi-Fi/蓝牙/SIM 数据和 MiFlash 交付规格。
- `docs/customization.md`：全面定制的模块划分、待确定设计及交付顺序。
- `vendor/bestos/overlay`：Android 10 资源覆盖，初始竖屏及电话/短信能力配置。

## 接入方式

先验证所选 Android 10 基础源码能为目标设备构建并启动，再将本项目的 `vendor/bestos` 放入源码树相同路径，在实际的设备产品 makefile 中加入：

```make
$(call inherit-product, vendor/bestos/config/common.mk)
```

当前配置增加 bestOS 自有属性和初始资源覆盖，不会自动修改设置应用中的系统名称、开机动画或桌面。保留电话、短信、SIM 蜂窝数据、Wi-Fi 和蓝牙，默认竖屏；通信功能仍需要在选定底层源码后接入并进行实机验证。

不要用本目录直接生成或刷写 system/boot 镜像；尚未建立可用的设备构建目标。
