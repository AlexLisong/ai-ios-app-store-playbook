# 用 AI 把 iOS 应用提交到 App Store

这是一份可以直接复用的实践手册：从确定产品范围、用 AI 开发原生 iPhone 应用，到真机验证、签名上传、填写商店资料，最后确认已经提交 Apple 审核。

[English](README.md) · [可复制的 AI 提示词](docs/09-ai-workflow.md) · [发布清单](templates/release-plan.md) · [故障排查](docs/07-troubleshooting.md)

经验来自两类实际开发流程：实时听力辅助应用，以及录音、回听、词汇学习应用。文档已做匿名化；不包含原账户身份、联系方式、设备标识、证书、密钥、录音、基础设施信息或账户页面截图。

## 先记住这一点

**上传成功 ≠ 已提交审核 ≠ 审核通过 ≠ 已经上架。**

Xcode 可以显示 Uploaded，但 App Store Connect 仍可能缺少截图、隐私标签或地区设置。点击“添加以供审核”后，也可能还需要进入审核提交页面，执行最后的提交操作。必须重新打开状态页面，以实际状态为准。

## 从这里开始

1. 把[发布计划模板](templates/release-plan.md)复制到私有工作目录，写清产品、语言、收费、地区、隐私和授权范围。
2. 把[中文启动提示词](docs/09-ai-workflow.md)交给 AI，让它先读代码、建立验收标准，再完成开发和测试。
3. 默认功能尽量完整可用。界面中英文切换，不应偷偷改变翻译方向或语音播放语言。
4. 在模拟器检查布局，在真机检查 Apple 模型、权限、录音和音频路线。模拟器里的演示成功，不能证明真实麦克风工作正常。
5. 准备图标、真正的应用截图、中英文商店资料、隐私政策、支持页面和审核说明。
6. 在 Xcode 登录正确的开发者账户，选择正确 Team，优先使用自动签名，通过 Organizer 上传。
7. 在 App Store Connect 选择处理完成的 build，补齐所有必填项，提交审核，保存[发布回执](templates/release-receipt.md)。

示例流程采用“免费、无广告、无内购、中英文界面、仅加拿大和美国”。这些是产品选择，不是 Apple 对所有应用的要求。

## 每一步看什么

| 步骤 | 文档 | 关键判断 |
|---|---|---|
| 产品和架构 | [01](docs/01-product-and-architecture.md) | 本机功能与云端功能分开，演示与实时功能分开 |
| Xcode 与真机 | [02](docs/02-native-build-and-device.md) | 编译、安装、启动、真实功能分别验证 |
| 隐私和 Azure | [03](docs/03-privacy-and-cloud.md) | 自带密钥也可能涉及第三方数据收集与费用 |
| 截图和商店资料 | [04](docs/04-store-assets-and-listing.md) | 截图尺寸正确，内容来自实际应用，中英文一致 |
| 上传和提交 | [05](docs/05-upload-and-submit.md) | 处理完成、选择 build、最后提交、核实状态 |
| 支持网站 | [06](docs/06-support-site.md) | 复用现有域名，保留回滚，不影响其他站点 |
| 排错 | [07](docs/07-troubleshooting.md) | 锁屏、证书、浏览器上传权限等常见阻塞 |
| 验证边界 | [08](docs/08-evidence-and-lessons.md) | 清楚记录已验证和未验证，不夸大完成程度 |

## 最有价值的经验

- **先用 Xcode 自动签名。** 浏览器下载证书被组织策略阻止时，不应绕过策略。正确登录 Xcode 后，受支持的托管签名流程可能已经足够。
- **锁屏是常见真机阻塞。** 用户需要解锁、点“信任”、输入手机密码；测试过程中保持手机可用。安装完成不代表启动成功。
- **截图最后一公里很容易卡住。** 使用正确尺寸的模拟器截取原图。示例采用 1320 × 2868 PNG。浏览器扩展上传本地文件可能需要“Allow access to file URLs”；启用后重新加载上传页，确认仍是同一账户和应用。
- **可选 Azure 也必须讲清楚。** 默认本机不代表所有功能都不出设备。用户启用 Azure 后，要说明发送什么、发给谁、如何停止、可能的保留及费用。
- **费用分开说。** Apple 本机模型没有按调用计费的 LLM token 账单，但开发者计划、硬件、网站和可选 Azure 服务可能有费用。免费应用不等于所有运行成本为零。
- **应用包根目录不要误放 `Resources/` 文件夹。** 实际流程中触发过 CFBundle 将 iOS 包误识别为旧式 macOS 包的情况；改用明确的资源目录名，并检查最终构建产物。
- **录音与播放需要明确生命周期。** 回听或发音先停止并保存录音；实时翻译的音频会话则需要单独设计，防止 TTS 打断录音或被麦克风反复识别。
- **审核联系人不是公开页面内容。** 私人电话等只填到 Apple 的私有审核字段。公共模板使用虚构占位符。

## 检查这个仓库

```sh
python3 scripts/check_repo.py
python3 -m unittest discover -s tests -v
```

检查自己的图标、截图和 `.app`：

```sh
python3 scripts/check_images.py --kind icon /path/to/AppIcon.png
python3 scripts/check_images.py --kind screenshot /path/to/screenshots/*.png
python3 scripts/preflight.py /path/to/ExampleApp.app
```

这些工具只做本地检查，不登录账户、不读取钥匙串、不签名、不上传，也不会替你判断法律身份或保证审核通过。

经验整理于 2026 年 9 月。Apple 的 SDK 要求、截图规格、页面按钮和政策会变化；每次发布都应重新核对[官方资料](docs/sources.md)。详细操作文档以英文为主，关键流程、提示词和模板附中文说明。
