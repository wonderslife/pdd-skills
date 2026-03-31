# Design Patterns Reference

A comprehensive reference of the 23 GoF design patterns, organized by category.

## Table of Contents

1. [Creational Patterns](#1-creational-patterns)
2. [Structural Patterns](#2-structural-patterns)
3. [Behavioral Patterns](#3-behavioral-patterns)
4. [Pattern Selection Guide](#4-pattern-selection-guide)

---

## 1. Creational Patterns

### Singleton

**Intent**: Ensure a class only has one instance, and provide a global point of access to it.

**When to Use**:
- Need exactly one instance of a class
- Need a global access point
- Control access to shared resources

**Structure**:
```
┌─────────────────┐
│    Singleton    │
├─────────────────┤
│ - instance      │
├─────────────────┤
│ + getInstance() │
│ - Singleton()   │
└─────────────────┘
```

**Implementation**:
```java
public class Singleton {
    private static volatile Singleton instance;
    
    private Singleton() {}
    
    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}

// Recommended: Enum implementation
public enum Singleton {
    INSTANCE;
    
    public void doSomething() { }
}
```

**Pros**: Controlled access, reduced namespace, extensible
**Cons**: Can hide dependencies, difficult to test, may violate SRP

---

### Factory Method

**Intent**: Define an interface for creating an object, but let subclasses decide which class to instantiate.

**When to Use**:
- A class can't anticipate the class of objects it must create
- A class wants its subclasses to specify the objects it creates

**Structure**:
```
┌──────────────┐      ┌──────────────┐
│   Creator    │      │   Product    │
├──────────────┤      ├──────────────┤
│+factoryMethod│      │+operation()  │
└──────┬───────┘      └──────────────┘
       │                     △
       │                     │
┌──────┴───────┐      ┌──────┴───────┐
│ConcreteCreator│     │ConcreteProduct│
├──────────────┤      ├──────────────┤
│+factoryMethod│      │+operation()  │
└──────────────┘      └──────────────┘
```

**Implementation**:
```java
// Product interface
public interface Product {
    void use();
}

// Concrete products
public class ConcreteProductA implements Product {
    public void use() { System.out.println("Using Product A"); }
}

// Creator
public abstract class Creator {
    public abstract Product factoryMethod();
    
    public void doSomething() {
        Product product = factoryMethod();
        product.use();
    }
}

// Concrete creator
public class ConcreteCreatorA extends Creator {
    public Product factoryMethod() {
        return new ConcreteProductA();
    }
}
```

**Pros**: Decouples client from product creation, supports Open/Closed Principle
**Cons**: May require creating a creator subclass just to instantiate a product

---

### Abstract Factory

**Intent**: Provide an interface for creating families of related or dependent objects without specifying their concrete classes.

**When to Use**:
- A system should be independent of how its products are created
- A family of related product objects is designed to be used together

**Structure**:
```
┌──────────────────┐
│ AbstractFactory  │
├──────────────────┤
│+createProductA() │
│+createProductB() │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
┌───┴───┐ ┌───┴───┐
│Factory│ │Factory│
│   A   │ │   B   │
└───────┘ └───────┘
```

**Implementation**:
```java
// Abstract factory
public interface GUIFactory {
    Button createButton();
    TextField createTextField();
}

// Concrete factories
public class WindowsFactory implements GUIFactory {
    public Button createButton() { return new WindowsButton(); }
    public TextField createTextField() { return new WindowsTextField(); }
}

public class MacFactory implements GUIFactory {
    public Button createButton() { return new MacButton(); }
    public TextField createTextField() { return new MacTextField(); }
}
```

**Pros**: Isolates concrete classes, exchanges product families easily
**Cons**: Difficult to support new kinds of products

---

### Builder

**Intent**: Separate the construction of a complex object from its representation so that the same construction process can create different representations.

**When to Use**:
- The algorithm for creating a complex object should be independent of the parts
- The construction process must allow different representations

**Structure**:
```
Director → Builder ← ConcreteBuilder → Product
```

**Implementation**:
```java
public class Computer {
    private String cpu;
    private String ram;
    private String storage;
    
    private Computer(Builder builder) {
        this.cpu = builder.cpu;
        this.ram = builder.ram;
        this.storage = builder.storage;
    }
    
    public static class Builder {
        private String cpu;
        private String ram;
        private String storage;
        
        public Builder cpu(String cpu) { this.cpu = cpu; return this; }
        public Builder ram(String ram) { this.ram = ram; return this; }
        public Builder storage(String storage) { this.storage = storage; return this; }
        
        public Computer build() {
            return new Computer(this);
        }
    }
}

// Usage
Computer computer = new Computer.Builder()
    .cpu("Intel i7")
    .ram("16GB")
    .storage("512GB SSD")
    .build();
```

**Pros**: Fine control over construction process, immutable objects
**Cons**: Requires creating a separate Builder class

---

### Prototype

**Intent**: Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype.

**When to Use**:
- Classes to instantiate are specified at run-time
- Avoiding a proliferation of factory classes
- Instances of a class have few combinations of state

**Implementation**:
```java
public class Prototype implements Cloneable {
    private String name;
    private List<String> items;
    
    public Prototype clone() {
        try {
            Prototype cloned = (Prototype) super.clone();
            cloned.items = new ArrayList<>(this.items); // Deep copy
            return cloned;
        } catch (CloneNotSupportedException e) {
            throw new RuntimeException(e);
        }
    }
}
```

**Pros**: Reduces subclassing, dynamic addition/removal of products
**Cons**: Implementing Clone can be difficult for complex objects

---

## 2. Structural Patterns

### Adapter

**Intent**: Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces.

**When to Use**:
- You want to use an existing class, and its interface does not match
- You want to create a reusable class that cooperates with unrelated classes

**Structure**:
```
Target ← Adapter → Adaptee
```

**Implementation**:
```java
// Target interface
public interface Target {
    void request();
}

// Adaptee
public class Adaptee {
    public void specificRequest() { }
}

// Object Adapter
public class Adapter implements Target {
    private Adaptee adaptee;
    
    public Adapter(Adaptee adaptee) {
        this.adaptee = adaptee;
    }
    
    public void request() {
        adaptee.specificRequest();
    }
}
```

**Pros**: Single responsibility principle, Open/Closed Principle
**Cons**: Complexity increases

---

### Decorator

**Intent**: Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.

**When to Use**:
- To add responsibilities to individual objects dynamically
- When extension by subclassing is impractical

**Structure**:
```
Component ← Decorator
    ↑           ↑
ConcreteComponent  ConcreteDecorator
```

**Implementation**:
```java
public interface Component {
    void operation();
}

public class ConcreteComponent implements Component {
    public void operation() {
        System.out.println("Base operation");
    }
}

public abstract class Decorator implements Component {
    protected Component component;
    
    public Decorator(Component component) {
        this.component = component;
    }
    
    public void operation() {
        component.operation();
    }
}

public class ConcreteDecorator extends Decorator {
    public ConcreteDecorator(Component component) {
        super(component);
    }
    
    public void operation() {
        super.operation();
        addedBehavior();
    }
    
    private void addedBehavior() { }
}
```

**Pros**: More flexibility than static inheritance, avoids feature-laden classes
**Cons**: Many small objects, decorator can complicate code

---

### Proxy

**Intent**: Provide a surrogate or placeholder for another object to control access to it.

**When to Use**:
- Remote proxy: local representative for an object in a different address space
- Virtual proxy: creates expensive objects on demand
- Protection proxy: controls access to the original object

**Structure**:
```
Subject ← Proxy → RealSubject
```

**Implementation**:
```java
public interface Subject {
    void request();
}

public class RealSubject implements Subject {
    public void request() {
        System.out.println("Real request");
    }
}

public class Proxy implements Subject {
    private RealSubject realSubject;
    
    public void request() {
        if (realSubject == null) {
            realSubject = new RealSubject();
        }
        preRequest();
        realSubject.request();
        postRequest();
    }
    
    private void preRequest() { }
    private void postRequest() { }
}
```

**Pros**: Controls access, adds functionality transparently
**Cons**: May add overhead

---

### Facade

**Intent**: Provide a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use.

**When to Use**:
- You want to provide a simple interface to a complex subsystem
- There are many dependencies between clients and implementation classes

**Structure**:
```
Client → Facade → Subsystem classes
```

**Implementation**:
```java
public class ComputerFacade {
    private CPU cpu;
    private Memory memory;
    private HardDrive hardDrive;
    
    public ComputerFacade() {
        cpu = new CPU();
        memory = new Memory();
        hardDrive = new HardDrive();
    }
    
    public void start() {
        cpu.start();
        memory.start();
        hardDrive.start();
    }
    
    public void shutdown() {
        hardDrive.shutdown();
        memory.shutdown();
        cpu.shutdown();
    }
}
```

**Pros**: Shields clients from subsystem components, promotes weak coupling
**Cons**: Can become a "god object"

---

### Composite

**Intent**: Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions of objects uniformly.

**When to Use**:
- You want to represent part-whole hierarchies of objects
- You want clients to be able to ignore the difference between compositions and individual objects

**Structure**:
```
Component
    ↑
┌───┴───┐
Leaf   Composite → Component
```

**Implementation**:
```java
public interface Component {
    void operation();
}

public class Leaf implements Component {
    public void operation() { }
}

public class Composite implements Component {
    private List<Component> children = new ArrayList<>();
    
    public void add(Component component) { children.add(component); }
    public void remove(Component component) { children.remove(component); }
    
    public void operation() {
        for (Component child : children) {
            child.operation();
        }
    }
}
```

**Pros**: Defines class hierarchies consisting of primitive and complex objects, makes client simpler
**Cons**: Can make design overly general

---

### Flyweight

**Intent**: Use sharing to support large numbers of fine-grained objects efficiently.

**When to Use**:
- An application uses a large number of objects
- Storage costs are high because of the sheer quantity of objects

**Structure**:
```
FlyweightFactory → Flyweight
                        ↑
                ConcreteFlyweight
```

**Implementation**:
```java
public interface Flyweight {
    void operation(String extrinsicState);
}

public class ConcreteFlyweight implements Flyweight {
    private String intrinsicState;
    
    public ConcreteFlyweight(String intrinsicState) {
        this.intrinsicState = intrinsicState;
    }
    
    public void operation(String extrinsicState) { }
}

public class FlyweightFactory {
    private Map<String, Flyweight> flyweights = new HashMap<>();
    
    public Flyweight getFlyweight(String key) {
        if (!flyweights.containsKey(key)) {
            flyweights.put(key, new ConcreteFlyweight(key));
        }
        return flyweights.get(key);
    }
}
```

**Pros**: Reduces storage, reduces search time
**Cons**: Increases complexity, may add runtime cost

---

### Bridge

**Intent**: Decouple an abstraction from its implementation so that the two can vary independently.

**When to Use**:
- You want to avoid a permanent binding between an abstraction and its implementation
- Both the abstractions and their implementations should be extensible by subclassing

**Structure**:
```
Abstraction → Implementor
    ↑              ↑
RefinedAbstraction  ConcreteImplementor
```

**Implementation**:
```java
public interface DrawAPI {
    void drawCircle(int radius, int x, int y);
}

public class RedCircle implements DrawAPI {
    public void drawCircle(int radius, int x, int y) { }
}

public abstract class Shape {
    protected DrawAPI drawAPI;
    
    protected Shape(DrawAPI drawAPI) {
        this.drawAPI = drawAPI;
    }
    
    public abstract void draw();
}

public class Circle extends Shape {
    public Circle(DrawAPI drawAPI) {
        super(drawAPI);
    }
    
    public void draw() {
        drawAPI.drawCircle(radius, x, y);
    }
}
```

**Pros**: Separates interface and implementation, improves extensibility
**Cons**: Increases complexity

---

## 3. Behavioral Patterns

### Strategy

**Intent**: Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it.

**When to Use**:
- Many related classes differ only in their behavior
- You need different variants of an algorithm
- An algorithm uses data that clients shouldn't know about

**Structure**:
```
Context → Strategy
              ↑
        ConcreteStrategy
```

**Implementation**:
```java
public interface Strategy {
    int doOperation(int num1, int num2);
}

public class OperationAdd implements Strategy {
    public int doOperation(int num1, int num2) {
        return num1 + num2;
    }
}

public class Context {
    private Strategy strategy;
    
    public Context(Strategy strategy) {
        this.strategy = strategy;
    }
    
    public int executeStrategy(int num1, int num2) {
        return strategy.doOperation(num1, num2);
    }
}
```

**Pros**: Eliminates conditional statements, provides different implementations
**Cons**: Clients must know about strategies

---

### Observer

**Intent**: Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

**When to Use**:
- An abstraction has two aspects, one dependent on the other
- A change to one object requires changing others
- An object should be able to notify other objects without knowing who they are

**Structure**:
```
Subject → Observer
    ↑         ↑
ConcreteSubject  ConcreteObserver
```

**Implementation**:
```java
public interface Observer {
    void update(String state);
}

public interface Subject {
    void attach(Observer observer);
    void detach(Observer observer);
    void notifyObservers();
}

public class ConcreteSubject implements Subject {
    private List<Observer> observers = new ArrayList<>();
    private String state;
    
    public void attach(Observer observer) { observers.add(observer); }
    public void detach(Observer observer) { observers.remove(observer); }
    
    public void setState(String state) {
        this.state = state;
        notifyObservers();
    }
    
    public void notifyObservers() {
        for (Observer observer : observers) {
            observer.update(state);
        }
    }
}
```

**Pros**: Abstract coupling between Subject and Observer, support for broadcast communication
**Cons**: Unexpected updates, debugging difficulty

---

### Command

**Intent**: Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations.

**When to Use**:
- Parameterize objects by an action to perform
- Specify, queue, and execute requests at different times
- Support undo
- Support logging changes

**Structure**:
```
Invoker → Command ← Receiver
              ↑
        ConcreteCommand
```

**Implementation**:
```java
public interface Command {
    void execute();
    void undo();
}

public class Light {
    public void on() { }
    public void off() { }
}

public class LightOnCommand implements Command {
    private Light light;
    
    public LightOnCommand(Light light) {
        this.light = light;
    }
    
    public void execute() { light.on(); }
    public void undo() { light.off(); }
}

public class RemoteControl {
    private Command command;
    
    public void setCommand(Command command) {
        this.command = command;
    }
    
    public void pressButton() {
        command.execute();
    }
}
```

**Pros**: Decouples requester from performer, supports undo/redo
**Cons**: Many command classes

---

### State

**Intent**: Allow an object to alter its behavior when its internal state changes. The object will appear to change its class.

**When to Use**:
- An object's behavior depends on its state
- Operations have large, multipart conditional statements that depend on the object's state

**Structure**:
```
Context → State
              ↑
        ConcreteState
```

**Implementation**:
```java
public interface State {
    void handle(Context context);
}

public class StartState implements State {
    public void handle(Context context) {
        System.out.println("In start state");
        context.setState(new PlayingState());
    }
}

public class Context {
    private State state;
    
    public Context() {
        state = new StartState();
    }
    
    public void setState(State state) {
        this.state = state;
    }
    
    public void request() {
        state.handle(this);
    }
}
```

**Pros**: Localizes state-specific behavior, makes state transitions explicit
**Cons**: Can result in many state classes

---

### Template Method

**Intent**: Define the skeleton of an algorithm in an operation, deferring some steps to subclasses. Template Method lets subclasses redefine certain steps of an algorithm without changing the algorithm's structure.

**When to Use**:
- To implement the invariant parts of an algorithm once
- When common behavior among subclasses should be factored and localized

**Structure**:
```
AbstractClass ← ConcreteClass
```

**Implementation**:
```java
public abstract class Game {
    // Template method
    public final void play() {
        initialize();
        startPlay();
        endPlay();
    }
    
    protected abstract void initialize();
    protected abstract void startPlay();
    protected abstract void endPlay();
}

public class Cricket extends Game {
    protected void initialize() { System.out.println("Cricket initialized"); }
    protected void startPlay() { System.out.println("Cricket started"); }
    protected void endPlay() { System.out.println("Cricket finished"); }
}
```

**Pros**: Code reuse, common behavior in one place
**Cons**: Can be restrictive

---

### Chain of Responsibility

**Intent**: Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along the chain until an object handles it.

**When to Use**:
- More than one object may handle a request
- You want to issue a request to one of several objects without specifying the receiver explicitly

**Structure**:
```
Handler → Handler
    ↑
ConcreteHandler
```

**Implementation**:
```java
public abstract class Handler {
    protected Handler next;
    
    public Handler setNext(Handler next) {
        this.next = next;
        return next;
    }
    
    public abstract void handleRequest(int level);
}

public class LowHandler extends Handler {
    public void handleRequest(int level) {
        if (level <= 1) {
            System.out.println("Low handler handles request");
        } else if (next != null) {
            next.handleRequest(level);
        }
    }
}
```

**Pros**: Reduces coupling, adds flexibility
**Cons**: No guarantee of handling

---

### Mediator

**Intent**: Define an object that encapsulates how a set of objects interact. Mediator promotes loose coupling by keeping objects from referring to each other explicitly.

**When to Use**:
- A set of objects communicate in well-defined but complex ways
- You want to customize a behavior that's distributed between several objects

**Structure**:
```
Mediator
    ↑
ConcreteMediator ← Colleague
```

**Implementation**:
```java
public interface Mediator {
    void notify(Component sender, String event);
}

public class ConcreteMediator implements Mediator {
    private ComponentA componentA;
    private ComponentB componentB;
    
    public void notify(Component sender, String event) {
        if (event.equals("A")) {
            componentB.reactOnA();
        }
    }
}
```

**Pros**: Limits subclassing, decouples colleagues
**Cons**: Mediator can become complex

---

### Iterator

**Intent**: Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation.

**When to Use**:
- To access an aggregate object's contents without exposing its internal representation
- To support multiple traversals of aggregate objects

**Structure**:
```
Aggregate → Iterator
    ↑           ↑
ConcreteAggregate  ConcreteIterator
```

**Implementation**:
```java
public interface Iterator<T> {
    boolean hasNext();
    T next();
}

public interface Aggregate<T> {
    Iterator<T> createIterator();
}
```

**Pros**: Supports variations in traversal, simplifies aggregate interface
**Cons**: Can be overkill for simple collections

---

### Memento

**Intent**: Without violating encapsulation, capture and externalize an object's internal state so that the object can be restored to this state later.

**When to Use**:
- A snapshot of an object's state must be saved so that it can be restored later
- A direct interface to obtaining the state would expose implementation details

**Structure**:
```
Originator ← Memento → Caretaker
```

**Implementation**:
```java
public class Memento {
    private String state;
    
    public Memento(String state) {
        this.state = state;
    }
    
    public String getState() { return state; }
}

public class Originator {
    private String state;
    
    public void setState(String state) { this.state = state; }
    
    public Memento saveStateToMemento() {
        return new Memento(state);
    }
    
    public void getStateFromMemento(Memento memento) {
        state = memento.getState();
    }
}
```

**Pros**: Preserves encapsulation boundaries, simplifies originator
**Cons**: Can be expensive

---

### Visitor

**Intent**: Represent an operation to be performed on the elements of an object structure. Visitor lets you define a new operation without changing the classes of the elements on which it operates.

**When to Use**:
- An object structure contains many classes with differing interfaces
- Many distinct and unrelated operations need to be performed on objects

**Structure**:
```
Visitor → Element
    ↑         ↑
ConcreteVisitor  ConcreteElement
```

**Implementation**:
```java
public interface Visitor {
    void visit(ConcreteElementA element);
    void visit(ConcreteElementB element);
}

public interface Element {
    void accept(Visitor visitor);
}

public class ConcreteElementA implements Element {
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}
```

**Pros**: Easy to add new operations, gathers related behavior
**Cons**: Hard to add new element classes

---

## 4. Pattern Selection Guide

### By Problem Type

| Problem | Pattern |
|---------|---------|
| Need single instance | Singleton |
| Create objects flexibly | Factory Method |
| Create object families | Abstract Factory |
| Build complex objects | Builder |
| Clone objects | Prototype |
| Incompatible interfaces | Adapter |
| Add responsibilities dynamically | Decorator |
| Control access | Proxy |
| Simplify complex interface | Facade |
| Tree structures | Composite |
| Share common state | Flyweight |
| Separate abstraction from implementation | Bridge |
| Switch algorithms | Strategy |
| Event notification | Observer |
| Encapsulate requests | Command |
| State-dependent behavior | State |
| Algorithm skeleton | Template Method |
| Multiple handlers | Chain of Responsibility |
| Complex interactions | Mediator |
| Traverse collections | Iterator |
| Save/restore state | Memento |
| Add operations to structure | Visitor |

### By Code Smell

| Code Smell | Pattern Solution |
|------------|------------------|
| Large switch statements | State, Strategy |
| Many conditionals | Strategy, State, Null Object |
| Tight coupling | Observer, Mediator, Facade |
| Hard to create objects | Factory, Builder |
| Can't extend classes | Decorator, Adapter |
| Complex subsystems | Facade |
| Need to vary algorithms | Strategy, Template Method |
| Many similar objects | Flyweight, Prototype |
| Need to notify objects | Observer |
| Need to encapsulate requests | Command |

### Pattern Relationships

```
Creational ← → Structural ← → Behavioral
     │              │              │
     ▼              ▼              ▼
 Factory         Adapter        Strategy
 Abstract        Decorator      Observer
 Singleton       Proxy          Command
 Builder         Facade         State
 Prototype       Composite      Template
                 Flyweight      Chain
                 Bridge         Mediator
                                Iterator
                                Memento
                                Visitor
```
