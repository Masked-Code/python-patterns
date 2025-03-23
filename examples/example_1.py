from abc import ABC, abstractmethod
import time
import weakref
from threading import Lock
from typing import List

# Creational Pattern: Singleton
# Ensures only one instance of OrderLogger exists
class OrderLogger:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(OrderLogger, cls).__new__(cls)
        return cls._instance

    def log(self, message):
        print(f"[LOG] {message}")

# Creational Pattern: Factory Method
# Defines an interface for creating payment processors
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float):
        pass

class PaymentFactory:
    @staticmethod
    def create_payment_processor(payment_type: str) -> PaymentProcessor:
        if payment_type == "credit":
            return CreditCardProcessor()
        elif payment_type == "paypal":
            return PayPalProcessor()
        else:
            raise ValueError("Unknown payment type")

class CreditCardProcessor(PaymentProcessor):
    def process(self, amount: float):
        print(f"Processing ${amount} via Credit Card")

class PayPalProcessor(PaymentProcessor):
    def process(self, amount: float):
        print(f"Processing ${amount} via PayPal")

# Structural Pattern: Adapter
# Adapts a legacy inventory system to a modern interface
class InventorySystem:
    def check_stock(self, item_id: int, quantity: int) -> bool:
        return True  # Simplified legacy system

class ModernInventory(ABC):
    @abstractmethod
    def is_available(self, product_id: int, qty: int) -> bool:
        pass

class InventoryAdapter(ModernInventory):
    def __init__(self, legacy_inventory: InventorySystem):
        self.legacy = legacy_inventory

    def is_available(self, product_id: int, qty: int) -> bool:
        return self.legacy.check_stock(product_id, qty)

# Structural Pattern: Decorator
# Adds logging functionality to payment processing dynamically
class LoggingPaymentDecorator(PaymentProcessor):
    def __init__(self, wrapped: PaymentProcessor, logger: OrderLogger):
        self.wrapped = wrapped
        self.logger = logger

    def process(self, amount: float):
        self.logger.log(f"Starting payment of ${amount}")
        self.wrapped.process(amount)
        self.logger.log(f"Completed payment of ${amount}")

# Behavioral Pattern: Observer
# Notifies subscribers (e.g., customer, warehouse) when an order status changes
class OrderSubject:
    def __init__(self):
        self._observers = []
        self._status = "Pending"

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self._status)

    def set_status(self, status: str):
        self._status = status
        self.notify()

class OrderObserver(ABC):
    @abstractmethod
    def update(self, status: str):
        pass

class Customer(OrderObserver):
    def __init__(self, name: str):
        self.name = name

    def update(self, status: str):
        print(f"Customer {self.name} notified: Order is now {status}")

class Warehouse(OrderObserver):
    def update(self, status: str):
        print(f"Warehouse notified: Order is now {status}")

# Behavioral Pattern: Strategy
# Allows different discount strategies to be applied dynamically
class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, amount: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply_discount(self, amount: float) -> float:
        return amount

class SeasonalDiscount(DiscountStrategy):
    def apply_discount(self, amount: float) -> float:
        return amount * 0.9  # 10% off

class Order:
    def __init__(self, discount_strategy: DiscountStrategy):
        self.items = []
        self.discount_strategy = discount_strategy
        self.subject = OrderSubject()

    def add_item(self, item_id: int, price: float):
        self.items.append((item_id, price))

    def calculate_total(self) -> float:
        total = sum(price for _, price in self.items)
        return self.discount_strategy.apply_discount(total)

# Modern Pattern: Circuit Breaker
# Prevents repeated calls to a failing service (simulated inventory check)
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3):
        self.state = "CLOSED"
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > 5:  # Reset after 5 seconds
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit is open, service unavailable")
        
        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                self.last_failure_time = time.time()
            raise e

# Main execution
if __name__ == "__main__":
    # Singleton logger
    logger = OrderLogger()

    # Factory Method for payment processor
    payment_processor = PaymentFactory.create_payment_processor("credit")

    # Decorator to add logging to payment
    decorated_payment = LoggingPaymentDecorator(payment_processor, logger)

    # Adapter for inventory
    legacy_inventory = InventorySystem()
    inventory = InventoryAdapter(legacy_inventory)

    # Strategy for discount
    order = Order(SeasonalDiscount())

    # Observer setup
    customer = Customer("Alice")
    warehouse = Warehouse()
    order.subject.attach(customer)
    order.subject.attach(warehouse)

    # Circuit Breaker for inventory check
    breaker = CircuitBreaker()
    order.add_item(1, 100.0)
    total = order.calculate_total()

    # Process order
    print(f"Total after discount: ${total}")
    if breaker.call(inventory.is_available, 1, 1):
        decorated_payment.process(total)
        order.subject.set_status("Processed")
    else:
        print("Inventory unavailable")