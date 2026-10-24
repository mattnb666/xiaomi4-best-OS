# 原厂线刷包提取报告

已从 V10.1.1.0.MXDCNFI 中国稳定版 Fastboot 包提取。未执行任何刷机脚本或镜像中的程序。

## 文件位置

所有二进制产物在本地 `downloads/stock-rom/` 下，该目录被 Git 忽略，不自动上传仓库。

- `extracted/`：原厂包完整解出内容，包含 boot/system/recovery、基带固件、分区表和刷机脚本。
- `analysis/system.raw.img`：展开的 EXT 文件系统镜像，1,342,177,280 字节。
- `analysis/system-files/`：系统普通文件，按原目录保存。
- `analysis/system-file-manifest.json`：2,673 个文件或链接条目；2,485 个普通文件有 SHA-256。符号链接只记录目标，不在主机上创建或跟随；记录原始 mode、uid、gid，不在 macOS 上应用这些权限。
- `analysis/driver-candidates.json`：按路径关键词分类的适配候选清单，不是已验证的最小驱动依赖集。
- `analysis/boot/`：kernel、解压内核、ramdisk.gz/cpio、普通 ramdisk 文件及 dt.img。
- `analysis/boot-inspection.json`：启动参数、分量大小/哈希和 ramdisk 条目。
- `analysis/image-manifest.json`：原厂镜像及配置的 SHA-256 清单。

## 观察结果

- build.prop 的 Android 版本为 **6.0.1**（下载文件名仅写 6.0）。
- 内核字符串为 **Linux 3.4.0-g6231d51**，编译器 GCC 4.9.x-google，构建时间 2018-10-10。
- 默认 ro.product.model 为 **MI 3W**；device=cancro，board=MSM8974。该共享包的默认型号不能直接作为小米 4 LTE 最终身份配置。
- 原厂 flash_all.bat 检查 product=MSM8974，拒绝 board_version=4.4 和 5.x，并会刷写分区表、引导固件及用户数据。不能直接复用为 bestOS 刷机脚本。
- boot 使用 2048 字节页；提取 kernel 10,855,751 字节、ramdisk 1,373,153 字节、DT 分量 2,512,896 字节。此镜像观察到命令行起始偏移 60，使用针对该原包的解析，不宣称通用现代 boot 解析器。

## 适配材料候选

| 分类 | 条目数（可能交叉） | 示例 |
| --- | ---: | --- |
| 相机 | 266 | camera.msm8974.so、mm-qcamera-daemon、chromatix 相关库 |
| 图形 | 18 | gralloc.msm8974.so、hwcomposer.msm8974.so、EGL/GLES 库 |
| 音频 | 177 | audio.primary.msm8974.so、ACDB 与 mixer 配置 |
| 通信 | 27 | rild、QMI、APN 配置 |
| Wi-Fi/蓝牙 | 70 | wcnss_service、无线配置及相关库 |
| 传感器/电源 | 41 | 传感器、电源与温控相关文件 |

## 验证与限制

归档 gzip 完整性检查已通过；系统使用 dissect.extfs 3.14 只读解析，没有挂载文件系统。普通文件保存哈希，镜像单独计算 SHA-256。此为普通本地工具静态证据，不是 REA 引擎输出。

驱动候选包含相关配置、工具及库，并不表示每项都是独立驱动，也尚未验证 Android 10 兼容性。屏幕、触摸等内核驱动可能编入内核，提取二进制不能恢复对应 C 源码。下一步需要匹配内核源码、设备树、HAL 接口和 ELF 依赖；实际板号与硬件组合仍待实机核对。
