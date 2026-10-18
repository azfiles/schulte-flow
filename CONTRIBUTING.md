# 贡献与扩展

经典棋盘逻辑在 `GameSession.java`，原生界面在 `MainActivity.java`；Godot 规则在 `godot/scripts/round.gd`，关卡在 `levels.gd`，界面和反馈在 `main.gd`。

修改规则后运行相应测试；修改 UI 后手动运行对应完整 APK 工作流，检查模拟器报告与实际画面。新增文案需扩展字体子集。先保持包名、存档结构、版本号和演示签名兼容，再逐步增加统计、训练模式、无障碍与本地数据导出。

已发布文件保持不可变：新功能提高 Android versionCode/versionName 及构建文件名，并创建新标签，不能覆盖旧 APK 或验证记录。体验发布不能代替真机音效、触感、性能与续航验证。

`Preserve published releases` 只用于一次性迁移已有文件和校验，不是新代码的构建入口。
