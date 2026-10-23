# Magisk Alpha root 集成

## 用户需求与证据边界

- 小米 4 LTE，刷入 bestOS 后即具备 Magisk root 能力。
- 优先使用 Magisk Alpha 版本代码 30700，预装匹配管理应用。
- MiFlash 最终刷入的 boot.img 必须经过 Magisk 修补。
- 用户反馈当前内核只支持 Alpha，此项作为适配线索，尚未经验证；当前 MIUI 内核兼容性不能直接推定新 bestOS 内核兼容性。
- Alpha 发布频道可查到 `e8a58776-alpha 30700`；尚未取得、校验对应 APK。

## 构建和交付流程

1. 先构建并验证 Android 10 / cancro 未修补 boot 镜像，确认 ramdisk、启动布局、内核、分区容量。
2. 获取可信来源的准确 Alpha APK，记录完整版本、签名和 SHA-256；不混用其他分支的同版本代码。
3. 以同一 bestOS 构建生成的 boot.img 为输入，依据目标设备布局完成修补。不得用当前 MIUI 5.x boot 或其他 ROM 的预修补 boot 替代。
4. 按 Magisk 上游指引在目标设备完成修补/验证；记录修补日志与输入输出校验值。若启动布局不支持仅修补 boot，先解决架构适配，不能交付名义上的 patched boot。
5. 将验证通过的修补镜像放入最终 MiFlash 包 `images/boot.img`；在恢复资料中另存未修补的同构建 boot。路径是交付约定，当前文件不存在。
6. 预装匹配版本管理应用，验证清除数据后的首次启动是否需要额外初始化，不能只预装 APK 就宣称已有 root。
7. 验证重启后 Magisk 服务和 su 可用，正常授权后 `su -c id` 返回 uid=0；同时验证启动、通话、短信、蜂窝数据、Wi-Fi、蓝牙与应用更新。

## 权限与现有要求

- 系统具备 root 不等于所有应用自动获准 root；使用 Magisk 逐应用授权，不默认向 MT 或其他应用授予 root。
- 保持 SELinux enforcing 为目标，不为集成 root 默认关闭系统权限检查。
- MT 管理器不可卸载的约束针对普通权限操作；用户主动授予 root 后可以更改系统，此时无法承诺绝对不可删除。
- Google Play 和依赖完整性检查的应用需实测，不承诺 root 环境通过认证，不加入绕过认证的默认配置。

## 当前状态

只有需求和集成流程。尚无 bestOS boot.img、Alpha APK、修补结果或设备测试，不能交付可刷机镜像。

## 来源

- Alpha 发布频道：https://t.me/s/magiskalpha
- Magisk 安装说明：https://github.com/topjohnwu/Magisk/blob/master/docs/install.md
- 启动布局说明：https://topjohnwu.github.io/Magisk/boot
