# AOSP Android 10 源码基底

更新日期：2026-10-25。

## 本次实际完成

- 从用户提供的 GitHub 官方镜像取得完整 `android-10.0.0_r47/default.xml`，本地位于 `sources/aosp-manifest/default.xml`。
- XML 解析通过，共 741 个 project，default revision 为 `refs/tags/android-10.0.0_r47`。检查记录在同目录 inspection.json。
- r47 暂作为源码准备基线，不表示最新 Android 10 安全版本或已匹配 cancro 的最终版本。
- 编写 `tools/sync_aosp10.sh`，供 Linux x86_64 / Ubuntu WSL2 同步使用。仅做了 shell 语法检查，未执行完整同步。
- 官方 repo 启动器已下载到临时目录，但尚未安装或进行 GPG 签名验证；不将其当作已配置完成的工具。

**未完成：741 个项目下载、完整源码检出、设备树接入、6.1 内核移植、系统编译和实机启动。manifest 文件不是底包镜像。**

旧 default.xml.partial 为此前失败记录，不可用于同步。GitHub manifest 中 remote fetch 为相对路径 `..`；不能简单把初始化 URL 改成 GitHub 后就认为所有项目都能同步。脚本仍使用 AOSP 官方 manifest 地址。

## 当前阻碍

当前 Mac 可用空间检查约 58 GiB，未启动全量同步以免磁盘耗尽。用户再次确认 Windows 电脑（8 GB RAM / 500 GB 总容量）尚未安装 Ubuntu / WSL2；该电脑当前无法由本会话直接操作。官方 Git 源和 raw GitHub HTTP 本次下载超时，完整 manifest 经 GitHub 连接器取得，不表示 Linux 主机能够访问所有源码仓库。

## Windows 环境准备

在目标 Windows 电脑的管理员 PowerShell 中运行：

```powershell
wsl --install -d Ubuntu-22.04
```

按 Windows 提示重启，打开 Ubuntu 完成 Linux 用户初始化，再用 `wsl -l -v` 确认发行版运行于 WSL 2。若 Windows 版本不支持该命令，先按微软 WSL 文档配置；本项目尚未检查那台电脑的 Windows 版本或虚拟化状态。

Ubuntu 中先准备源码同步工具：

```bash
sudo apt update
sudo apt install git curl ca-certificates python3 repo
```

此处仅准备下载工具，不代表已配齐 Android 10 编译依赖。具体编译依赖与旧版工具链需在源码就绪后核验。8 GB 内存下先限制同步并发为 2；编译并发、交换空间及内存不足问题另行验证，不承诺构建性能。

把此项目复制或克隆到 Ubuntu 的 Linux 文件系统，进入项目目录后执行：

```bash
bash tools/sync_aosp10.sh "$HOME/bestos/aosp10"
```

不要把源码放在 `/mnt/c` 等 Windows 挂载目录。运行前核对 Linux 文件系统及其宿主磁盘实际剩余空间；脚本的 200 GiB 是本项目保守的首次同步预留门槛，并非 Android 10 官方精确需求，编译还需额外空间。

如果 repo sync 中断，检查报错后进入源码目录继续：

```bash
repo sync -c -j2 --no-clone-bundle --no-tags --fail-fast
repo manifest -r -o bestos-aosp10-pinned.xml
```

同步成功后保存固定提交清单，再加入经过验证的 cancro 设备配置、vendor 依赖、内核和 bestOS 定制。当前没有可用的 `lunch bestos_cancro` 目标，不能把通用 AOSP 镜像用于 MiFlash。

## 来源

- AOSP manifest：https://android.googlesource.com/platform/manifest
- GitHub manifest 镜像：https://github.com/aosp-mirror/platform_manifest
- AOSP 环境说明：https://source.android.com/docs/setup/start/requirements （页面面向当前版本，其资源数字不能直接作为 Android 10 实测需求）
- WSL 安装说明：https://learn.microsoft.com/windows/wsl/install
