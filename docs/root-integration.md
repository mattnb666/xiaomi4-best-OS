# Root 集成：KernelSU 条件优先

## 2026-10-25 更新：6.1 可用后优先 KernelSU

- 用户最新选择：若 Linux 6.1 在小米 4 LTE 上适配成功，且 KernelSU 在该设备上验证可用，则以 KernelSU 替换 Magisk Alpha。此条件覆盖此前“必须由 Alpha 修补 boot”的要求。
- KernelSU 与 Magisk 是不同的 root 实现；“KSU 面具”按 KernelSU 及其管理应用理解，不默认同时安装两个 root 框架。
- 小米 4 的目标是 ARM 32 位、非 GKI 设备移植。仅内核版本为 6.1 不代表符合官方 GKI 镜像要求；不得直接刷入通用 android14-6.1 等 boot 镜像。
- 尚未确定可用的 KernelSU 版本或分支。需核实内核端、管理应用、ksud 的 ARM32 和 Android 10 支持，以及所需 hooks、SELinux 和模块挂载支持。
- 若条件满足，构建适配 cancro 的 KernelSU 内核，打包同次 bestOS 构建的 ramdisk 与设备树，生成 MiFlash 使用的 boot.img，并预装匹配管理应用。刷入后应可按应用授权 root；不能只预装管理 APK。
- 必须验证首次启动、恢复出厂后的初始化、重启后的 su 授权与拒绝、模块安装和卸载。现有玩机/游戏模块需逐个检查，不能假设 Magisk 模块完全兼容 KernelSU。
- 当前未满足切换条件；以下 Alpha 方案仅作为历史候选保留，不表示已决定回退或已实现。若 KSU 不适用，记录阻碍后再确定方案。

## 原 Alpha 候选需求与证据边界

- 小米 4 LTE，刷入 bestOS 后即具备 Magisk root 能力。
- 优先使用 Magisk Alpha 版本代码 30700，预装匹配管理应用。
- MiFlash 最终刷入的 boot.img 必须经过 Magisk 修补。
- 用户反馈当前内核只支持 Alpha，此项作为适配线索，尚未经验证；当前 MIUI 内核兼容性不能直接推定新 bestOS 内核兼容性。
- Alpha 发布频道可查到 `e8a58776-alpha 30700`；尚未取得、校验对应 APK。

## 原 Alpha 候选构建和交付流程

1. 先构建并验证 Android 10 / cancro 未修补 boot 镜像，确认 ramdisk、启动布局、内核、分区容量。
2. 获取可信来源的准确 Alpha APK，记录完整版本、签名和 SHA-256；不混用其他分支的同版本代码。
3. 以同一 bestOS 构建生成的 boot.img 为输入，依据目标设备布局完成修补。不得用当前 MIUI 5.x boot 或其他 ROM 的预修补 boot 替代。
4. 按 Magisk 上游指引在目标设备完成修补/验证；记录修补日志与输入输出校验值。若启动布局不支持仅修补 boot，先解决架构适配，不能交付名义上的 patched boot。
5. 将验证通过的修补镜像放入最终 MiFlash 包 `images/boot.img`；在恢复资料中另存未修补的同构建 boot。路径是交付约定，当前文件不存在。
6. 预装匹配版本管理应用，验证清除数据后的首次启动是否需要额外初始化，不能只预装 APK 就宣称已有 root。
7. 验证重启后 Magisk 服务和 su 可用，正常授权后 `su -c id` 返回 uid=0；同时验证启动、通话、短信、蜂窝数据、Wi-Fi、蓝牙与应用更新。

## 权限与现有要求

- 系统具备 root 不等于所有应用自动获准 root；使用选定的 root 管理器逐应用授权，不默认向 MT 或其他应用授予 root。
- 保持 SELinux enforcing 为目标，不为集成 root 默认关闭系统权限检查。
- MT 管理器不可卸载的约束针对普通权限操作；用户主动授予 root 后可以更改系统，此时无法承诺绝对不可删除。
- Google Play 和依赖完整性检查的应用需实测，不承诺 root 环境通过认证，不加入绕过认证的默认配置。

## 当前状态

只有需求和集成流程。尚无 bestOS boot.img、Alpha APK、修补结果或设备测试，不能交付可刷机镜像。

## 来源

- Alpha 发布频道：https://t.me/s/magiskalpha
- Magisk 安装说明：https://github.com/topjohnwu/Magisk/blob/master/docs/install.md
- 启动布局说明：https://topjohnwu.github.io/Magisk/boot

- KernelSU 官方安装说明：https://kernelsu.org/guide/installation.html
- KernelSU 官方源码与支持范围：https://github.com/tiann/KernelSU
