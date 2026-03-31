---
name: expert-ruoyi
description: 若依(RuoYi)框架开发专家，精通项目搭建、代码生成、问题诊断、架构优化。当用户涉及若依框架开发、SpringBoot后台管理、权限系统、代码生成器、菜单路由配置等问题时自动触发。提供问题诊断、最佳实践和解决方案。
license: MIT
compatibility: 若依框架项目
metadata:
  author: asset-platform
  version: "3.0"
  triggers:
    - "/ruoyi" | "/若依"
    - "若依框架" | "RuoYi" | "权限配置" | "菜单路由"
    - "@PreAuthorize" | "@DataScope" | "sys_menu"
    - "代码生成器" | "代码生成" | "权限校验"
---

# 若依框架开发专家

## 1. 技能概述

### 1.1 核心能力

```yaml
核心能力:
  - 项目搭建: SpringBoot + MyBatis + Shiro/Security
  - 代码生成: CRUD代码自动生成
  - 权限管理: 菜单权限、按钮权限、数据权限
  - 动态路由: 基于sys_menu表的动态路由
  - 最佳实践: 若依框架开发规范

适用场景:
  - 新功能开发遇到权限问题
  - 菜单配置后页面404
  - 代码生成器使用
  - 权限注解不生效
  - 数据范围过滤异常
```

### 1.2 与其他技能协作

| 协作技能 | 协作方式 | 传入数据 | 期望输出 |
|---------|---------|---------|---------|
| **pdd-implement-feature** | Consultation | 若依技术问题 | 解决方案 |
| **pdd-code-reviewer** | Reference | 发现若依问题 | 框架最佳实践 |
| **software-engineer** | Delegation | 代码实现任务 | 符合规范的代码 |

## 2. 快速诊断模式

### 2.1 问题分类索引

```yaml
问题类型:
  路由问题:
    - 页面404
    - 菜单不显示
    - 路由404

  权限问题:
    - 权限注解不生效
    - 按钮不显示
    - 数据范围错误

  代码生成问题:
    - 生成代码报错
    - 生成后需要调整

  配置问题:
    - 数据库配置
    - Redis缓存
    - 会话管理
```

### 2.2 路由问题诊断

```
问题: 点击菜单后页面404

诊断流程:
1. 检查 sys_menu 表配置
   SELECT * FROM sys_menu WHERE menu_name = 'XXX';

2. 检查 component 路径
   - 路径相对于 src/views
   - 文件必须存在

3. 检查 visible 字段
   - '0' = 显示菜单
   - '1' = 隐藏菜单

4. 检查父菜单是否存在
   SELECT * FROM sys_menu WHERE menu_id = parent_id;

5. 检查角色权限分配
   SELECT * FROM sys_role_menu WHERE menu_id = menu_id;
```

### 2.3 权限问题诊断

```
问题: @PreAuthorize 注解不生效

诊断流程:
1. 检查注解是否正确
   @PreAuthorize("@ss.hasPermi('xxx:xxx:xxx')")

2. 检查 sys_menu 表中权限标识符
   - perms 字段必须与注解中一致

3. 检查角色菜单分配
   SELECT * FROM sys_role_menu WHERE menu_id IN
   (SELECT menu_id FROM sys_menu WHERE perms = 'xxx:xxx:xxx');

4. 检查用户角色
   SELECT * FROM sys_user_role WHERE user_id = user_id;

5. 清除Redis缓存
   FLUSHDB
```

## 3. 核心配置规范

### 3.1 菜单配置规范

```sql
-- 目录类型 (M)
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, menu_type, visible, perms, icon)
VALUES ('资产管理', 0, 1, 'asset', NULL, 'M', '0', NULL, 'asset');

-- 菜单类型 (C) - 列表页
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, menu_type, visible, perms, icon)
VALUES ('资产列表', parent_id, 1, 'list', 'asset/index', 'C', '0', 'asset:list:list', 'list');

-- 菜单类型 (C) - 隐藏页面 (新增/编辑/详情)
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, menu_type, visible, perms)
VALUES ('资产新增', parent_id, 10, 'add', 'asset/form', 'C', '1', 'asset:list:add');

-- 按钮类型 (F) - 权限控制
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, menu_type, visible, perms)
VALUES ('资产新增按钮', menu_id, 1, '', '', 'F', '0', 'asset:list:add');
```

### 3.2 权限注解规范

```java
// Controller 层
@RestController
@RequestMapping("/asset/list")
public class AssetListController {

    // 列表查询 - 需要 list 权限
    @PreAuthorize("@ss.hasPermi('asset:list:list')")
    @GetMapping
    public AjaxResult list() { }

    // 新增 - 需要 add 权限
    @PreAuthorize("@ss.hasPermi('asset:list:add')")
    @PostMapping
    public AjaxResult add() { }

    // 修改 - 需要 edit 权限
    @PreAuthorize("@ss.hasPermi('asset:list:edit')")
    @PutMapping
    public AjaxResult edit() { }

    // 删除 - 需要 remove 权限
    @PreAuthorize("@ss.hasPermi('asset:list:remove')")
    @DeleteMapping
    public AjaxResult remove() { }

    // 导出 - 需要 export 权限
    @PreAuthorize("@ss.hasPermi('asset:list:export')")
    @GetMapping("/export")
    public void export() { }
}
```

