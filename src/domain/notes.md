The term "Entity" 
An entity has a unique identity that doesn't change, even when its properties change.

tells us:

✅ It has business identity
✅ It can change over time
✅ It represents a real business concept
✅ It has behavior (methods)

Compare to:

"Model" - could be database model (technical)
"Class" - just programming concept
"Object" - too generic



Domain Layer says: "I need to save users"
Infrastructure Layer says: "I know how to save to PostgreSQL"



Domain Layer says:

"I need to:
- Create and manage Todos and Users
- Save them somewhere
- Retrieve them by various criteria
- But I don't care HOW or WHERE they're stored!"