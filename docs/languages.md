# bestOS 全局语言

## 已确认要求

首次开机引导（用户称激活选项）和设置中的语言选择都只显示以下四项，单选后应用到系统全局：

| 固定显示名称 | Locale | 说明 |
| --- | --- | --- |
| 中文简体 | zh-CN | 简体中文，默认选择（暂定） |
| 中文繁體（香港） | zh-HK | 繁体中文，香港地区用语 |
| 中文繁體（台灣） | zh-TW | 繁体中文，台湾地区用语 |
| English | en-US | 英文，暂用美国地区格式 |

使用各语言自身名称，以便切换后仍能识别。香港与台湾分别维护文本资源和格式，不只做机械繁简转换。

用户后续要求：地区选择独立，只有中国大陆、香港、美国，见 `regions.md`。本表的语言 Locale 标签用于匹配翻译，不代表地区选择列表；台湾繁体语言继续保留。现有 locale 配置尚未实现语言与系统地区的独立处理。

## 已写配置

- common.mk 的 PRODUCT_LOCALES 设置为四个地区；完整产品接入时必须检查继承链最终值，避免其他产品配置追加语言。
- framework supported_locales 资源覆盖为四项。
- 以上未编译，仅通过 XML 静态检查；不代表已完成定制的四行单选 UI。

## 待实现与验收

- 定制首次引导与 Settings 使用同一份四项语言定义，直接列出四行，不进入额外地区列表，不提供添加其他语言入口。
- 选择后通过系统配置服务持久更新全局 LocaleList；不能只修改当前 Activity。以选中语言为主，确保重启仍保留。
- Launcher、SystemUI、Settings 及 bestOS 自带应用提供对应翻译；验证日期、数字、字体字形和文本布局。
- 不用 SIM 或网络推断自动覆盖用户选择；语言选择不改变 SIM/APN 或强制修改时区。
- Google、MT、Magisk 等第三方 APK 保持原始签名，由它们的翻译资源和应用内设置决定是否跟随；不保证所有界面都具有港繁/台繁区分。
- 系统语言四项限制不等于限制输入法键盘语言，也不更改第三方应用自身语言菜单。

## 来源

AOSP Android 10 supported_locales 定义：
https://raw.githubusercontent.com/aosp-mirror/platform_frameworks_base/android-10.0.0_r47/core/res/res/values/locale_config.xml
