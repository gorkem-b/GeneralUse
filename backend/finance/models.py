# Import the base Model class from Django, which all our database tables will inherit from
from django.db import models

# Import the built-in User model provided by Django. 
# We use this so we don't have to build our own authentication system from scratch!
from django.contrib.auth.models import User

# Import MinValueValidator, which helps us ensure users don't enter negative numbers
from django.core.validators import MinValueValidator

# Import Decimal for accurate money calculations (floats can have rounding errors!)
from decimal import Decimal

# =====================================================================
# ACTIVE MANAGER FOR SOFT DELETION
# =====================================================================
class ActiveManager(models.Manager):
    """
    Custom manager that automatically filters out soft-deleted records from queries.
    This prevents deleted data from showing up in the UI, while still keeping it
    in the database for data integrity or recovery.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


# =====================================================================
# CATEGORY MODEL
# Think of a model like a blueprint for a database table.
# Every instance of this class will be one row in the 'finance_category' table.
# =====================================================================
class Category(models.Model):
    """
    Represents a financial category for classifying transactions.
    Categories are scoped per user to support a multi-tenant architecture.
    """
    
    # Define the choices for the 'type' field.
    # The first value ('INCOME') is what gets saved to the database.
    # The second value ('Income') is what gets shown to the user in forms.
    TYPE_CHOICES = (
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    )
    
    # Foreign key linking the category to a specific user.
    # 'on_delete=models.CASCADE' means if the User is deleted, all their Categories get deleted too!
    # 'related_name' lets us do `user.categories.all()` to get all categories for a user.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    
    # Name of the category (e.g., "Groceries", "Salary"). max_length ensures it doesn't get too long.
    name = models.CharField(max_length=100)
    
    # Type dictates whether this category is for money coming in or going out.
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    # Soft deletion flag
    is_deleted = models.BooleanField(default=False)

    # Managers
    objects = ActiveManager() # Default manager filters out deleted items
    all_objects = models.Manager() # Backup manager to access everything including deleted

    # The Meta class holds extra configuration for the model.
    class Meta:
        # We explicitly name the table in the database so it's easy to find.
        db_table = 'finance_category'
        # unique_together ensures that one specific user cannot have two categories with the exact same name.
        unique_together = ('user', 'name')

    # The __str__ method defines what this object looks like when printed (e.g., in the admin panel).
    def __str__(self):
        return f"{self.name} ({self.type})"


# =====================================================================
# TRANSACTION MODEL
# This table holds the actual records of money being spent or earned.
# =====================================================================
class Transaction(models.Model):
    """
    Represents a single financial transaction (income or expense) made by a user.
    Transactions are securely isolated per user.
    """
    # Links the transaction to the user who created it.
    # Again, if the user is deleted, their transactions are deleted too.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    
    # The monetary amount. We use DecimalField instead of FloatField because money needs exact precision.
    amount = models.DecimalField(
        max_digits=10, # Maximum 10 digits total (e.g., 99,999,999.99)
        decimal_places=2, # Exactly 2 digits after the decimal point (cents)
        # We use a validator to ensure the amount is at least 0.01 (no zero or negative transactions allowed!)
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # The exact date the transaction occurred.
    date = models.DateField()
    
    # Optional description or note for the transaction.
    # blank=True means forms can leave it empty. null=True means the database can store it as NULL.
    description = models.CharField(max_length=255, blank=True, null=True)
    
    # Links the transaction to its categorization type (e.g., linking a $50 transaction to "Groceries").
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions')

    # Soft deletion flag
    is_deleted = models.BooleanField(default=False)

    # Managers
    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        # Explicit table name for the database.
        db_table = 'finance_transaction'

    # How this transaction appears when printed out as a string.
    def __str__(self):
        return f"{self.amount} on {self.date}"
