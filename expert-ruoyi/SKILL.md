---
name: expert-ruoyi
description: RuoYi Framework Development Expert, proficient in project setup, code generation, problem diagnosis, and architecture optimization. Automatically triggered when users encounter RuoYi framework development, SpringBoot backend management, permission systems, code generators, menu routing configuration, and other related issues. Provides problem diagnosis, best practices, and solutions. 支持中文触发：若依框架开发、SpringBoot后台管理、权限系统、代码生成器、菜单路由配置、若依、RuoYi。
license: MIT
compatibility: RuoYi Framework Projects
metadata:
  author: neuqik@hotmail.com
  version: "3.0"
  triggers:
    - "/ruoyi" | "/若依"
    - "若依框架" | "RuoYi" | "权限配置" | "菜单路由"
    - "@PreAuthorize" | "@DataScope" | "sys_menu"
    - "代码生成器" | "代码生成" | "权限校验"
---

# RuoYi Framework Development Expert

## 1. Skill Overview

### 1.1 Core Capabilities

```yaml
Core Capabilities:
  - Project Setup: SpringBoot + MyBatis + Shiro/Security
  - Code Generation: Automatic CRUD code generation
  - Permission Management: Menu permissions, button permissions, data permissions
  - Dynamic Routing: Dynamic routing based on sys_menu table
  - Best Practices: RuoYi framework development standards

Applicable Scenarios:
  - Permission issues during new feature development
  - Page 404 after menu configuration
  - Code generator usage
  - Permission annotations not working
  - Data scope filtering exceptions
```

### 1.2 Collaboration with Other Skills

| Collaborating Skill | Collaboration Method | Input Data | Expected Output |
|---------|---------|---------|---------|
| **pdd-implement-feature** | Consultation | RuoYi technical issues | Solutions |
| **pdd-code-reviewer** | Reference | Discovered RuoYi issues | Framework best practices |
| **software-engineer** | Delegation | Code implementation tasks | Standards-compliant code |

## 2. Quick Diagnosis Mode

### 2.1 Problem Classification Index

```yaml
Problem Types:
  Routing Issues:
    - Page 404
    - Menu not displaying
    - Route 404

  Permission Issues:
    - Permission annotations not working
    - Buttons not displaying
    - Data scope errors

  Code Generation Issues:
    - Generated code errors
    - Adjustments needed after generation

  Configuration Issues:
    - Database configuration
    - Redis cache
    - Session management
```

### 2.2 Routing Issue Diagnosis

```
Problem: Page 404 after clicking menu

Diagnosis Process:
1. Check sys_menu table configuration
   SELECT * FROM sys_menu WHERE menu_name = 'XXX';

2. Check component path
   - Path relative to src/views
   - File must exist

3. Check visible field
   - '0' = Show menu
   - '1' = Hide menu

4. Check if parent menu exists
   SELECT * FROM sys_menu WHERE menu_id = parent_id;

5. Check role permission assignment
   SELECT * FROM sys_role_menu WHERE menu_id = menu_id;
```

### 2.3 Permission Issue Diagnosis

```
Problem: @PreAuthorize annotation not working

Diagnosis Process:
1. Check if annotation is correct
   @PreAuthorize("@ss.hasPermi('xxx:xxx:xxx')")

2. Check permission identifier in sys_menu table
   - perms field must match the annotation

3. Check role menu assignment
   SELECT * FROM sys_role_menu WHERE menu_id IN
   (SELECT menu_id FROM sys_menu WHERE perms = 'xxx:xxx:xxx');

4. Check user role
   SELECT * FROM sys_user_role WHERE user_id = user_id;

5. Clear Redis cache
   FLUSHDB
```

## 3. Core Configuration Standards

### 3.1 Menu Configuration Standards

```sql
-- Directory Type (M)
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, menu_type, visible, perms, icon)
VALUES ('Asset Management', 0, 1, 'asset', NULL, 'M', '0', NULL, 'asset');

-- Menu Type (C) - List Page
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, menu_type, visible, perms, icon)
VALUES ('Asset List', parent_id, 1, 'list', 'asset/index', 'C', '0', 'asset:list:list', 'list');

-- Menu Type (C) - Hidden Page (Add/Edit/Detail)
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, menu_type, visible, perms)
VALUES ('Asset Add', parent_id, 10, 'add', 'asset/form', 'C', '1', 'asset:list:add');

-- Button Type (F) - Permission Control
INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, menu_type, visible, perms)
VALUES ('Asset Add Button', menu_id, 1, '', '', 'F', '0', 'asset:list:add');
```

### 3.2 Permission Annotation Standards

