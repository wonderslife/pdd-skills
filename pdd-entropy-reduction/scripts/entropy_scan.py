#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDD 熵减检测脚本

用于检测代码库中的熵增问题，包括：
- 文档-代码不一致
- 架构边界违规
- 重复代码
- 过期TODO
- 复杂度过高

使用方法:
    python entropy_scan.py --project /path/to/project --output report.md
"""

import os
import re
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class EntropyIssue:
    """熵增问题"""
    category: str           # 类别: doc, arch, code, debt
    severity: str           # 严重程度: critical, high, medium, low
    title: str              # 问题标题
    location: str           # 位置
    description: str        # 描述
    suggestion: str         # 建议
    score: int = 0          # 熵值贡献


@dataclass
class EntropyReport:
    """熵减报告"""
    project_path: str
    scan_time: str
    doc_entropy: int = 0
    arch_entropy: int = 0
    code_entropy: int = 0
    debt_entropy: int = 0
    total_entropy: int = 0
    issues: List[EntropyIssue] = field(default_factory=list)
    
    def calculate_total(self):
        """计算综合熵值"""
        self.total_entropy = int(
            self.doc_entropy * 0.25 +
            self.arch_entropy * 0.30 +
            self.code_entropy * 0.25 +
            self.debt_entropy * 0.20
        )
    
    def get_status(self) -> str:
        """获取状态"""
        if self.total_entropy <= 30:
            return "🟢 健康"
        elif self.total_entropy <= 60:
            return "🟡 警告"
        else:
            return "🔴 危险"


class EntropyScanner:
    """熵减扫描器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.issues: List[EntropyIssue] = []
        
        # 配置
        self.config = {
            'todo_stale_days': 30,
            'doc_stale_days': 90,
            'complexity_threshold': 20,
            'function_length_threshold': 100,
            'nesting_threshold': 5,
            'duplicate_threshold': 5,
        }
        
        # 排除目录
        self.exclude_dirs = {
            'node_modules', 'dist', 'build', '.git', '__pycache__',
            'target', 'vendor', '.idea', '.vscode'
        }
        
        # 文档目录
        self.doc_dirs = {'docs', 'doc', 'documentation'}
        
        # 六层模型
        self.layers = {
            'types': 1,
            'config': 2,
            'repo': 3,
            'service': 4,
            'runtime': 5,
            'ui': 6
        }
    
    def scan(self) -> EntropyReport:
        """执行扫描"""
        report = EntropyReport(
            project_path=str(self.project_path),
            scan_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        # 1. 文档一致性扫描
        doc_issues = self._scan_document_consistency()
        report.doc_entropy = self._calculate_category_entropy(doc_issues)
        self.issues.extend(doc_issues)
        
        # 2. 架构边界扫描
        arch_issues = self._scan_architecture_violations()
        report.arch_entropy = self._calculate_category_entropy(arch_issues)
        self.issues.extend(arch_issues)
        
        # 3. 代码质量扫描
        code_issues = self._scan_code_quality()
        report.code_entropy = self._calculate_category_entropy(code_issues)
        self.issues.extend(code_issues)
        
        # 4. 技术债务扫描
        debt_issues = self._scan_technical_debt()
        report.debt_entropy = self._calculate_category_entropy(debt_issues)
        self.issues.extend(debt_issues)
        
        report.issues = self.issues
        report.calculate_total()
        
        return report
    
    def _scan_document_consistency(self) -> List[EntropyIssue]:
        """扫描文档一致性"""
        issues = []
        
        # 1. 检查过期TODO
        issues.extend(self._check_stale_todos())
        
        # 2. 检查孤立文档
        issues.extend(self._check_orphan_docs())
        
        # 3. 检查API文档一致性
        issues.extend(self._check_api_doc_consistency())
        
        return issues
    
    def _check_stale_todos(self) -> List[EntropyIssue]:
        """检查过期TODO"""
        issues = []
        stale_threshold = datetime.now() - timedelta(days=self.config['todo_stale_days'])
        
        todo_pattern = re.compile(
            r'//\s*(TODO|FIXME|HACK|XXX):\s*(.+?)(?:\s*-\s*(\d{4}-\d{2}-\d{2}))?$',
            re.IGNORECASE
        )
        
        for file_path in self._iter_code_files():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        match = todo_pattern.search(line)
                        if match:
                            todo_type, content, date_str = match.groups()
                            
                            if date_str:
                                todo_date = datetime.strptime(date_str, '%Y-%m-%d')
                                if todo_date < stale_threshold:
                                    issues.append(EntropyIssue(
                                        category='doc',
                                        severity='medium',
                                        title=f'过期{todo_type.upper()}',
                                        location=f'{file_path}:{line_num}',
                                        description=f'{todo_type}: {content} (创建于 {date_str})',
                                        suggestion='完成或删除此TODO',
                                        score=5
                                    ))
            except Exception:
                continue
        
        return issues
    
    def _check_orphan_docs(self) -> List[EntropyIssue]:
        """检查孤立文档"""
        issues = []
        
        # 查找文档目录
        for doc_dir in self.doc_dirs:
            doc_path = self.project_path / doc_dir
            if not doc_path.exists():
                continue
            
            # 检查每个文档文件
            for doc_file in doc_path.rglob('*.md'):
                # 检查是否有对应的代码文件
                doc_name = doc_file.stem
                
                # 特殊文档不需要对应代码
                special_docs = {'README', 'CHANGELOG', 'CONTRIBUTING', 'LICENSE', 'index'}
                if doc_name in special_docs:
                    continue
                
                # 检查是否被引用
                referenced = self._is_doc_referenced(doc_file)
                if not referenced:
                    issues.append(EntropyIssue(
                        category='doc',
                        severity='low',
                        title='孤立文档',
                        location=str(doc_file.relative_to(self.project_path)),
                        description='文档未被任何代码或其他文档引用',
                        suggestion='检查是否需要归档或删除',
                        score=3
                    ))
        
        return issues
    
    def _is_doc_referenced(self, doc_file: Path) -> bool:
        """检查文档是否被引用"""
        doc_name = doc_file.name
        doc_path_str = str(doc_file.relative_to(self.project_path))
        
        for file_path in self._iter_all_files():
            if file_path.suffix in {'.md', '.ts', '.js', '.tsx', '.jsx', '.py', '.java'}:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if doc_name in content or doc_path_str in content:
                            return True
                except Exception:
                    continue
        
        return False
    
    def _check_api_doc_consistency(self) -> List[EntropyIssue]:
        """检查API文档一致性"""
        issues = []
        
        # 查找API定义文件
        api_files = list(self.project_path.rglob('**/api/*.ts')) + \
                   list(self.project_path.rglob('**/api/*.js'))
        
        # 查找API文档
        api_docs = list(self.project_path.rglob('**/docs/api/*.md'))
        
        if api_files and not api_docs:
            issues.append(EntropyIssue(
                category='doc',
                severity='high',
                title='缺少API文档',
                location='docs/api/',
                description=f'发现 {len(api_files)} 个API文件，但没有对应的API文档',
                suggestion='创建API文档目录并编写文档',
                score=10
            ))
        
        return issues
    
    def _scan_architecture_violations(self) -> List[EntropyIssue]:
        """扫描架构违规"""
        issues = []
        
        # 检查六层模型违规
        issues.extend(self._check_layer_violations())
        
        # 检查循环依赖
        issues.extend(self._check_circular_dependencies())
        
        return issues
    
    def _check_layer_violations(self) -> List[EntropyIssue]:
        """检查层级违规"""
        issues = []
        
        # 定义层级检测规则
        layer_patterns = {
            'ui': ['components/', 'views/', 'pages/', 'ui/'],
            'service': ['services/', 'service/', 'business/'],
            'repo': ['repositories/', 'repo/', 'dao/', 'data/'],
            'config': ['config/', 'configuration/'],
            'types': ['types/', 'interfaces/', 'models/'],
        }
        
        for file_path in self._iter_code_files():
            file_str = str(file_path)
            
            # 确定文件所在层级
            file_layer = None
            for layer, patterns in layer_patterns.items():
                if any(p in file_str for p in patterns):
                    file_layer = layer
                    break
            
            if not file_layer:
                continue
            
            # 检查导入
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # 检查是否导入了更高层级
                    for layer, patterns in layer_patterns.items():
                        if self.layers.get(layer, 0) > self.layers.get(file_layer, 0):
                            for pattern in patterns:
                                if f"from '{pattern}" in content or f'from "{pattern}' in content:
                                    issues.append(EntropyIssue(
                                        category='arch',
                                        severity='critical',
                                        title='层级违规',
                                        location=str(file_path.relative_to(self.project_path)),
                                        description=f'{file_layer}层导入了{layer}层',
                                        suggestion='重构以符合六层依赖模型',
                                        score=15
                                    ))
            except Exception:
                continue
        
        return issues
    
    def _check_circular_dependencies(self) -> List[EntropyIssue]:
        """检查循环依赖"""
        issues = []
        
        # 简化的循环依赖检测
        imports = defaultdict(set)
        
        for file_path in self._iter_code_files():
            if file_path.suffix not in {'.ts', '.js', '.tsx', '.jsx'}:
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # 提取导入
                    import_pattern = re.compile(r"from\s+['\"](.+?)['\"]")
                    for match in import_pattern.finditer(content):
                        import_path = match.group(1)
                        if not import_path.startswith('.'):
                            continue
                        
                        # 解析相对路径
                        source = str(file_path.relative_to(self.project_path))
                        imports[source].add(import_path)
            except Exception:
                continue
        
        # 检测循环（简化版）
        # 实际实现需要完整的依赖图分析
        
        return issues
    
    def _scan_code_quality(self) -> List[EntropyIssue]:
        """扫描代码质量"""
        issues = []
        
        # 检查复杂度
        issues.extend(self._check_complexity())
        
        # 检查重复代码
        issues.extend(self._check_duplicates())
        
        # 检查命名规范
        issues.extend(self._check_naming())
        
        return issues
    
    def _check_complexity(self) -> List[EntropyIssue]:
        """检查代码复杂度"""
        issues = []
        
        for file_path in self._iter_code_files():
            if file_path.suffix not in {'.ts', '.js', '.tsx', '.jsx', '.py', '.java'}:
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    
                    # 检查函数长度
                    self._check_function_length(file_path, lines, issues)
                    
                    # 检查嵌套深度
                    self._check_nesting_depth(file_path, lines, issues)
            except Exception:
                continue
        
        return issues
    
    def _check_function_length(self, file_path: Path, lines: List[str], issues: List[EntropyIssue]):
        """检查函数长度"""
        threshold = self.config['function_length_threshold']
        
        # 简化的函数检测
        func_pattern = re.compile(r'^\s*(async\s+)?function\s+(\w+|<[^>]+>)')
        class_pattern = re.compile(r'^\s*class\s+\w+')
        
        func_start = None
        func_name = None
        brace_count = 0
        
        for i, line in enumerate(lines):
            if func_pattern.match(line):
                if func_start is not None and i - func_start > threshold:
                    issues.append(EntropyIssue(
                        category='code',
                        severity='medium',
                        title='函数过长',
                        location=f'{file_path}:{func_start + 1}',
                        description=f'函数 {func_name} 有 {i - func_start} 行，超过阈值 {threshold}',
                        suggestion='拆分为更小的函数',
                        score=8
                    ))
                func_start = i
                func_name = func_pattern.match(line).group(2)
                brace_count = 0
            
            if func_start is not None:
                brace_count += line.count('{') - line.count('}')
                if brace_count == 0 and '{' in ''.join(lines[func_start:i+1]):
                    if i - func_start > threshold:
                        issues.append(EntropyIssue(
                            category='code',
                            severity='medium',
                            title='函数过长',
                            location=f'{file_path}:{func_start + 1}',
                            description=f'函数 {func_name} 有 {i - func_start} 行',
                            suggestion='拆分为更小的函数',
                            score=8
                        ))
                    func_start = None
    
    def _check_nesting_depth(self, file_path: Path, lines: List[str], issues: List[EntropyIssue]):
        """检查嵌套深度"""
        threshold = self.config['nesting_threshold']
        max_depth = 0
        max_depth_line = 0
        
        current_depth = 0
        for i, line in enumerate(lines):
            current_depth += line.count('{') - line.count('}')
            if current_depth > max_depth:
                max_depth = current_depth
                max_depth_line = i + 1
        
        if max_depth > threshold:
            issues.append(EntropyIssue(
                category='code',
                severity='medium',
                title='嵌套过深',
                location=f'{file_path}:{max_depth_line}',
                description=f'最大嵌套深度 {max_depth}，超过阈值 {threshold}',
                suggestion='使用早返回或提取方法减少嵌套',
                score=6
            ))
    
    def _check_duplicates(self) -> List[EntropyIssue]:
        """检查重复代码"""
        issues = []
        
        # 简化的重复检测
        code_blocks = defaultdict(list)
        block_size = 10  # 代码块大小
        
        for file_path in self._iter_code_files():
            if file_path.suffix not in {'.ts', '.js', '.tsx', '.jsx'}:
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    
                    for i in range(len(lines) - block_size):
                        block = ''.join(lines[i:i+block_size]).strip()
                        if len(block) > 50:  # 忽略太短的块
                            code_blocks[block].append((str(file_path), i+1))
            except Exception:
                continue
        
        # 找出重复的块
        for block, locations in code_blocks.items():
            if len(locations) >= self.config['duplicate_threshold']:
                issues.append(EntropyIssue(
                    category='code',
                    severity='high',
                    title='重复代码',
                    location=', '.join([f'{p}:{l}' for p, l in locations[:3]]),
                    description=f'发现 {len(locations)} 处相似代码块',
                    suggestion='提取到共享函数',
                    score=12
                ))
        
        return issues
    
    def _check_naming(self) -> List[EntropyIssue]:
        """检查命名规范"""
        issues = []
        
        # 简化的命名检查
        bad_patterns = [
            (r'\bvar\s+[a-z]\b', '单字母变量名'),
            (r'\bfunction\s+[a-z]\s*\(', '单字母函数名'),
            (r'\b(const|let|var)\s+_\w+', '下划线前缀变量'),
        ]
        
        for file_path in self._iter_code_files():
            if file_path.suffix not in {'.ts', '.js', '.tsx', '.jsx'}:
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        for pattern, desc in bad_patterns:
                            if re.search(pattern, line):
                                issues.append(EntropyIssue(
                                    category='code',
                                    severity='low',
                                    title='命名不规范',
                                    location=f'{file_path}:{line_num}',
                                    description=desc,
                                    suggestion='使用更具描述性的名称',
                                    score=2
                                ))
            except Exception:
                continue
        
        return issues
    
    def _scan_technical_debt(self) -> List[EntropyIssue]:
        """扫描技术债务"""
        issues = []
        
        # 检查TODO数量
        todo_count = sum(1 for issue in self.issues if 'TODO' in issue.title)
        if todo_count > 20:
            issues.append(EntropyIssue(
                category='debt',
                severity='high',
                title='技术债务过多',
                location='全局',
                description=f'发现 {todo_count} 个未处理的TODO',
                suggestion='分配时间偿还技术债务',
                score=15
            ))
        
        # 检查测试覆盖率（简化）
        test_files = list(self.project_path.rglob('**/*.test.ts')) + \
                    list(self.project_path.rglob('**/*.spec.ts'))
        source_files = list(self.project_path.rglob('**/src/**/*.ts'))
        
        if source_files and len(test_files) / len(source_files) < 0.5:
            issues.append(EntropyIssue(
                category='debt',
                severity='medium',
                title='测试覆盖率低',
                location='tests/',
                description=f'测试文件与源文件比例: {len(test_files)}/{len(source_files)}',
                suggestion='增加单元测试',
                score=8
            ))
        
        return issues
    
    def _calculate_category_entropy(self, issues: List[EntropyIssue]) -> int:
        """计算类别熵值"""
        if not issues:
            return 0
        
        total_score = sum(issue.score for issue in issues)
        # 归一化到 0-100
        return min(100, total_score)
    
    def _iter_code_files(self):
        """迭代代码文件"""
        for file_path in self.project_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in {
                '.ts', '.js', '.tsx', '.jsx', '.py', '.java', '.go', '.rs'
            }:
                # 排除目录
                if any(part in self.exclude_dirs for part in file_path.parts):
                    continue
                yield file_path
    
    def _iter_all_files(self):
        """迭代所有文件"""
        for file_path in self.project_path.rglob('*'):
            if file_path.is_file():
                if any(part in self.exclude_dirs for part in file_path.parts):
                    continue
                yield file_path


def generate_report(report: EntropyReport, output_format: str = 'markdown') -> str:
    """生成报告"""
    if output_format == 'json':
        return json.dumps({
            'project_path': report.project_path,
            'scan_time': report.scan_time,
            'entropy': {
                'doc': report.doc_entropy,
                'arch': report.arch_entropy,
                'code': report.code_entropy,
                'debt': report.debt_entropy,
                'total': report.total_entropy
            },
            'status': report.get_status(),
            'issues': [
                {
                    'category': i.category,
                    'severity': i.severity,
                    'title': i.title,
                    'location': i.location,
                    'description': i.description,
                    'suggestion': i.suggestion
                }
                for i in report.issues
            ]
        }, indent=2, ensure_ascii=False)
    
    # Markdown 格式
    md = f"""# PDD 熵减报告

## 报告元信息

- **项目路径**: {report.project_path}
- **扫描时间**: {report.scan_time}
- **报告ID**: ER-{datetime.now().strftime('%Y%m%d-%H%M%S')}

## 熵值评分总览

| 维度 | 熵值 | 状态 |
|------|------|------|
| 文档一致性 | {report.doc_entropy} | {'🟢' if report.doc_entropy <= 30 else '🟡' if report.doc_entropy <= 60 else '🔴'} |
| 架构合规性 | {report.arch_entropy} | {'🟢' if report.arch_entropy <= 30 else '🟡' if report.arch_entropy <= 60 else '🔴'} |
| 代码质量 | {report.code_entropy} | {'🟢' if report.code_entropy <= 30 else '🟡' if report.code_entropy <= 60 else '🔴'} |
| 技术债务 | {report.debt_entropy} | {'🟢' if report.debt_entropy <= 30 else '🟡' if report.debt_entropy <= 60 else '🔴'} |
| **综合评分** | **{report.total_entropy}** | **{report.get_status()}** |

## 问题清单

"""
    
    # 按严重程度分组
    by_severity = defaultdict(list)
    for issue in report.issues:
        by_severity[issue.severity].append(issue)
    
    for severity in ['critical', 'high', 'medium', 'low']:
        if by_severity[severity]:
            md += f"### {severity.upper()} ({len(by_severity[severity])})\n\n"
            for issue in by_severity[severity]:
                md += f"- **{issue.title}**\n"
                md += f"  - 位置: `{issue.location}`\n"
                md += f"  - 描述: {issue.description}\n"
                md += f"  - 建议: {issue.suggestion}\n\n"
    
    md += f"""
## 改进建议

### 立即处理 (Critical)

"""
    
    critical_issues = [i for i in report.issues if i.severity == 'critical']
    if critical_issues:
        for i, issue in enumerate(critical_issues, 1):
            md += f"{i}. [{issue.category}] {issue.title}\n"
            md += f"   - 位置: {issue.location}\n"
            md += f"   - 建议: {issue.suggestion}\n\n"
    else:
        md += "无 Critical 级别问题。\n\n"
    
    md += """
---

> 本报告由 PDD 熵减机制自动生成
"""
    
    return md


def main():
    parser = argparse.ArgumentParser(description='PDD 熵减检测脚本')
    parser.add_argument('--project', '-p', required=True, help='项目路径')
    parser.add_argument('--output', '-o', default='entropy-report.md', help='输出文件')
    parser.add_argument('--format', '-f', choices=['markdown', 'json'], default='markdown', help='输出格式')
    
    args = parser.parse_args()
    
    print(f"正在扫描项目: {args.project}")
    
    scanner = EntropyScanner(args.project)
    report = scanner.scan()
    
    output = generate_report(report, args.format)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"报告已生成: {args.output}")
    print(f"综合熵值: {report.total_entropy} ({report.get_status()})")


if __name__ == '__main__':
    main()
