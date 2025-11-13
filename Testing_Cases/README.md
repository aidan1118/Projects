# Lab 5 - Oh, What Could Possibly Go Wrong? 🫣

## Objective
Learn how to construct and run unit tests in Visual Studio; encourage reading the documentation and independent learning. This lab focuses on implementing comprehensive unit testing to verify the application's basic functionality, emphasizing that unit tests should be at the heart of software development, not an afterthought.

## Project Overview
This project is a C# console application that manages a supper club database using Supabase as the backend. The application follows a layered architecture with business logic separation and includes comprehensive unit testing.

## Main Components

### 1. Core Application (`Lab5-APT`)
- **Models**: Contains the data models and database interaction classes
  - `SupperClub.cs` - Entity model representing a supper club with validation
  - `Database.cs` - Database access layer using Supabase client
  - `IDatabase.cs` - Interface defining database operations
  - `BusinessLogic.cs` - Business logic layer handling application rules
  - `IBusinessLogic.cs` - Interface defining business operations
  - `SupperClubError.cs` - Enumeration of possible error states

### 2. Test Project (`TestProject1`)
- Comprehensive xUnit test suite covering all public methods in the `IBusinessLogic` interface
- Tests structured with Arrange-Act-Assert pattern
- Coverage includes:
  - Adding new supper clubs to the database
  - Deleting supper clubs from the database  
  - Editing existing supper clubs
  - Deleting all supper clubs
  - Edge cases and error conditions

### 3. Database Schema
The application uses a Supabase PostgreSQL database with the following table structure:

```sql
CREATE TABLE supper_clubs (
    club_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    ratings INTEGER[], 
    ratings_string TEXT,
    average_rating NUMERIC
);
```

## Key Features
- **Data Validation**: Ensures supper club data meets business requirements
- **Error Handling**: Comprehensive error reporting for various failure scenarios
- **Separation of Concerns**: Clear separation between data access, business logic, and testing layers
- **Asynchronous Operations**: All database operations are async for better performance
- **Unit Testing**: Thorough test coverage with both positive and negative test cases

## Testing Approach
- All tests operate through the business logic layer (no direct database access in tests)
- Tests cover both successful operations and edge cases
- Includes validation of error conditions (negative ratings, duplicate IDs, nonexistent clubs)
- Uses both `[Fact]` and `[Theory]` attributes as appropriate
- Descriptive test names clearly indicate what functionality is being tested

## Technology Stack
- **.NET 9.0**: Core framework
- **Supabase**: Backend database and API
- **xUnit**: Unit testing framework
- **C#**: Primary programming language

## Architecture
The application follows a three-layer architecture:
1. **Data Layer**: Database operations and entity models
2. **Business Logic Layer**: Application rules and validation
3. **Testing Layer**: Comprehensive unit test coverage

This structure ensures proper separation of concerns and makes the application maintainable and testable.