from fastapi import FastAPI
from app.routes import auth, expense, income, budget, report


app = FastAPI(title="Expense Tracker",debug=True)



# Included routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(expense.router, prefix="/expenses", tags=["Expenses"])
app.include_router(income.router, prefix="/income", tags=["Income"])
app.include_router(budget.router, prefix="/budgets", tags=["Budgets"])
app.include_router(report.router, prefix="/reports", tags=["Reports"])


@app.get("/")
def root():
    return "Expense Tracking and Budget Management System"

