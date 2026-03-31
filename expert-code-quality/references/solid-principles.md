# SOLID Principles Reference

A comprehensive guide to the five SOLID principles of object-oriented design.

## Table of Contents

1. [Overview](#1-overview)
2. [Single Responsibility Principle (SRP)](#2-single-responsibility-principle-srp)
3. [Open/Closed Principle (OCP)](#3-openclosed-principle-ocp)
4. [Liskov Substitution Principle (LSP)](#4-liskov-substitution-principle-lsp)
5. [Interface Segregation Principle (ISP)](#5-interface-segregation-principle-isp)
6. [Dependency Inversion Principle (DIP)](#6-dependency-inversion-principle-dip)
7. [SOLID Quick Reference](#7-solid-quick-reference)

---

## 1. Overview

SOLID is an acronym for five design principles intended to make software designs more understandable, flexible, and maintainable.

| Letter | Principle | Key Concept |
|--------|-----------|-------------|
| **S** | Single Responsibility | One reason to change |
| **O** | Open/Closed | Open for extension, closed for modification |
| **L** | Liskov Substitution | Subtypes must be substitutable |
| **I** | Interface Segregation | Small, focused interfaces |
| **D** | Dependency Inversion | Depend on abstractions |

---

## 2. Single Responsibility Principle (SRP)

### Definition

> A class should have only one reason to change.

### Explanation

Every module or class should have responsibility over a single part of the functionality provided by the software, and that responsibility should be entirely encapsulated by the class.

### Violation Detection

```
□ Does the class have more than one "reason to change"?
□ Does the class name contain "and" or "or"?
□ Are there groups of methods using different instance variables?
□ Is the class doing more than one thing?
```

### Example: Violation

```java
// VIOLATION: Employee has multiple reasons to change
public class Employee {
    private String name;
    private double salary;
    
    // Reason 1: Employee data changes
    public String getName() { return name; }
    public double getSalary() { return salary; }
    
    // Reason 2: Pay calculation changes
    public double calculatePay() { /* ... */ }
    public double calculateTax() { /* ... */ }
    
    // Reason 3: Reporting changes
    public String generateReport() { /* ... */ }
    public void printReport() { /* ... */ }
    
    // Reason 4: Persistence changes
    public void save() { /* ... */ }
    public void load() { /* ... */ }
}
```

### Example: Correct

```java
// Each class has one reason to change
public class Employee {
    private String name;
    private double salary;
    
    public String getName() { return name; }
    public double getSalary() { return salary; }
}

public class PayCalculator {
    public double calculatePay(Employee employee) { /* ... */ }
    public double calculateTax(Employee employee) { /* ... */ }
}

public class EmployeeReporter {
    public String generateReport(Employee employee) { /* ... */ }
    public void printReport(String report) { /* ... */ }
}

public class EmployeeRepository {
    public void save(Employee employee) { /* ... */ }
    public Employee load(int id) { /* ... */ }
}
```

### Benefits

- Easier to understand
- Easier to test
- Easier to maintain
- Lower coupling

---

## 3. Open/Closed Principle (OCP)

### Definition

> Software entities should be open for extension, but closed for modification.

### Explanation

You should be able to extend a class's behavior without modifying its source code. This is typically achieved through abstractions and polymorphism.

### Violation Detection

```
□ Do you need to modify existing code to add new behavior?
□ Are there switch statements on type?
□ Do you need to touch multiple files for one feature?
□ Is adding new types difficult?
```

### Example: Violation

```java
// VIOLATION: Must modify class to add new shapes
public class AreaCalculator {
    public double calculateArea(Object shape) {
        if (shape instanceof Circle) {
            Circle circle = (Circle) shape;
            return Math.PI * circle.getRadius() * circle.getRadius();
        } else if (shape instanceof Rectangle) {
            Rectangle rectangle = (Rectangle) shape;
            return rectangle.getWidth() * rectangle.getHeight();
        }
        // Must add new "else if" for each new shape!
        throw new IllegalArgumentException("Unknown shape");
    }
}
```

### Example: Correct

```java
// Open for extension, closed for modification
public interface Shape {
    double calculateArea();
}

public class Circle implements Shape {
    private double radius;
    
    public double calculateArea() {
        return Math.PI * radius * radius;
    }
}

public class Rectangle implements Shape {
    private double width;
    private double height;
    
    public double calculateArea() {
        return width * height;
    }
}

// Adding new shapes doesn't require modifying existing code
public class Triangle implements Shape {
    private double base;
    private double height;
    
    public double calculateArea() {
        return 0.5 * base * height;
    }
}

// Calculator never needs modification
public class AreaCalculator {
    public double calculateArea(Shape shape) {
        return shape.calculateArea();
    }
}
```

### Benefits

- No risk of breaking existing functionality
- Easy to add new features
- Follows Single Responsibility Principle

---

## 4. Liskov Substitution Principle (LSP)

### Definition

> Subtypes must be substitutable for their base types without altering the correctness of the program.

### Explanation

If S is a subtype of T, then objects of type T may be replaced with objects of type S without altering any of the desirable properties of the program.

### Violation Detection

```
□ Does subclass throw unexpected exceptions?
□ Does subclass return unexpected values?
□ Does subclass have stricter preconditions?
□ Does subclass have weaker postconditions?
□ Does subclass violate base class invariants?
```

### Example: Violation

```java
// VIOLATION: Square is not a proper Rectangle
public class Rectangle {
    protected double width;
    protected double height;
    
    public void setWidth(double width) { this.width = width; }
    public void setHeight(double height) { this.height = height; }
    
    public double getArea() { return width * height; }
}

public class Square extends Rectangle {
    @Override
    public void setWidth(double width) {
        this.width = width;
        this.height = width; // Violates Rectangle behavior!
    }
    
    @Override
    public void setHeight(double height) {
        this.width = height; // Violates Rectangle behavior!
        this.height = height;
    }
}

// Client code breaks
void resizeRectangle(Rectangle rect) {
    rect.setWidth(5);
    rect.setHeight(4);
    // Expected: area = 20
    // With Square: area = 16 (unexpected!)
}
```

### Example: Correct

```java
// Correct: Use composition or proper hierarchy
public abstract class Shape {
    public abstract double getArea();
}

public class Rectangle extends Shape {
    private double width;
    private double height;
    
    public double getArea() { return width * height; }
    // setWidth and setHeight are Rectangle-specific
}

public class Square extends Shape {
    private double side;
    
    public double getArea() { return side * side; }
    public void setSide(double side) { this.side = side; }
}
```

### LSP Rules

| Rule | Description |
|------|-------------|
| **Signature Rule** | Subtype method signatures must match |
| **Methods Rule** | Subtype methods must return subtype |
| **Properties Rule** | Subtype must preserve invariants |
| **Preconditions** | Cannot be stronger in subtype |
| **Postconditions** | Cannot be weaker in subtype |

### Benefits

- Reliable polymorphism
- Predictable behavior
- Reusable code

---

## 5. Interface Segregation Principle (ISP)

### Definition

> Clients should not be forced to depend on interfaces they do not use.

### Explanation

Many client-specific interfaces are better than one general-purpose interface. No client should be forced to depend on methods it does not use.

### Violation Detection

```
□ Does interface have many methods?
□ Do implementations throw "UnsupportedOperationException"?
□ Do clients only use some methods?
□ Is interface "fat"?
```

### Example: Violation

```java
// VIOLATION: Fat interface
public interface Worker {
    void work();
    void eat();
    void sleep();
}

public class Human implements Worker {
    public void work() { /* works */ }
    public void eat() { /* eats */ }
    public void sleep() { /* sleeps */ }
}

public class Robot implements Worker {
    public void work() { /* works */ }
    public void eat() { 
        throw new UnsupportedOperationException("Robots don't eat!"); 
    }
    public void sleep() { 
        throw new UnsupportedOperationException("Robots don't sleep!"); 
    }
}
```

### Example: Correct

```java
// Segregated interfaces
public interface Workable {
    void work();
}

public interface Feedable {
    void eat();
}

public interface Sleepable {
    void sleep();
}

public class Human implements Workable, Feedable, Sleepable {
    public void work() { /* works */ }
    public void eat() { /* eats */ }
    public void sleep() { /* sleeps */ }
}

public class Robot implements Workable {
    public void work() { /* works */ }
    // No need to implement eat() or sleep()
}
```

### Benefits

- No unnecessary dependencies
- Easier to implement
- Clearer contracts
- Better cohesion

---

## 6. Dependency Inversion Principle (DIP)

### Definition

> High-level modules should not depend on low-level modules. Both should depend on abstractions.
> Abstractions should not depend on details. Details should depend on abstractions.

### Explanation

The principle suggests that we should decouple high-level modules from low-level modules by introducing an abstraction layer between them.

### Violation Detection

```
□ Does high-level class directly instantiate low-level class?
□ Are there "new" keywords in business logic?
□ Is code difficult to test?
□ Are dependencies hardcoded?
```

### Example: Violation

```java
// VIOLATION: High-level depends on low-level
public class UserService {
    private MySQLDatabase database; // Direct dependency
    
    public UserService() {
        this.database = new MySQLDatabase(); // Hardcoded
    }
    
    public User getUser(int id) {
        return database.query("SELECT * FROM users WHERE id = " + id);
    }
}
```

### Example: Correct

```java
// Correct: Depend on abstractions
public interface Database {
    User query(String sql);
}

public class MySQLDatabase implements Database {
    public User query(String sql) { /* MySQL implementation */ }
}

public class PostgreSQLDatabase implements Database {
    public User query(String sql) { /* PostgreSQL implementation */ }
}

public class UserService {
    private Database database; // Depends on abstraction
    
    public UserService(Database database) { // Dependency injection
        this.database = database;
    }
    
    public User getUser(int id) {
        return database.query("SELECT * FROM users WHERE id = " + id);
    }
}

// Usage
UserService service = new UserService(new MySQLDatabase());
UserService service = new UserService(new PostgreSQLDatabase());
```

### Dependency Injection Types

| Type | Description |
|------|-------------|
| **Constructor Injection** | Dependencies passed in constructor |
| **Setter Injection** | Dependencies set via setters |
| **Interface Injection** | Dependencies via interface method |
| **Field Injection** | Dependencies set directly on fields (not recommended) |

### Benefits

- Loose coupling
- Easy to test (mock dependencies)
- Easy to change implementations
- Follows Open/Closed Principle

---

## 7. SOLID Quick Reference

### Principle Summary

| Principle | Problem | Solution |
|-----------|---------|----------|
| **SRP** | Class doing too much | Split into focused classes |
| **OCP** | Must modify to extend | Use abstractions |
| **LSP** | Subclass breaks behavior | Ensure substitutability |
| **ISP** | Fat interfaces | Split into small interfaces |
| **DIP** | High depends on low | Depend on abstractions |

### Code Smell → SOLID Principle

| Code Smell | Violated Principle |
|------------|-------------------|
| Large Class | SRP |
| Divergent Change | SRP |
| Shotgun Surgery | OCP |
| Switch Statements | OCP |
| Refused Bequest | LSP |
| Fat Interface | ISP |
| Tight Coupling | DIP |

### SOLID → Pattern Mapping

| Principle | Supporting Patterns |
|-----------|---------------------|
| **SRP** | Facade, Mediator |
| **OCP** | Strategy, Observer, Decorator |
| **LSP** | Template Method, Null Object |
| **ISP** | Adapter, Facade |
| **DIP** | Dependency Injection, Factory, Strategy |

### Quick Checklist

```
□ Does each class have one responsibility?
□ Can you extend without modifying?
□ Are subclasses substitutable for parents?
□ Are interfaces small and focused?
□ Do you depend on abstractions, not concretions?
```

### Refactoring to SOLID

| From | To | Refactoring |
|------|-----|-------------|
| Large class | SRP | Extract Class |
| Switch on type | OCP | Replace Conditional with Polymorphism |
| Subclass violations | LSP | Replace Inheritance with Delegation |
| Fat interface | ISP | Extract Interface |
| Direct instantiation | DIP | Replace Constructor with Factory |