### 3.3 数据权限规范

```java
// Service 层
public interface IAssetService {

    // 添加 @DataScope 注解
    @DataScope(deptAlias = "d", userAlias = "u")
    List<Asset> selectAssetList(Asset asset);
}

// Mapper XML
<select id="selectAssetList" resultMap="AssetResult">
    SELECT a.*, d.dept_name
    FROM asset a
    LEFT JOIN sys_dept d ON a.dept_id = d.dept_id
    LEFT JOIN sys_user u ON a.create_by = u.user_name
    WHERE a.del_flag = '0'
    ${params.dataScope}
</select>
```

## 4. 代码生成器使用

### 4.1 生成后必须调整项

| 调整项 | 原因 | 优先级 |
|--------|------|--------|
| 添加 @Validated 注解 | 参数校验 | P0 |
| 添加 @DataScope 注解 | 数据权限 | P0 |
| 添加 @Xss 注解 | XSS防护 | P0 |
| 配置 sys_menu 表 | 菜单路由 | P0 |
| 分配角色菜单权限 | 权限生效 | P0 |
| 清除Redis缓存 | 刷新权限缓存 | P0 |

### 4.2 代码调整示例

```java
// 调整前 (生成器默认)
@PostMapping
public AjaxResult add(Asset asset) {
    return AjaxResult.success(assetService.insertAsset(asset));
}

// 调整后 (添加参数校验)
@PreAuthorize("@ss.hasPermi('asset:list:add')")
@Log(title = "资产管理", businessType = BusinessType.INSERT)
@PostMapping
public AjaxResult add(@Validated @RequestBody Asset asset) {
    return AjaxResult.success(assetService.insertAsset(asset));
}

// 实体类添加 XSS 防护
@Excel(name = "资产名称")
@Xss
private String assetName;

// 列表查询添加数据权限
@DataScope(deptAlias = "d", userAlias = "u")
List<Asset> selectAssetList(Asset asset);
```

## 5. 常见问题解决方案

### 5.1 页面404问题

**问题**: 点击菜单后页面404

**排查步骤**:
```sql
-- Step 1: 检查菜单是否存在
SELECT * FROM sys_menu WHERE menu_name LIKE '%XXX%';

-- Step 2: 检查 component 路径是否正确
-- 路径格式: module/path (相对于 src/views)
-- 例如: equity-transfer/apply/index

-- Step 3: 检查文件是否存在
-- src/views/equity-transfer/apply/index.vue

-- Step 4: 检查父菜单
SELECT * FROM sys_menu WHERE menu_id = parent_id;

-- Step 5: 检查角色权限
SELECT * FROM sys_role_menu WHERE menu_id = menu_id;
```

**解决方案**:
1. 确认 sys_menu 表中 component 路径正确
2. 确认 Vue 文件存在于正确位置
3. 确认菜单已分配给用户角色
4. 清除Redis缓存
5. 重新登录

### 5.2 权限注解不生效

**问题**: @PreAuthorize 注解不生效，所有用户都能访问

**排查步骤**:
```sql
-- Step 1: 检查权限标识符是否匹配
SELECT perms FROM sys_menu WHERE menu_name = 'XXX';

-- Step 2: 检查角色菜单分配
SELECT r.role_name, m.menu_name
FROM sys_role_menu rm
JOIN sys_menu m ON rm.menu_id = m.menu_id
WHERE m.perms = 'xxx:xxx:xxx';

-- Step 3: 检查用户角色
SELECT u.user_name, r.role_name
FROM sys_user_role ur
JOIN sys_role r ON ur.role_id = r.role_id
WHERE ur.user_id = user_id;
```

**解决方案**:
1. 确认注解中的权限标识符与 sys_menu.perms 一致
2. 确认角色已分配对应菜单权限
3. 确认用户已分配对应角色
4. 清除Redis缓存
5. 重新登录获取最新权限

### 5.3 数据范围过滤不生效

**问题**: 用户能看到不属于自己部门的数据

**排查步骤**:
```sql
-- Step 1: 检查用户所属部门
SELECT u.user_name, d.dept_name, d.dept_id
FROM sys_user u
JOIN sys_dept d ON u.dept_id = d.dept_id
WHERE u.user_id = user_id;

-- Step 2: 检查数据权限配置
-- 查看 Mapper XML 是否正确配置了 ${params.dataScope}

-- Step 3: 检查 @DataScope 注解
-- 确认 deptAlias 和 userAlias 与 SQL 别名一致
```

**解决方案**:
1. 确认 @DataScope 注解配置正确
2. 确认 Mapper XML 中表别名正确
3. 确认 sys_user 表中 dept_id 正确
4. 重新登录获取新的会话信息

### 5.4 按钮权限不显示