```java
// Controller Layer
@RestController
@RequestMapping("/asset/list")
public class AssetListController {

    // List Query - Requires list permission
    @PreAuthorize("@ss.hasPermi('asset:list:list')")
    @GetMapping
    public AjaxResult list() { }

    // Add - Requires add permission
    @PreAuthorize("@ss.hasPermi('asset:list:add')")
    @PostMapping
    public AjaxResult add() { }

    // Edit - Requires edit permission
    @PreAuthorize("@ss.hasPermi('asset:list:edit')")
    @PutMapping
    public AjaxResult edit() { }

    // Delete - Requires remove permission
    @PreAuthorize("@ss.hasPermi('asset:list:remove')")
    @DeleteMapping
    public AjaxResult remove() { }

    // Export - Requires export permission
    @PreAuthorize("@ss.hasPermi('asset:list:export')")
    @GetMapping("/export")
    public void export() { }
}
```

### 3.3 Data Permission Standards

```java
// Service Layer
public interface IAssetService {

    // Add @DataScope annotation
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

## 4. Code Generator Usage

### 4.1 Required Adjustments After Generation

| Adjustment Item | Reason | Priority |
|--------|------|--------|
| Add @Validated annotation | Parameter validation | P0 |
| Add @DataScope annotation | Data permissions | P0 |
| Add @Xss annotation | XSS protection | P0 |
| Configure sys_menu table | Menu routing | P0 |
| Assign role menu permissions | Permissions take effect | P0 |
| Clear Redis cache | Refresh permission cache | P0 |

### 4.2 Code Adjustment Examples

```java
// Before Adjustment (Generator Default)
@PostMapping
public AjaxResult add(Asset asset) {
    return AjaxResult.success(assetService.insertAsset(asset));
}

// After Adjustment (Add Parameter Validation)
@PreAuthorize("@ss.hasPermi('asset:list:add')")
@Log(title = "Asset Management", businessType = BusinessType.INSERT)
@PostMapping
public AjaxResult add(@Validated @RequestBody Asset asset) {
    return AjaxResult.success(assetService.insertAsset(asset));
}

// Entity Class Add XSS Protection
@Excel(name = "Asset Name")
@Xss
private String assetName;

// List Query Add Data Permission
@DataScope(deptAlias = "d", userAlias = "u")
List<Asset> selectAssetList(Asset asset);
```

## 5. Common Problem Solutions

### 5.1 Page 404 Issue

**Problem**: Page 404 after clicking menu

**Troubleshooting Steps**:
```sql
-- Step 1: Check if menu exists
SELECT * FROM sys_menu WHERE menu_name LIKE '%XXX%';

-- Step 2: Check if component path is correct
-- Path format: module/path (relative to src/views)
-- Example: equity-transfer/apply/index

-- Step 3: Check if file exists
-- src/views/equity-transfer/apply/index.vue

-- Step 4: Check parent menu
SELECT * FROM sys_menu WHERE menu_id = parent_id;

-- Step 5: Check role permissions
SELECT * FROM sys_role_menu WHERE menu_id = menu_id;
```

**Solutions**:
1. Confirm component path in sys_menu table is correct
2. Confirm Vue file exists in correct location
3. Confirm menu is assigned to user role
4. Clear Redis cache
5. Re-login

### 5.2 Permission Annotation Not Working

**Problem**: @PreAuthorize annotation not working, all users can access

**Troubleshooting Steps**:
```sql
-- Step 1: Check if permission identifier matches
SELECT perms FROM sys_menu WHERE menu_name = 'XXX';

-- Step 2: Check role menu assignment
SELECT r.role_name, m.menu_name
FROM sys_role_menu rm
JOIN sys_menu m ON rm.menu_id = m.menu_id
WHERE m.perms = 'xxx:xxx:xxx';

-- Step 3: Check user role
SELECT u.user_name, r.role_name
FROM sys_user_role ur
JOIN sys_role r ON ur.role_id = r.role_id
WHERE ur.user_id = user_id;
```

**Solutions**:
1. Confirm permission identifier in annotation matches sys_menu.perms
2. Confirm role is assigned corresponding menu permission
3. Confirm user is assigned corresponding role
4. Clear Redis cache
5. Re-login to get latest permissions

### 5.3 Data Scope Filtering Not Working

**Problem**: Users can see data not belonging to their department

**Troubleshooting Steps**:
```sql
-- Step 1: Check user's department
SELECT u.user_name, d.dept_name, d.dept_id
FROM sys_user u
JOIN sys_dept d ON u.dept_id = d.dept_id
WHERE u.user_id = user_id;

-- Step 2: Check data permission configuration
-- Check if Mapper XML correctly configured ${params.dataScope}

