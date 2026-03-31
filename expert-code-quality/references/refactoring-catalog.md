# Refactoring Catalog

A comprehensive catalog of refactoring techniques from Martin Fowler's "Refactoring: Improving the Design of Existing Code".

## Table of Contents

1. [Composing Methods](#1-composing-methods)
2. [Moving Features Between Objects](#2-moving-features-between-objects)
3. [Organizing Data](#3-organizing-data)
4. [Simplifying Conditional Expressions](#4-simplifying-conditional-expressions)
5. [Simplifying Method Calls](#5-simplifying-method-calls)
6. [Dealing with Generalization](#6-dealing-with-generalization)

---

## 1. Composing Methods

### Extract Method

**Problem**: You have a code fragment that can be grouped together.

**Solution**: Turn the fragment into a method whose name explains the purpose of the method.

```java
// Before
void printOwing() {
    System.out.println("***********************");
    System.out.println("*** Customer Owes ***");
    System.out.println("***********************");
    // ... more code
}

// After
void printOwing() {
    printBanner();
    // ... more code
}

void printBanner() {
    System.out.println("***********************");
    System.out.println("*** Customer Owes ***");
    System.out.println("***********************");
}
```

**Mechanics**:
1. Create a new method, name it after the intention
2. Copy the extracted code to the new method
3. Replace the original code with a call to the method
4. Compile and test

---

### Inline Method

**Problem**: A method's body is just as clear as its name.

**Solution**: Put the method's body into the body of its callers and remove the method.

```java
// Before
int getRating() {
    return moreThanFiveLateDeliveries() ? 2 : 1;
}
boolean moreThanFiveLateDeliveries() {
    return numberOfLateDeliveries > 5;
}

// After
int getRating() {
    return numberOfLateDeliveries > 5 ? 2 : 1;
}
```

---

### Extract Variable

**Problem**: You have a complex expression.

**Solution**: Put the result of the expression, or parts of the expression, in a temporary variable with a name that explains the purpose.

```java
// Before
if (platform.toUpperCase().indexOf("MAC") > -1 &&
    browser.toUpperCase().indexOf("IE") > -1 &&
    wasInitialized() && resize > 0) {
    // do something
}

// After
final boolean isMacOs = platform.toUpperCase().indexOf("MAC") > -1;
final boolean isIEBrowser = browser.toUpperCase().indexOf("IE") > -1;
final boolean wasResized = resize > 0;

if (isMacOs && isIEBrowser && wasInitialized() && wasResized) {
    // do something
}
```

---

### Replace Temp with Query

**Problem**: You are using a temporary variable to hold the result of an expression.

**Solution**: Extract the expression into a method. Replace all references to the temp with the expression. The new method can then be used in other methods.

```java
// Before
double getPrice() {
    int basePrice = quantity * itemPrice;
    double discountFactor;
    if (basePrice > 1000) discountFactor = 0.95;
    else discountFactor = 0.98;
    return basePrice * discountFactor;
}

// After
double getPrice() {
    return basePrice() * discountFactor();
}

private int basePrice() {
    return quantity * itemPrice;
}

private double discountFactor() {
    if (basePrice() > 1000) return 0.95;
    else return 0.98;
}
```

---

### Introduce Explaining Variable

**Problem**: You have a complicated expression.

**Solution**: Put the result of the expression, or parts of the expression, in a temporary variable with a name that explains the purpose.

```java
// Before
if ((platform.toUpperCase().indexOf("MAC") > -1) &&
    (browser.toUpperCase().indexOf("IE") > -1) &&
    wasInitialized() && resize > 0) {
    // do something
}

// After
final boolean isMacOs = platform.toUpperCase().indexOf("MAC") > -1;
final boolean isIEBrowser = browser.toUpperCase().indexOf("IE") > -1;
final boolean wasResized = resize > 0;

if (isMacOs && isIEBrowser && wasInitialized() && wasResized) {
    // do something
}
```

---

### Split Temporary Variable

**Problem**: You have a temporary variable assigned to more than once, but is not a loop variable nor a collecting temporary variable.

**Solution**: Make a separate temporary variable for each assignment.

```java
// Before
double temp = 2 * (height + width);
System.out.println(temp);
temp = height * width;
System.out.println(temp);

// After
final double perimeter = 2 * (height + width);
System.out.println(perimeter);
final double area = height * width;
System.out.println(area);
```

---

### Remove Assignments to Parameters

**Problem**: The code assigns to a parameter.

**Solution**: Use a temporary variable instead.

```java
// Before
int discount(int inputVal, int quantity, int yearToDate) {
    if (inputVal > 50) inputVal -= 2;
    // ...
}

// After
int discount(int inputVal, int quantity, int yearToDate) {
    int result = inputVal;
    if (inputVal > 50) result -= 2;
    // ...
}
```

---

### Replace Method with Method Object

**Problem**: You have a long method that uses local variables in such a way that you cannot apply Extract Method.

**Solution**: Turn the method into its own object so that all the local variables become fields on that object. You can then decompose the method into other methods on the same object.

```java
// Before
class Order {
    double price() {
        double primaryBasePrice;
        double secondaryBasePrice;
        double tertiaryBasePrice;
        // long computation
    }
}

// After
class Order {
    double price() {
        return new PriceCalculator(this).compute();
    }
}

class PriceCalculator {
    private double primaryBasePrice;
    private double secondaryBasePrice;
    private double tertiaryBasePrice;
    
    PriceCalculator(Order order) {
        // initialize fields
    }
    
    double compute() {
        // computation
    }
}
```

---

### Substitute Algorithm

**Problem**: You want to replace an algorithm with one that is clearer.

**Solution**: Replace the body of the method that implements the algorithm with a new algorithm.

```java
// Before
String foundPerson(String[] people) {
    for (int i = 0; i < people.length; i++) {
        if (people[i].equals("Don")) {
            return "Don";
        }
        if (people[i].equals("John")) {
            return "John";
        }
        if (people[i].equals("Kent")) {
            return "Kent";
        }
    }
    return "";
}

// After
String foundPerson(String[] people) {
    List<String> candidates = Arrays.asList("Don", "John", "Kent");
    for (String person : people) {
        if (candidates.contains(person)) {
            return person;
        }
    }
    return "";
}
```

---

## 2. Moving Features Between Objects

### Move Method

**Problem**: A method is, or will be, using or used by more features of another class than the class on which it is defined.

**Solution**: Create a new method with a similar body in the class it uses most. Either turn the old method into a simple delegation, or remove it altogether.

```java
// Before
class Account {
    double overdraftCharge() {
        if (type.isPremium()) {
            double result = 10;
            if (daysOverdrawn > 7) {
                result += (daysOverdrawn - 7) * 0.85;
            }
            return result;
        }
        return daysOverdrawn * 1.75;
    }
}

// After
class AccountType {
    double overdraftCharge(int daysOverdrawn) {
        if (isPremium()) {
            double result = 10;
            if (daysOverdrawn > 7) {
                result += (daysOverdrawn - 7) * 0.85;
            }
            return result;
        }
        return daysOverdrawn * 1.75;
    }
}
```

---

### Move Field

**Problem**: A field is, or will be, used by another class more than the class on which it is defined.

**Solution**: Create a new field in the target class, and change all its users.

---

### Extract Class

**Problem**: One class does work that should be done by two.

**Solution**: Create a new class and move the relevant fields and methods from the old class into the new class.

```java
// Before
class Person {
    private String name;
    private String officeAreaCode;
    private String officeNumber;
    
    String getTelephoneNumber() {
        return "(" + officeAreaCode + ") " + officeNumber;
    }
}

// After
class Person {
    private String name;
    private TelephoneNumber officeTelephone = new TelephoneNumber();
    
    String getTelephoneNumber() {
        return officeTelephone.getTelephoneNumber();
    }
}

class TelephoneNumber {
    private String areaCode;
    private String number;
    
    String getTelephoneNumber() {
        return "(" + areaCode + ") " + number;
    }
}
```

---

### Inline Class

**Problem**: A class isn't doing very much.

**Solution**: Move all its features into another class and delete it.

---

### Hide Delegate

**Problem**: A client is calling a delegate class of an object through an accessor.

**Solution**: Create methods on the server to hide the delegate.

```java
// Before
class Person {
    Department department;
    
    Department getDepartment() {
        return department;
    }
}

// Client code
manager = john.getDepartment().getManager();

// After
class Person {
    Department department;
    
    Person getManager() {
        return department.getManager();
    }
}

// Client code
manager = john.getManager();
```

---

### Remove Middle Man

**Problem**: A class is doing too much simple delegation.

**Solution**: Get the client to call the delegate directly.

---

### Introduce Foreign Method

**Problem**: A server class you are using needs an additional method, but you can't modify the class.

**Solution**: Create a method in the client class with an instance of the server class as its first argument.

```java
// Before
Date newStart = new Date(previousEnd.getYear(),
    previousEnd.getMonth(), previousEnd.getDate() + 1);

// After
Date newStart = nextDay(previousEnd);

private static Date nextDay(Date arg) {
    return new Date(arg.getYear(), arg.getMonth(), arg.getDate() + 1);
}
```

---

### Introduce Local Extension

**Problem**: A server class you are using needs several additional methods, but you can't modify the class.

**Solution**: Create a new class containing these extra methods. Make this extension class a subclass or wrapper of the original.

---

## 3. Organizing Data

### Self Encapsulate Field

**Problem**: You are accessing a field directly, but the coupling to the field is becoming awkward.

**Solution**: Create getting and setting methods for the field and use only those to access the field.

```java
// Before
private int low, high;
boolean includes(int arg) {
    return arg >= low && arg <= high;
}

// After
private int low, high;
boolean includes(int arg) {
    return arg >= getLow() && arg <= getHigh();
}
int getLow() { return low; }
int getHigh() { return high; }
```

---

### Replace Data Value with Object

**Problem**: You have a data item that needs additional data or behavior.

**Solution**: Turn the data item into an object.

```java
// Before
class Order {
    private String customer;
}

// After
class Order {
    private Customer customer;
}

class Customer {
    private String name;
}
```

---

### Change Value to Reference

**Problem**: You have a class with many equal instances that you want to replace with a single object.

**Solution**: Turn the object into a reference object.

---

### Change Reference to Value

**Problem**: You have a reference object that is small, immutable, and awkward to manage.

**Solution**: Turn the reference object into a value object.

---

### Replace Array with Object

**Problem**: You have an array in which certain elements mean different things.

**Solution**: Replace the array with an object that has a field for each element.

```java
// Before
String[] row = new String[3];
row[0] = "Liverpool";
row[1] = "15";

// After
Performance row = new Performance();
row.setName("Liverpool");
row.setWins("15");
```

---

### Duplicate Observed Data

**Problem**: You have domain data that only needs to be in a GUI control, but domain methods need access to it.

**Solution**: Copy the data to a domain object and set up an observer to synchronize the two.

---

### Change Unidirectional Association to Bidirectional

**Problem**: You have two classes that need to use each other's features, but there is only a one-way link.

**Solution**: Add back pointers, and change modifiers to update both sets.

---

### Change Bidirectional Association to Unidirectional

**Problem**: You have a bidirectional association between two classes, but one of the classes no longer needs features from the other.

**Solution**: Drop the unnecessary end of the association.

---

### Replace Magic Number with Symbolic Constant

**Problem**: You have a literal number with a particular meaning.

**Solution**: Create a constant, name it after the meaning, and replace the number with it.

```java
// Before
double potentialEnergy(double mass, double height) {
    return mass * height * 9.81;
}

// After
static final double GRAVITATIONAL_CONSTANT = 9.81;

double potentialEnergy(double mass, double height) {
    return mass * height * GRAVITATIONAL_CONSTANT;
}
```

---

### Encapsulate Field

**Problem**: There is a public field.

**Solution**: Make it private and provide accessors.

```java
// Before
public String name;

// After
private String name;
public String getName() { return name; }
public void setName(String name) { this.name = name; }
```

---

### Encapsulate Collection

**Problem**: A method returns a collection that is a member of the class.

**Solution**: Have it return a read-only view and provide add/remove methods.

---

## 4. Simplifying Conditional Expressions

### Decompose Conditional

**Problem**: You have a complicated conditional (if-then-else) statement.

**Solution**: Extract methods from the condition, then part, and else part.

```java
// Before
if (date.before(SUMMER_START) || date.after(SUMMER_END)) {
    charge = quantity * winterRate + winterServiceCharge;
} else {
    charge = quantity * summerRate;
}

// After
if (isSummer(date)) {
    charge = summerCharge(quantity);
} else {
    charge = winterCharge(quantity);
}
```

---

### Consolidate Conditional Expression

**Problem**: You have a sequence of conditional tests with the same result.

**Solution**: Combine them into a single conditional expression and extract it.

```java
// Before
double disabilityAmount() {
    if (seniority < 2) return 0;
    if (monthsDisabled > 12) return 0;
    if (isPartTime) return 0;
    // compute the disability amount
}

// After
double disabilityAmount() {
    if (isNotEligibleForDisability()) return 0;
    // compute the disability amount
}

boolean isNotEligibleForDisability() {
    return seniority < 2 || monthsDisabled > 12 || isPartTime;
}
```

---

### Consolidate Duplicate Conditional Fragments

**Problem**: The same fragment of code is in all branches of a conditional expression.

**Solution**: Move it outside of the expression.

```java
// Before
if (isSpecialDeal()) {
    total = price * 0.95;
    send();
} else {
    total = price * 0.98;
    send();
}

// After
if (isSpecialDeal()) {
    total = price * 0.95;
} else {
    total = price * 0.98;
}
send();
```

---

### Remove Control Flag

**Problem**: You have a variable that is acting as a control flag for a series of boolean expressions.

**Solution**: Use a break or return instead.

---

### Replace Nested Conditional with Guard Clauses

**Problem**: A method has conditional behavior that does not make clear the normal path of execution.

**Solution**: Use guard clauses for all the special cases.

```java
// Before
double getPayAmount() {
    double result;
    if (isDead) {
        result = deadAmount();
    } else {
        if (isSeparated) {
            result = separatedAmount();
        } else {
            if (isRetired) {
                result = retiredAmount();
            } else {
                result = normalPayAmount();
            }
        }
    }
    return result;
}

// After
double getPayAmount() {
    if (isDead) return deadAmount();
    if (isSeparated) return separatedAmount();
    if (isRetired) return retiredAmount();
    return normalPayAmount();
}
```

---

### Replace Conditional with Polymorphism

**Problem**: You have a conditional that chooses different behavior depending on the type of an object.

**Solution**: Move each leg of the conditional to an overriding method in a subclass. Make the original method abstract.

```java
// Before
double getSpeed() {
    switch (type) {
        case EUROPEAN:
            return getBaseSpeed();
        case AFRICAN:
            return getBaseSpeed() - getLoadFactor() * numberOfCoconuts;
        case NORWEGIAN_BLUE:
            return isNailed ? 0 : getBaseSpeed(voltage);
    }
}

// After
abstract class Bird {
    abstract double getSpeed();
}

class EuropeanBird extends Bird {
    double getSpeed() { return getBaseSpeed(); }
}

class AfricanBird extends Bird {
    double getSpeed() { return getBaseSpeed() - getLoadFactor() * numberOfCoconuts; }
}
```

---

### Introduce Null Object

**Problem**: You have repeated checks for a null value.

**Solution**: Replace the null value with a null object.

```java
// Before
if (customer != null) {
    plan = customer.getPlan();
} else {
    plan = Plan.NULL;
}

// After
interface Customer {
    Plan getPlan();
}

class NullCustomer implements Customer {
    Plan getPlan() { return Plan.NULL; }
}

// Usage
plan = customer.getPlan(); // No null check needed
```

---

### Introduce Assertion

**Problem**: A section of code assumes something about the state of the program.

**Solution**: Make the assumption explicit with an assertion.

```java
// Before
double getExpenseLimit() {
    // should have either expense limit or a primary project
    return (expenseLimit != NULL_EXPENSE) ?
        expenseLimit : primaryProject.getMemberExpenseLimit();
}

// After
double getExpenseLimit() {
    Assert.isTrue(expenseLimit != NULL_EXPENSE || primaryProject != null);
    return (expenseLimit != NULL_EXPENSE) ?
        expenseLimit : primaryProject.getMemberExpenseLimit();
}
```

---

## 5. Simplifying Method Calls

### Rename Method

**Problem**: The name of a method does not reveal its purpose.

**Solution**: Rename the method.

```java
// Before
String getNm() { return name; }

// After
String getName() { return name; }
```

---

### Add Parameter

**Problem**: A method needs more information from its caller.

**Solution**: Add a parameter for an object that can pass on this information.

---

### Remove Parameter

**Problem**: A parameter is no longer used by the method body.

**Solution**: Remove it.

---

### Separate Query from Modifier

**Problem**: You have a method that returns a value but also changes the state of an object.

**Solution**: Create two methods, one for the query and one for the modification.

```java
// Before
String getNewMissions() {
    String result = "";
    for (Mission mission : missions) {
        if (mission.isNew()) {
            result += mission.getName() + "\n";
            mission.markAsRead();
        }
    }
    return result;
}

// After
String getNewMissions() {
    return missions.stream()
        .filter(Mission::isNew)
        .map(Mission::getName)
        .collect(Collectors.joining("\n"));
}

void markNewMissionsAsRead() {
    missions.stream()
        .filter(Mission::isNew)
        .forEach(Mission::markAsRead);
}
```

---

### Parameterize Method

**Problem**: Several methods do similar things but with different values contained in the method body.

**Solution**: Create a single method that uses a parameter for the different values.

```java
// Before
void tenPercentRaise() { salary *= 1.1; }
void fivePercentRaise() { salary *= 1.05; }

// After
void raise(double factor) { salary *= (1 + factor); }
```

---

### Replace Parameter with Explicit Methods

**Problem**: You have a method that runs different code depending on the values of an enumerated parameter.

**Solution**: Create a separate method for each value of the parameter.

```java
// Before
void setValue(String name, int value) {
    if (name.equals("height")) {
        height = value;
        return;
    }
    if (name.equals("width")) {
        width = value;
        return;
    }
}

// After
void setHeight(int arg) { height = arg; }
void setWidth(int arg) { width = arg; }
```

---

### Preserve Whole Object

**Problem**: You are getting several values from an object and passing these values as parameters in a method call.

**Solution**: Instead, pass the whole object.

```java
// Before
int low = daysTempRange().getLow();
int high = daysTempRange().getHigh();
boolean withinPlan = plan.withinRange(low, high);

// After
boolean withinPlan = plan.withinRange(daysTempRange());
```

---

### Replace Parameter with Method

**Problem**: An object invokes a method, then passes the result as a parameter for a method. The receiver can also invoke this method.

**Solution**: Remove the parameter and let the receiver invoke the method.

```java
// Before
int basePrice = quantity * itemPrice;
discountLevel = getDiscountLevel();
double finalPrice = discountedPrice(basePrice, discountLevel);

// After
double finalPrice = discountedPrice();
```

---

### Introduce Parameter Object

**Problem**: You have a group of parameters that naturally go together.

**Solution**: Replace them with an object.

```java
// Before
void printReport(Date start, Date end, String title, String author);

// After
class ReportParameters {
    Date start;
    Date end;
    String title;
    String author;
}

void printReport(ReportParameters params);
```

---

### Remove Setting Method

**Problem**: The value of a field should be set only when it is initialized, and not changed at any other time.

**Solution**: Remove any setting method for that field.

---

### Hide Method

**Problem**: A method is not used by any other class.

**Solution**: Make the method private.

---

### Replace Constructor with Factory Method

**Problem**: You want to do more than simple construction when you create an object.

**Solution**: Replace the constructor with a factory method.

```java
// Before
Employee(int type) {
    this.type = type;
}

// After
static Employee create(int type) {
    switch (type) {
        case ENGINEER: return new Engineer();
        case SALESMAN: return new Salesman();
        case MANAGER: return new Manager();
    }
}
```

---

### Encapsulate Downcast

**Problem**: A method returns an object that needs to be downcasted by its callers.

**Solution**: Move the downcast to within the method.

```java
// Before
Object lastReading() {
    return readings.lastElement();
}

// After
Reading lastReading() {
    return (Reading) readings.lastElement();
}
```

---

### Replace Error Code with Exception

**Problem**: A method returns a special code to indicate an error.

**Solution**: Throw an exception instead.

```java
// Before
int withdraw(int amount) {
    if (amount > balance) {
        return -1;
    }
    balance -= amount;
    return 0;
}

// After
void withdraw(int amount) throws BalanceException {
    if (amount > balance) {
        throw new BalanceException();
    }
    balance -= amount;
}
```

---

### Replace Exception with Test

**Problem**: You are throwing an exception on a condition the caller could have checked first.

**Solution**: Change the caller to make the test first.

```java
// Before
double getValueForPeriod(int periodNumber) {
    try {
        return values[periodNumber];
    } catch (ArrayIndexOutOfBoundsException e) {
        return 0;
    }
}

// After
double getValueForPeriod(int periodNumber) {
    if (periodNumber >= values.length) {
        return 0;
    }
    return values[periodNumber];
}
```

---

## 6. Dealing with Generalization

### Pull Up Field

**Problem**: Two subclasses have the same field.

**Solution**: Move the field to the superclass.

---

### Pull Up Method

**Problem**: You have methods with identical results on subclasses.

**Solution**: Move them to the superclass.

---

### Pull Up Constructor Body

**Problem**: You have constructors on subclasses with mostly identical bodies.

**Solution**: Create a superclass constructor; call this from the subclass methods.

---

### Push Down Method

**Problem**: Behavior on a superclass is relevant only for some of its subclasses.

**Solution**: Move it to those subclasses.

---

### Push Down Field

**Problem**: A field is used only by some subclasses.

**Solution**: Move it to those subclasses.

---

### Extract Subclass

**Problem**: A class has features that are used only in some instances.

**Solution**: Create a subclass for that subset of features.

```java
// Before
class JobItem {
    private int unitPrice;
    private boolean isLabor;
    
    int getTotalPrice() {
        return isLabor ? getQuantity() * getEmployee().getRate() 
                       : unitPrice * getQuantity();
    }
}

// After
abstract class JobItem {
    abstract int getTotalPrice();
}

class LaborItem extends JobItem {
    int getTotalPrice() {
        return getQuantity() * getEmployee().getRate();
    }
}

class PartsItem extends JobItem {
    int getTotalPrice() {
        return unitPrice * getQuantity();
    }
}
```

---

### Extract Superclass

**Problem**: You have two classes with similar features.

**Solution**: Create a superclass and move the common features to the superclass.

---

### Extract Interface

**Problem**: Several clients use the same subset of a class interface, or two classes have part of their interfaces in common.

**Solution**: Extract the subset into an interface.

```java
// Before
class Employee {
    double getRate();
    boolean hasSpecialSkill();
}

// After
interface Billable {
    double getRate();
}

class Employee implements Billable {
    public double getRate() { ... }
    boolean hasSpecialSkill() { ... }
}
```

---

### Collapse Hierarchy

**Problem**: A superclass and subclass are not very different.

**Solution**: Merge them together.

---

### Form Template Method

**Problem**: You have two methods in subclasses that carry out similar steps in the same order, but the steps are different.

**Solution**: Get the steps into methods with the same signature, so that the original methods become the same. Then you can pull them up.

---

### Replace Inheritance with Delegation

**Problem**: A subclass uses only part of a superclass interface or does not want to inherit data.

**Solution**: Create a field for the superclass, adjust methods to delegate to the superclass, and remove the inheritance.

---

### Replace Delegation with Inheritance

**Problem**: You're using delegation and are often writing many simple delegations for the entire interface.

**Solution**: Make the delegating class a subclass of the delegate.

---

## Summary: Refactoring Quick Reference Card

| Smell | Primary Refactoring |
|-------|---------------------|
| Duplicated Code | Extract Method |
| Long Method | Extract Method |
| Large Class | Extract Class |
| Long Parameter List | Introduce Parameter Object |
| Divergent Change | Extract Class |
| Shotgun Surgery | Move Method |
| Feature Envy | Move Method |
| Data Clumps | Extract Class |
| Primitive Obsession | Replace Data Value with Object |
| Switch Statements | Replace Conditional with Polymorphism |
| Parallel Inheritance | Move Method |
| Lazy Class | Inline Class |
| Speculative Generality | Inline Class |
| Temporary Field | Extract Class |
| Message Chains | Hide Delegate |
| Middle Man | Remove Middle Man |
| Inappropriate Intimacy | Move Method |
| Alternative Classes | Rename Method |
| Incomplete Library Class | Introduce Foreign Method |
| Data Class | Encapsulate Collection |
| Refused Bequest | Push Down Method |
| Comments | Extract Method |
