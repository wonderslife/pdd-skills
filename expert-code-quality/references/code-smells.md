# Code Smells Reference

A comprehensive guide to identifying and fixing code smells, based on Martin Fowler's "Refactoring".

## Table of Contents

1. [Method-Level Smells](#1-method-level-smells)
2. [Class-Level Smells](#2-class-level-smells)
3. [Relationship Smells](#3-relationship-smells)
4. [Other Smells](#4-other-smells)
5. [Smell Detection Checklist](#5-smell-detection-checklist)

---

## 1. Method-Level Smells

### Duplicated Code

**Detection**:
- Same code structure in multiple places
- Similar code with minor variations
- Copy-paste programming

**Problems**:
- Changes must be made in multiple places
- Risk of inconsistent changes
- Increased maintenance burden

**Solutions**:
| Situation | Refactoring |
|-----------|-------------|
| Same method in same class | Extract Method |
| Same method in sibling classes | Pull Up Method |
| Same method in unrelated classes | Extract Class |
| Similar but not identical | Form Template Method |

**Example**:
```java
// Smell
public class Order {
    public double calculateTotal() {
        double total = 0;
        for (Item item : items) {
            total += item.getPrice() * item.getQuantity();
        }
        return total;
    }
}

public class Invoice {
    public double calculateAmount() {
        double amount = 0;
        for (Item item : items) {
            amount += item.getPrice() * item.getQuantity();
        }
        return amount;
    }
}

// Fixed
public class ItemCalculator {
    public double calculateSum(List<Item> items) {
        return items.stream()
            .mapToDouble(i -> i.getPrice() * i.getQuantity())
            .sum();
    }
}
```

---

### Long Method

**Detection**:
- Method exceeds 20 lines
- Requires comments to explain sections
- Deep nesting (3+ levels)
- Multiple responsibilities

**Problems**:
- Hard to understand
- Hard to test
- Hard to reuse
- Hard to name

**Solutions**:
| Situation | Refactoring |
|-----------|-------------|
| Logical code block | Extract Method |
| Complex conditional | Decompose Conditional |
| Long loop body | Extract Method |
| Many temporary variables | Replace Temp with Query |
| Too many parameters | Introduce Parameter Object |

**Metrics**:
- **Good**: < 10 lines
- **Acceptable**: 10-20 lines
- **Warning**: 20-50 lines
- **Critical**: > 50 lines

---

### Long Parameter List

**Detection**:
- More than 3-4 parameters
- Parameters often passed together
- Difficult to remember order

**Problems**:
- Hard to use correctly
- Hard to read
- Hard to maintain
- Often indicates missing abstraction

**Solutions**:
| Situation | Refactoring |
|-----------|-------------|
| Parameters from same object | Preserve Whole Object |
| Parameters always together | Introduce Parameter Object |
| Can be derived | Replace Parameter with Method |
| Flag parameter | Replace Parameter with Explicit Methods |

**Example**:
```java
// Smell
void printReport(Date start, Date end, String title, 
                 String author, String department, boolean summary);

// Fixed
class ReportParameters {
    Date start;
    Date end;
    String title;
    String author;
    String department;
    boolean summary;
}

void printReport(ReportParameters params);
```

---

### Switch Statements

**Detection**:
- Large switch/case blocks
- Switch on type codes
- Repeated switch on same variable

**Problems**:
- Violates Open/Closed Principle
- Changes require modifying switch
- Often duplicated across codebase

**Solutions**:
| Situation | Refactoring |
|-----------|-------------|
| Switch on type | Replace Conditional with Polymorphism |
| Switch in multiple places | Move Method + Replace Conditional |
| Simple type switching | Replace Type Code with Subclasses |

---

## 2. Class-Level Smells

### Large Class

**Detection**:
- Class exceeds 300 lines
- More than 10 instance variables
- More than 20 methods
- Multiple responsibilities

**Problems**:
- Violates Single Responsibility Principle
- Hard to understand
- Hard to test
- High coupling

**Solutions**:
| Situation | Refactoring |
|-----------|-------------|
| Distinct responsibilities | Extract Class |
| Subclass only uses some features | Extract Subclass |
| Common interface | Extract Interface |
| Large data class | Extract Class for behavior |

**Metrics**:
- **Good**: < 100 lines, < 5 fields
- **Acceptable**: 100-200 lines, 5-10 fields
- **Warning**: 200-300 lines, 10-15 fields
- **Critical**: > 300 lines, > 15 fields

---

### Divergent Change

**Detection**:
- One class changes for multiple reasons
- Different types of changes affect same class
- Class has multiple "axes of change"

**Problems**:
- Violates Single Responsibility Principle
- Changes are risky
- Difficult to understand

**Solutions**:
- Extract Class for each responsibility
- Identify different reasons for change
- Separate concerns

**Example**:
```java
// Smell: Employee changes for pay, reporting, AND persistence
public class Employee {
    // Pay calculation
    public double calculatePay() { }
    public double calculateTax() { }
    
    // Reporting
    public String generateReport() { }
    public void printReport() { }
    
    // Persistence
    public void save() { }
    public void load() { }
}

// Fixed: Separate responsibilities
public class Employee {
    private EmployeeData data;
}

public class PayCalculator { }
public class EmployeeReporter { }
public class EmployeeRepository { }
```

---

### Shotgun Surgery

**Detection**:
- One change requires modifying many classes
- Each class only needs small change
- Changes scattered across codebase

**Problems**:
- Easy to miss a change
- Difficult to track all changes
- High coupling across classes

**Solutions**:
| Situation | Refactoring |
|-----------|-------------|
| Feature spread across classes | Move Method |
| Small classes doing little | Inline Class |
| Common functionality | Extract Class |

---

### Feature Envy

**Detection**:
- Method uses another class's data more than its own
- Method calls many getters on another object
- Method belongs in another class

**Problems**:
- Misplaced responsibility
- Increased coupling
- Violates encapsulation

**Solutions**:
- Move Method to the class it envies
- Extract Method if only part should move

**Example**:
```java
// Smell
class Order {
    public double calculateDiscount(Customer customer) {
        return customer.getPoints() > 100 ? 
            customer.getOrderTotal() * 0.1 : 0;
    }
}

// Fixed
class Customer {
    public double calculateDiscount() {
        return points > 100 ? orderTotal * 0.1 : 0;
    }
}
```

---

### Data Class

**Detection**:
- Class has only fields and getters/setters
- No business logic
- Other classes manipulate the data

**Problems**:
- Anemic domain model
- Behavior separated from data
- Procedural code in OO clothing

**Solutions**:
- Encapsulate Collection
- Move behavior to data class
- Hide setters if possible

---

## 3. Relationship Smells

### Inappropriate Intimacy

**Detection**:
- Classes access each other's private parts
- Too much knowledge of each other's internals
- Tight coupling between classes

**Problems**:
- Fragile code
- Changes ripple
- Hard to understand dependencies

**Solutions**:
| Situation | Refactoring |
|-----------|-------------|
| Accessing private fields | Move Method |
| Two-way navigation | Change Bidirectional to Unidirectional |
| Subclass knows parent internals | Replace Inheritance with Delegation |

---

### Message Chains

**Detection**:
- Long chains of method calls: `a.b().c().d()`
- Client knows structure of object graph
- Deep knowledge of relationships

**Problems**:
- Tight coupling to structure
- Changes in chain break client
- Law of Demeter violation

**Solutions**:
- Hide Delegate
- Extract Method to hide chain

**Example**:
```java
// Smell
manager = department.getManager().getContactInfo().getPhoneNumber();

// Fixed
manager = department.getManagerPhone();
```

---

### Middle Man

**Detection**:
- Class mostly delegates to another
- Simple pass-through methods
- No real behavior

**Problems**:
- Unnecessary indirection
- Bloats codebase
- Confuses understanding

**Solutions**:
- Remove Middle Man
- Inline Method
- Keep if adding value (caching, validation)

---

### Parallel Inheritance Hierarchies

**Detection**:
- Creating subclass in one hierarchy forces creating in another
- Hierarchies mirror each other

**Problems**:
- Shotgun surgery for hierarchy changes
- Tight coupling between hierarchies

**Solutions**:
- Move methods to associate hierarchies
- Use composition instead of inheritance

---

## 4. Other Smells

### Primitive Obsession

**Detection**:
- Overuse of primitives (String, int, etc.)
- Multiple parameters of same primitive type
- Constants representing types

**Problems**:
- No type safety
- No encapsulation
- Easy to mix up values

**Solutions**:
- Replace Data Value with Object
- Replace Type Code with Class
- Introduce Parameter Object

**Example**:
```java
// Smell
void setTemperature(double value, String unit);

// Fixed
void setTemperature(Temperature temp);

class Temperature {
    private double value;
    private TemperatureUnit unit;
}
```

---

### Lazy Class

**Detection**:
- Class doing almost nothing
- Could be inlined
- No real purpose

**Problems**:
- Unnecessary complexity
- Maintenance overhead
- Confuses design

**Solutions**:
- Inline Class
- Merge with related class

---

### Speculative Generality

**Detection**:
- Abstract classes with one implementation
- Unused parameters
- "Future-proof" hooks

**Problems**:
- Unnecessary complexity
- Harder to understand
- Maintenance burden

**Solutions**:
- Collapse Hierarchy
- Inline Class
- Remove unused code

---

### Temporary Field

**Detection**:
- Instance variables only set in certain circumstances
- Object has "partial" states
- Null checks for fields

**Problems**:
- Confusing code
- Hard to understand valid states
- Often indicates missing class

**Solutions**:
- Extract Class
- Introduce Null Object

---

### Refused Bequest

**Detection**:
- Subclass doesn't use inherited methods
- Subclass overrides to do nothing
- "Is-a" relationship doesn't hold

**Problems**:
- Incorrect inheritance
- Confusing hierarchy
- LSP violation

**Solutions**:
- Push Down Method
- Replace Inheritance with Delegation

---

### Comments

**Detection**:
- Comments explaining "what" instead of "why"
- Commented-out code
- Long comment blocks

**Problems**:
- Often indicates code smell
- Comments can become outdated
- Can mask bad code

**Solutions**:
- Extract Method instead of explaining
- Rename to make code self-documenting
- Delete commented-out code

**Note**: Good comments explain "why", not "what".

---

## 5. Smell Detection Checklist

### Quick Scan Checklist

```
□ Any method over 20 lines?
□ Any class over 300 lines?
□ Any duplicated code?
□ Any switch statements?
□ Any method with > 4 parameters?
□ Any class with > 10 fields?
□ Any deep inheritance (> 3 levels)?
□ Any long message chains?
□ Any data-only classes?
□ Any lazy classes?
```

### Severity Classification

| Severity | Description | Action |
|----------|-------------|--------|
| **Critical** | Causes bugs, blocks development | Fix immediately |
| **High** | Significant maintenance burden | Fix soon |
| **Medium** | Reduces code quality | Fix when working in area |
| **Low** | Minor improvement | Fix opportunistically |

### Smell → Refactoring Quick Reference

| Smell | Primary Refactoring | Alternative |
|-------|---------------------|-------------|
| Duplicated Code | Extract Method | Pull Up Method |
| Long Method | Extract Method | Replace Temp with Query |
| Large Class | Extract Class | Extract Subclass |
| Long Parameter List | Introduce Parameter Object | Preserve Whole Object |
| Divergent Change | Extract Class | - |
| Shotgun Surgery | Move Method | Inline Class |
| Feature Envy | Move Method | - |
| Data Clumps | Extract Class | Introduce Parameter Object |
| Primitive Obsession | Replace Data Value with Object | - |
| Switch Statements | Replace with Polymorphism | - |
| Parallel Inheritance | Move Method | - |
| Lazy Class | Inline Class | - |
| Speculative Generality | Inline Class | Collapse Hierarchy |
| Temporary Field | Extract Class | Introduce Null Object |
| Message Chains | Hide Delegate | - |
| Middle Man | Remove Middle Man | - |
| Inappropriate Intimacy | Move Method | Change Bidirectional |
| Alternative Classes | Rename Method | - |
| Incomplete Library Class | Introduce Foreign Method | Introduce Local Extension |
| Data Class | Encapsulate Collection | Move Method |
| Refused Bequest | Push Down Method | Replace Inheritance |
| Comments | Extract Method | Rename |

### Detection Tools

**IDE Warnings**:
- Method length warnings
- Parameter count warnings
- Cyclomatic complexity warnings

**Static Analysis**:
- SonarQube
- PMD
- Checkstyle
- ESLint (JavaScript)
- Pylint (Python)

**Metrics to Monitor**:
- Lines of Code (LOC)
- Cyclomatic Complexity
- Coupling Between Objects (CBO)
- Lack of Cohesion of Methods (LCOM)
