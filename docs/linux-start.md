# 在另一台 Linux 电脑继续 bestOS

更新：2026-10-28。当前准备目标是 Ubuntu 22.04 x86_64（原生或 WSL2）。其他发行版安装器会停止，避免错误安装依赖。宿主系统版本与手机 Android 10 / 目标 Linux 6.1 内核是不同概念。

## 从新电脑开始

Ubuntu 终端执行：

```bash
sudo apt update
sudo apt install git
mkdir -p ~/bestos
cd ~/bestos
git clone https://github.com/mattnb666/xiaomi4-best-OS.git project
cd project
bash start-bestos.sh all
```

已有 project 时进入它，检查 `git status` 并保留本地修改，再用 `git pull --ff-only` 更新。不要重复覆盖已有目录。

`all` 自动安装基础依赖、检查环境和网络、初始化指定 AOSP tag 并同步源码。sudo 可能要求输入本机密码。默认源码目录 `~/bestos/aosp10`，可通过第二参数指定另一处 Linux 文件系统目录：

```bash
bash start-bestos.sh all /path/to/linux-disk/aosp10
```

这是环境与源码准备入口，不是已完成的 ROM 自动编译器。同步成功只说明该阶段完成；目前没有验证可用的 cancro 设备树、6.1 内核或 lunch 目标，因此不会执行虚构的编译目标。

## 分阶段、日志与恢复

```bash
bash start-bestos.sh prepare
bash start-bestos.sh check
bash start-bestos.sh sync
```

日志在项目 `out/environment/`，默认不提交。`prepare` 可重复执行 apt 安装；`sync` 可恢复本工具创建且 source/tag 匹配的工作区，未经管理的已有 .repo、修改后的来源或 local manifests 会停止供检查。不使用 reset/clean/force-sync，不清理用户文件。repo init 中断时先人工检查，不自动删目录重来。

同步需至少 200 GiB 剩余空间，这是项目的规划门槛而非官方精确需求；编译还需要额外空间。预检不自动创建 swap、调整分区、关 TLS 或更改全局 Python/Java。Ubuntu 22.04 与 Android 10 旧预置工具的实际兼容性仍待完整源码测试。

## 最新电脑配置

用户最新报告 A8 5600 / FM2、DDR3 4 GB、500 GB 机械硬盘；完整 CPU 型号待核对。这替代此前 8 GB 内存的准备假设。该电脑用于代码编辑、材料处理和 Windows MiFlash；不推荐用它完整编译 AOSP。不要使用旧的 WSL 6 GB 内存示例。可在资源更充足的 Linux 主机运行相同脚本；不会自动购买服务器或启用付费构建。

## 还需的材料与配置

- 仓库：Android 10 r47 manifest（741 个项目）、bestOS 初始配置、文档、字标。
- 尚未下载完成：完整 AOSP。tag 为准备基线，未宣称已适配手机。
- 尚未上传成功：原厂镜像/驱动、boot 组件和 MT APK。搬运与哈希见 [附件状态](binary-assets.md)，不会对不存在的 Release 链接发起假下载。
- 尚待确定：小米 4 LTE 板号/分区、设备树、合法 vendor 依赖、Linux 6.1 ARM32 移植和工具链、KSU 版本兼容性。
- 尚未实现：完整桌面/设置/引导、Google 集成、模块安装与最终 MiFlash 包。现有要求以 README 和专题文档为准。

## 给新电脑上的助手

> 继续制作 bestOS。请先读 README.md、docs/linux-start.md、docs/product-spec.md、docs/binary-assets.md、docs/kernel-6.1-port.md 和 docs/root-integration.md。检查当前主机、日志及已有源码，保留所有本地修改。用 start-bestos.sh 分阶段准备环境和同步；不能把准备完成当作编译成功。先完成 cancro 设备适配再编译，6.1 与 KSU 尚未经实机验证。更新证据和 GitHub，不执行未经核验的刷机步骤。

## 验证情况

入口、依赖与同步脚本通过 Bash 语法检查；入口帮助、非法参数及 macOS 拒绝路径已测试。目标 Ubuntu 上的 apt 安装、完整下载、断点续传和编译尚未实测。
