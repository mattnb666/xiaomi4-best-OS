# 小米 4 LTE / Linux 6.1 移植目标

用户于 2026-10-25 要求编译 Linux 6.1 系列内核。此目标是替换底层内核的设备移植，不只是修改版本字符串。Android 用户空间仍以 AOSP Android 10 为目标。

## 已有证据

- 原厂包提取内核为 3.4.0-g6231d51，设备树数据已提取，但尚无对应可编译源码。
- Linux v6.1 上游文件树包含 `arch/arm/boot/dts/qcom-msm8974.dtsi`、`qcom-msm8974pro.dtsi` 与 `arch/arm/configs/qcom_defconfig`。
- 上游同平台设备文件包括 Nexus 5、Fairphone 2 等；这些设备的引脚、面板和电源配置不能直接用于小米 4。
- 当前检查尚未确立可用于小米 4 LTE 的 6.1 DTS、defconfig 或完整补丁集，不生成声称可刷入的 boot。

## 移植工作

1. 确定实际 LTE 板号和硬件组合，取得合法来源的小米 4 内核源码和板级配置，参考原厂 DT 数据。
2. 在 6.1 中完成 ARM 32 位启动、内存、电源、时钟、存储和 USB 调试通道，先取得启动日志。
3. 逐项适配屏幕、触控、按键、充电、传感器及休眠；不能用其他 MSM8974 手机的 DTS 直接替代。
4. 验证 Android 10 所需 Binder、共享内存、SELinux、cgroup 等配置，以及用户空间对新内核接口的兼容处理。
5. 选择并验证 GPU 用户态/内核驱动组合、相机管线、音频及 modem/RIL；原厂 3.4 驱动接口和旧 HAL 不保证可直接用于 6.1。
6. 基础系统和硬件通过后优先验证 KernelSU 的 ARM32 / 非 GKI 兼容性；验证通过则替换 Alpha，构建集成 KSU 的 boot、检查容量及制作 MiFlash 包。内核版本达到 6.1 不自动满足 KSU 条件，详见 `root-integration.md`。

## 验收层次

- 编译通过：仅证明选定源码和工具链能生成产物。
- 内核启动：设备能执行内核并取得日志。
- Android 启动：能挂载数据并运行系统服务。
- 整机可用：显示、触摸、相机、通话、短信、LTE、Wi-Fi、蓝牙等逐项通过。

不得把第一层结果当作第四层结果。当前尚未下载完整 6.1 源码、准备 Linux 交叉编译环境或验证以上任一层。

## 来源

- Linux v6.1 平台设备树：https://github.com/torvalds/linux/blob/v6.1/arch/arm/boot/dts/qcom-msm8974.dtsi
- Linux v6.1 Qualcomm ARM 配置：https://github.com/torvalds/linux/blob/v6.1/arch/arm/configs/qcom_defconfig

具体 6.1.x 稳定版本和工具链尚未选定，需要结合移植补丁确定；v6.1 仅用于上游能力核查。
