# Windows 接手与环境准备

更新：2026-10-26。目标 Windows 主机：用户提供 8 GB RAM、500 GB 总磁盘容量。当前没有远程访问该电脑；以下脚本未在该电脑运行。Ubuntu 22.04 / WSL2 是准备路线，不代表 Android 10 已验证能在该宿主编译。

## 1. 先检查 Windows

下载或克隆本仓库。在 PowerShell 运行 `setup/windows/check-host.ps1`，查看 Windows 版本、虚拟化、内存、各卷剩余空间和 WSL 版本。脚本只读，不自动安装、分区、清理或关闭其他发行版。若执行策略阻止运行，可以在 PowerShell 逐段粘贴其中的只读命令，不必全局降低执行策略。

按微软官方 WSL 文档，简化安装命令要求 Windows 10 build 19041+ 或 Windows 11。以管理员身份运行：

```powershell
wsl --install -d Ubuntu-22.04
```

按提示重启并在 Ubuntu 创建 Linux 用户。用 `wsl -l -v` 确认 VERSION 为 2。旧版 Windows、虚拟化未开启或安装失败时先解决具体错误，不重装已有发行版，不执行 unregister。

## 2. 安排磁盘与内存

500 GB 是总容量，不是剩余容量。核对实际承载 WSL 虚拟磁盘的 Windows 卷；Linux 中看到的虚拟磁盘容量不等于宿主剩余空间。若系统盘空间不足，应在开始源码同步前把发行版安置到空间充足的卷，迁移方式按实际 WSL 版本核对，不盲目导出/注销。

源码放在 Ubuntu 的 `~/bestos/aosp10`，项目放在 `~/bestos/project`，不用 `/mnt/c` 或 `/mnt/d` 放源码。首次同步预留 200 GiB 为本项目检查门槛，编译还需额外空间，未作 Android 10 占用实测。

8 GB RAM 资源紧张；`setup/windows/wslconfig.example` 提供可选起点：WSL 6 GB、2 CPU、16 GB swap。它不是保证编译成功的配置。合并到现有 `%UserProfile%\.wslconfig` 前保留原配置，检查 swap 所在卷空间。配置影响所有 WSL2；保存各发行版工作后才考虑 `wsl --shutdown`，脚本不会自动执行。同步并发先用 2，未来编译从 1 开始，并根据实际 OOM 调整。

## 3. Ubuntu 安装与预检

Ubuntu 中执行：

```bash
sudo apt update
sudo apt install git
mkdir -p ~/bestos
cd ~/bestos
git clone https://github.com/mattnb666/xiaomi4-best-OS.git project
cd project
bash tools/setup_ubuntu.sh
python3 tools/preflight.py --source-parent "$HOME/bestos" --network
```

若 project 已存在，先检查 `git status`，不要覆盖或清理本地修改。环境脚本仅为 Ubuntu 22.04 安装仓库依赖；不修改全局 Java/Python 链接、不添加未核实 PPA、不下载第三方一键脚本。AOSP 使用所选源码要求的预置工具链；旧宿主库与 Python2 等实际兼容问题在同步后核实，不能假设现代 Ubuntu 自动兼容 Android 10。

预检输出可提供给后续助手；不包含环境变量、令牌或完整 Git 配置。网络检查访问 manifest 和 git-repo 官方地址，不代表 741 个仓库全部可达。失败时排查 DNS、连接或合法可用的镜像，不关闭 TLS 验证。

## 4. 同步源码

预检通过并确认 Windows 实际剩余空间后：

```bash
bash tools/sync_aosp10.sh "$HOME/bestos/aosp10"
```

已有工作区的续传方式、tag 与 manifest 说明见 [AOSP 基底](aosp-base.md)。同步失败不能标记完成；成功后应导出 pinned manifest，并验证 `build/envsetup.sh`、构建系统和工具链项目是否存在。当前没有 cancro lunch 目标，不执行未经适配的编译或刷机命令。

## 5. 搬运本地材料

GitHub 已有代码、文档、manifest、字标与原始素材 ZIP。以下二进制尚未上传成功，换电脑后不能假设 git clone 会带上它们：

- 原厂镜像、系统文件/驱动、boot 组件及 MT APK：本地 `out/github-assets/`；详情、文件名和 SHA-256 见 [附件清单](binary-assets.md)。
- 用 USB、局域网或后续成功发布的 Release 搬运；先核对 SHA-256，再解压到独立材料目录。不要执行原厂包中的刷机程序。
- MT APK 经校验后复制至 `vendor/bestos/prebuilt/MTManager/MTManager.apk`，保持原签名。Google、KSU/Alpha、工具/游戏模块尚未取得或验证。

MiFlash 在 Windows 运行；AOSP 编译在 Linux 环境运行。USB 连接、平台工具、驱动和真实分区检查留到硬件适配阶段；当前不安装未知驱动，不提供可执行刷写脚本。

## 6. 给后续助手的交接

可以直接发送：

> 继续这个仓库的 bestOS 小米 4 LTE 项目。先读 README、docs/windows-handoff.md、docs/aosp-base.md、docs/binary-assets.md 和 docs/kernel-6.1-port.md。检查 Windows/WSL2 环境和本地文件；保留所有现有改动。先完成 AOSP Android 10 源码同步并记录固定版本，再评估 cancro 设备树、6.1 ARM32 内核移植与 KSU 兼容性。尚无编译成功或可刷机镜像，不把原厂 3.4 boot 视为 bestOS，也不宣称素材包是完整开机动画。大附件上传仍未完成。根据实际测试更新文档和 GitHub。

阶段顺序：宿主预检 → 依赖 → 源码同步 → 设备配置/驱动与内核 → 最小 Android 启动 → bestOS 定制/Root → 硬件回归 → MiFlash 包与恢复验证。

## 验证边界与来源

目前只在 Mac 完成 Bash 语法检查、Python 预检的拒绝路径检查和文档链接检查。PowerShell、Ubuntu apt 安装、repo 全量同步和编译均未在目标机验证。

- https://learn.microsoft.com/windows/wsl/install
- https://learn.microsoft.com/windows/wsl/wsl-config
- https://source.android.com/docs/setup/start/requirements （当前版资源要求不可直接当作 Android 10 实测值）