**问题**: 用户有权限但按钮不显示

**排查步骤**:
```javascript
// 检查前端是否有 v-hasPermi 指令
<el-button v-hasPermi="['asset:list:add']">
  新增
</el-button>

// 检查权限标识符是否一致
// 前端: asset:list:add
// 后端: @PreAuthorize("@ss.hasPermi('asset:list:add')")
// 数据库: sys_menu.perms = 'asset:list:add'
```

**解决方案**:
1. 确认前端按钮使用了 v-hasPermi 指令
2. 确认权限标识符完全一致
3. 确认按钮对应的菜单权限已分配
4. 清除浏览器缓存
5. 重新登录

## 6. 最佳实践清单

### 6.1 开发检查清单

```yaml
新增功能检查项:
  - [ ] sys_menu 表配置完整 (目录/菜单/按钮)
  - [ ] component 路径正确
  - [ ] 权限标识符唯一且规范
  - [ ] 角色菜单权限已分配
  - [ ] @PreAuthorize 注解配置正确
  - [ ] @DataScope 注解配置正确 (如需要)
  - [ ] @Validated 参数校验添加
  - [ ] @Xss 文本字段防护添加
  - [ ] @Log 操作日志添加
  - [ ] Redis缓存已清除
  - [ ] 用户重新登录
```

### 6.2 API命名规范

```javascript
// 标准API命名
export function listAsset(query) {
  return request({ url: '/asset/list', method: 'get', params: query });
}

export function getAsset(assetId) {
  return request({ url: '/asset/' + assetId, method: 'get' });
}

export function addAsset(data) {
  return request({ url: '/asset', method: 'post', data });
}

export function updateAsset(data) {
  return request({ url: '/asset', method: 'put', data });
}

export function delAsset(assetId) {
  return request({ url: '/asset/' + assetId, method: 'delete' });
}

export function exportAsset(query) {
  return request({ url: '/asset/export', method: 'get', params: query });
}
```

## 7. Guardrails

### 7.1 必须遵守

- [ ] 所有页面（包括隐藏页）都必须在 sys_menu 表配置
- [ ] 权限标识符必须与 sys_menu.perms 完全一致
- [ ] 数据权限必须配置 ${params.dataScope}
- [ ] @RequestBody 参数必须添加 @Validated 注解
- [ ] 文本字段建议添加 @Xss 注解

### 7.2 避免事项

- ❌ 硬编码权限标识符
- ❌ 跳过菜单配置直接访问页面
- ❌ 前端验证替代后端验证
- ❌ 忘记清除Redis缓存

## 8. 本地开发指南

本项目有特定的开发规范和历史经验，请在提供建议时优先参考：

### 8.1 项目规则文件

| 文件 | 路径 | 内容 |
|------|------|------|
| **项目规则** | `.trae/rules/project_rules.md` | 目录结构、命名规范、开发规范、API命名规范 |
| **经验教训** | `.trae/rules/lessons.md` | 历史问题和解决方案，包含若依框架特定问题 |

### 8.2 本地开发文档

| 文档 | 路径 | 内容 |
|------|------|------|
| **若依框架样式修改方案** | `docs/plans/若依框架样式修改方案.md` | 样式调整、主题配置、品牌一致性 |

### 8.3 历史问题参考

在 `.trae/rules/lessons.md` 中记录了以下若依框架相关问题：

1. **菜单路由配置问题** (2026-03-08)
   - 问题：新增页面404
   - 原因：未在 sys_menu 表配置路由
   - 解决：所有页面（包括隐藏页）都需要配置

2. **API方法命名规范问题** (2026-03-08)
   - 问题：前后端命名不一致
   - 原因：未先定义规范
   - 解决：设计文档先行，代码实现跟随

3. **FP-ZCCZ1-001 Code Review实践** (2026-03-08)
   - 问题：缺少参数校验、XSS防护、数据权限
   - 解决：添加 @Validated、@Xss、@DataScope 注解

### 8.4 项目特定检查项

```yaml
项目特定检查项:
  - [ ] 检查 lessons.md 中是否有相关问题的解决方案
  - [ ] 遵循 project_rules.md 中的命名规范
  - [ ] 参考现有代码的实现模式
  - [ ] 确认数据库配置：mysql6.sqlpub.com:3311/asset_ruoyi
```

## 9. 外部参考文档

- [若依官网](http://ruoyi.vip/)
- [若依文档](http://doc.ruoyi.vip/)
- [RuoYi-Vue GitHub](https://github.com/yangzongzhuan/RuoYi-Vue)
- [RuoYi-Vue Gitee](https://gitee.com/y_project/RuoYi-Vue)

## 10. 版本历史

| 版本 | 日期 | 变更内容 |
|-----|------|---------|
| 3.1 | 2026-03-22 | 添加本地开发指南和文档引用 |
| 3.0 | 2026-03-21 | 标准化结构，添加诊断模式，增强协作指导 |
| 2.0 | 早期 | 完善问题解决方案 |
| 1.0 | 早期 | 初始版本 |