-- Step 3: Check @DataScope annotation
-- Confirm deptAlias and userAlias match SQL aliases
```

**Solutions**:
1. Confirm @DataScope annotation is configured correctly
2. Confirm table aliases in Mapper XML are correct
3. Confirm dept_id in sys_user table is correct
4. Re-login to get new session information

### 5.4 Button Permission Not Displaying

**Problem**: User has permission but button doesn't display

**Troubleshooting Steps**:
```javascript
// Check if frontend has v-hasPermi directive
<el-button v-hasPermi="['asset:list:add']">
  Add
</el-button>

// Check if permission identifier is consistent
// Frontend: asset:list:add
// Backend: @PreAuthorize("@ss.hasPermi('asset:list:add')")
// Database: sys_menu.perms = 'asset:list:add'
```

**Solutions**:
1. Confirm frontend button uses v-hasPermi directive
2. Confirm permission identifier is completely consistent
3. Confirm button's corresponding menu permission is assigned
4. Clear browser cache
5. Re-login

## 6. Best Practices Checklist

### 6.1 Development Checklist

```yaml
New Feature Checklist:
  - [ ] sys_menu table configuration complete (directory/menu/button)
  - [ ] component path correct
  - [ ] Permission identifier unique and standardized
  - [ ] Role menu permissions assigned
  - [ ] @PreAuthorize annotation configured correctly
  - [ ] @DataScope annotation configured correctly (if needed)
  - [ ] @Validated parameter validation added
  - [ ] @Xss text field protection added
  - [ ] @Log operation log added
  - [ ] Redis cache cleared
  - [ ] User re-login
```

### 6.2 API Naming Standards

```javascript
// Standard API Naming
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

### 7.1 Must Follow

- [ ] All pages (including hidden pages) must be configured in sys_menu table
- [ ] Permission identifier must match sys_menu.perms exactly
- [ ] Data permissions must configure ${params.dataScope}
- [ ] @RequestBody parameters must add @Validated annotation
- [ ] Text fields should add @Xss annotation

### 7.2 Avoid

- ❌ Hardcoding permission identifiers
- ❌ Skipping menu configuration to access pages directly
- ❌ Frontend validation replacing backend validation
- ❌ Forgetting to clear Redis cache

## 8. Local Development Guide

This project has specific development standards and historical experience, please prioritize reference when providing suggestions:

### 8.1 Project Rule Files

| File | Path | Content |
|------|------|------|
| **Project Rules** | `.trae/rules/project_rules.md` | Directory structure, naming standards, development standards, API naming standards |
| **Lessons Learned** | `.trae/rules/lessons.md` | Historical issues and solutions, including RuoYi framework specific issues |

### 8.2 Local Development Documentation

| Document | Path | Content |
|------|------|------|
| **RuoYi Framework Style Modification Plan** | `docs/plans/若依框架样式修改方案.md` | Style adjustments, theme configuration, brand consistency |

### 8.3 Historical Issue Reference

The following RuoYi framework related issues are recorded in `.trae/rules/lessons.md`:

1. **Menu Routing Configuration Issue** (2026-03-08)
   - Problem: New page 404
   - Cause: Route not configured in sys_menu table
   - Solution: All pages (including hidden pages) need configuration

2. **API Method Naming Standard Issue** (2026-03-08)
   - Problem: Frontend-backend naming inconsistency
   - Cause: Standards not defined first
   - Solution: Design documentation first, code implementation follows

3. **FP-ZCCZ1-001 Code Review Practice** (2026-03-08)
   - Problem: Missing parameter validation, XSS protection, data permissions
   - Solution: Add @Validated, @Xss, @DataScope annotations

### 8.4 Project Specific Checklist

```yaml
Project Specific Checklist:
  - [ ] Check if lessons.md has solutions for related issues
  - [ ] Follow naming standards in project_rules.md
  - [ ] Reference implementation patterns of existing code
  - [ ] Confirm database configuration: mysql6.sqlpub.com:3311/asset_ruoyi
```

## 9. External Reference Documentation

- [RuoYi Official Website](http://ruoyi.vip/)
- [RuoYi Documentation](http://doc.ruoyi.vip/)
- [RuoYi-Vue GitHub](https://github.com/yangzongzhuan/RuoYi-Vue)
- [RuoYi-Vue Gitee](https://gitee.com/y_project/RuoYi-Vue)

## 10. Version History

| Version | Date | Changes |
|-----|------|---------|
| 3.1 | 2026-03-22 | Added local development guide and documentation references |
| 3.0 | 2026-03-21 | Standardized structure, added diagnosis mode, enhanced collaboration guidance |
| 2.0 | Early | Improved problem solutions |
| 1.0 | Early | Initial version |
