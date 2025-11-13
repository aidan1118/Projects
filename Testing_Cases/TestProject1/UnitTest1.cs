using Lab3SuperSupperClub.Models;

namespace TestProject1;

public class UnitTest1
{
    // Helper method to create a clean BusinessLogic instance for each test
    private IBusinessLogic CreateBusinessLogic()
    {
        return new BusinessLogic();
    }

    // Helper method to clear all supper clubs for clean test state
    private async Task ClearAllSupperClubs(IBusinessLogic businessLogic)
    {
        var clubs = await businessLogic.GetSupperClubs();
        foreach (var club in clubs.ToList())
        {
            await businessLogic.DeleteSupperClub(club.ClubId);
        }
    }

    #region AddSupperClub Tests

    [Fact]
    public async Task TestSuccessfulSCAddition()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        int clubId = 1001;
        string name = "Test Club";
        string city = "Test City";
        int[] ratings = [4, 5, 3];

        // Act
        var result = await businessLogic.AddSupperClub(clubId, name, city, ratings);

        // Assert
        Assert.Equal(SupperClubError.None, result);
        var addedClub = await businessLogic.FindSupperClub(clubId);
        Assert.NotNull(addedClub);
        Assert.Equal(clubId, addedClub.ClubId);
        Assert.Equal(name, addedClub.Name);
        Assert.Equal(city, addedClub.City);
        Assert.Equal(ratings, addedClub.Ratings);
    }

    [Fact]
    public async Task TestAdditionDuplicateSCId()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        int clubId = 1002;
        string name1 = "First Club";
        string name2 = "Second Club";
        string city = "Test City";
        int[] ratings = [4, 5, 3];

        // Act
        var firstResult = await businessLogic.AddSupperClub(clubId, name1, city, ratings);
        var secondResult = await businessLogic.AddSupperClub(clubId, name2, city, ratings);

        // Assert
        Assert.Equal(SupperClubError.None, firstResult);
        Assert.Equal(SupperClubError.DuplicateSupperClubId, secondResult);
        
        // Verify only the first club exists
        var club = await businessLogic.FindSupperClub(clubId);
        Assert.NotNull(club);
        Assert.Equal(name1, club.Name); // Should be the first club's name
    }

    [Theory]
    [InlineData(0, 5, 3)]
    [InlineData(-1, 4, 5)]
    [InlineData(6, 3, 2)]
    [InlineData(3, 0, 4)]
    [InlineData(4, -2, 5)]
    [InlineData(2, 3, 6)]
    public async Task TestAdditionInvalidRatings(int rating1, int rating2, int rating3)
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        int clubId = 1003;
        string name = "Test Club";
        string city = "Test City";
        int[] invalidRatings = [rating1, rating2, rating3];

        // Act
        var result = await businessLogic.AddSupperClub(clubId, name, city, invalidRatings);
        
        // Assert - Now validation is in BusinessLogic, so it should fail
        Assert.Equal(SupperClubError.InvalidRatings, result);
        
        // Verify club was not added
        var club = await businessLogic.FindSupperClub(clubId);
        Assert.Null(club);
    }

    [Fact]
    public async Task TestAdditionEmptyName()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        int clubId = 1004;
        string emptyName = "";
        string city = "Test City";
        int[] ratings = [4, 5, 3];

        // Act
        var result = await businessLogic.AddSupperClub(clubId, emptyName, city, ratings);

        // Assert - Business logic now validates names
        Assert.Equal(SupperClubError.NameTooShort, result);
        
        // Verify club was not added
        var club = await businessLogic.FindSupperClub(clubId);
        Assert.Null(club);
    }

    [Fact]
    public async Task TestAdditionEmptyCity()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        int clubId = 1005;
        string name = "Test Club";
        string emptyCity = "";
        int[] ratings = [4, 5, 3];

        // Act
        var result = await businessLogic.AddSupperClub(clubId, name, emptyCity, ratings);

        // Assert - Business logic now validates cities
        Assert.Equal(SupperClubError.CityTooShort, result);
        
        // Verify club was not added
        var club = await businessLogic.FindSupperClub(clubId);
        Assert.Null(club);
    }

    [Fact]
    public async Task TestAdditionInvalidClubId()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        int invalidClubId = -5;
        string name = "Test Club";
        string city = "Test City";
        int[] ratings = [4, 5, 3];

        // Act
        var result = await businessLogic.AddSupperClub(invalidClubId, name, city, ratings);

        // Assert - Business logic now validates club IDs
        Assert.Equal(SupperClubError.InvalidClubId, result);
        
        // Verify club was not added
        var club = await businessLogic.FindSupperClub(invalidClubId);
        Assert.Null(club);
    }

    [Fact]
    public async Task TestAdditionNullRatings()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        int clubId = 1006;
        string name = "Test Club";
        string city = "Test City";
        int[]? nullRatings = null;

        // Act
        var result = await businessLogic.AddSupperClub(clubId, name, city, nullRatings!);

        // Assert - Business logic validates null ratings
        Assert.Equal(SupperClubError.InvalidRatings, result);
        
        // Verify club was not added
        var club = await businessLogic.FindSupperClub(clubId);
        Assert.Null(club);
    }

    [Fact]
    public async Task TestAdditionWrongRatingsLength()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        int clubId = 1007;
        string name = "Test Club";
        string city = "Test City";
        int[] wrongLengthRatings = [4, 5]; // Only 2 ratings instead of 3

        // Act
        var result = await businessLogic.AddSupperClub(clubId, name, city, wrongLengthRatings);

        // Assert - Business logic validates ratings length
        Assert.Equal(SupperClubError.InvalidRatings, result);
        
        // Verify club was not added
        var club = await businessLogic.FindSupperClub(clubId);
        Assert.Null(club);
    }

    [Fact]
    public void TestTryParseRatingsHelper()
    {
        // Test the helper method that was extracted from MainPage.xaml.cs
        
        // Valid input
        bool result1 = BusinessLogic.TryParseRatings("4 5 3", out int[]? ratings1);
        Assert.True(result1);
        Assert.NotNull(ratings1);
        Assert.Equal([4, 5, 3], ratings1);

        // Invalid input - too few numbers
        bool result2 = BusinessLogic.TryParseRatings("4 5", out int[]? ratings2);
        Assert.False(result2);
        Assert.Null(ratings2);

        // Invalid input - non-numeric
        bool result3 = BusinessLogic.TryParseRatings("a b c", out int[]? ratings3);
        Assert.False(result3);
        Assert.Null(ratings3);

        // Invalid input - null
        bool result4 = BusinessLogic.TryParseRatings(null!, out int[]? ratings4);
        Assert.False(result4);
        Assert.Null(ratings4);
    }

    #endregion

    #region DeleteSupperClub Tests

    [Fact]
    public async Task TestSuccessfulSCDeletion()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        int clubId = 2001;
        string name = "Club to Delete";
        string city = "Delete City";
        int[] ratings = new int[] { 3, 4, 5 };

        // Add a club first
        await businessLogic.AddSupperClub(clubId, name, city, ratings);
        
        // Verify it exists
        var clubBeforeDelete = await businessLogic.FindSupperClub(clubId);
        Assert.NotNull(clubBeforeDelete);

        // Act
        var result = await businessLogic.DeleteSupperClub(clubId);

        // Assert
        Assert.Equal(SupperClubError.None, result);
        var deletedClub = await businessLogic.FindSupperClub(clubId);
        Assert.Null(deletedClub);
    }

    [Fact]
    public async Task TestDeletionNonexistentSCId()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        int nonexistentId = 9999;

        // Act
        var result = await businessLogic.DeleteSupperClub(nonexistentId);

        // Assert
        Assert.Equal(SupperClubError.SupperClubIdNotFound, result);
    }

    [Theory]
    [InlineData(-1)]
    [InlineData(0)]
    [InlineData(-100)]
    public async Task TestDeletionInvalidSCId(int invalidId)
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);

        // Act
        var result = await businessLogic.DeleteSupperClub(invalidId);

        // Assert - Now validates invalid club IDs
        Assert.Equal(SupperClubError.InvalidClubId, result);
    }

    #endregion

    #region EditSupperClub Tests

    [Fact]
    public async Task TestSuccessfulSCEdit()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        int clubId = 3001;
        string originalName = "Original Club";
        string originalCity = "Original City";
        int[] originalRatings = [3, 4, 2];
        
        string newName = "Updated Club";
        string newCity = "Updated City";
        int[] newRatings = [5, 4, 3];

        // Add original club
        await businessLogic.AddSupperClub(clubId, originalName, originalCity, originalRatings);

        // Act
        var result = await businessLogic.EditSupperClub(clubId, newName, newCity, newRatings);

        // Assert
        Assert.Equal(SupperClubError.None, result);
        
        // Verify the club was updated
        var updatedClub = await businessLogic.FindSupperClub(clubId);
        Assert.NotNull(updatedClub);
        Assert.Equal(clubId, updatedClub.ClubId);
        Assert.Equal(newName, updatedClub.Name);
        Assert.Equal(newCity, updatedClub.City);
        Assert.Equal(newRatings, updatedClub.Ratings);
    }

    [Fact]
    public async Task TestEditNonexistentSCId()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        int nonexistentId = 9998;
        string name = "Test Name";
        string city = "Test City";
        int[] ratings = [4, 5, 3];

        // Act
        var result = await businessLogic.EditSupperClub(nonexistentId, name, city, ratings);

        // Assert
        Assert.Equal(SupperClubError.SupperClubIdNotFound, result);
    }

    [Fact]
    public async Task TestEditWithEmptyName()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        int clubId = 3002;
        string originalName = "Original Club";
        string originalCity = "Original City";
        int[] originalRatings = [3, 4, 2];
        
        string emptyName = "";
        string newCity = "Updated City";
        int[] newRatings = [5, 4, 3];

        // Add original club
        await businessLogic.AddSupperClub(clubId, originalName, originalCity, originalRatings);

        // Act
        var result = await businessLogic.EditSupperClub(clubId, emptyName, newCity, newRatings);

        // Assert - Business logic now validates empty names
        Assert.Equal(SupperClubError.NameTooShort, result);
        
        // Verify club was not updated (still has original name)
        var club = await businessLogic.FindSupperClub(clubId);
        Assert.NotNull(club);
        Assert.Equal(originalName, club.Name);
        
        // Clean up
        await businessLogic.DeleteSupperClub(clubId);
    }

    #endregion

    #region DeleteAllSupperClubs Tests

    [Fact]
    public async Task TestDeleteAllSupperClubs()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        
        // Add multiple clubs
        await businessLogic.AddSupperClub(4001, "Club 1", "City 1", [4, 5, 3]);
        await businessLogic.AddSupperClub(4002, "Club 2", "City 2", [3, 4, 5]);
        await businessLogic.AddSupperClub(4003, "Club 3", "City 3", [5, 3, 4]);

        // Verify clubs exist
        var clubsBeforeDelete = await businessLogic.GetSupperClubs();
        Assert.True(clubsBeforeDelete.Count >= 3);

        // Act - Simulate the delete all functionality from MainPage.xaml.cs
        var allClubs = (await businessLogic.GetSupperClubs()).ToList();
        var deleteResults = new List<SupperClubError>();
        
        foreach (var club in allClubs)
        {
            var deleteResult = await businessLogic.DeleteSupperClub(club.ClubId);
            deleteResults.Add(deleteResult);
        }

        // Assert
        Assert.All(deleteResults, result => Assert.Equal(SupperClubError.None, result));
        
        // Verify all clubs are deleted
        var clubsAfterDelete = await businessLogic.GetSupperClubs();
        Assert.Empty(clubsAfterDelete);
    }

    [Fact]
    public async Task TestDeleteAllWhenEmpty()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);

        // Act - Try to delete all when there are no clubs
        var allClubs = (await businessLogic.GetSupperClubs()).ToList();
        var deleteResults = new List<SupperClubError>();
        
        foreach (var club in allClubs)
        {
            var deleteResult = await businessLogic.DeleteSupperClub(club.ClubId);
            deleteResults.Add(deleteResult);
        }

        // Assert - Should have no operations to perform
        Assert.Empty(deleteResults);
        Assert.Empty(allClubs);
    }

    #endregion

    #region Additional Edge Case Tests

    [Fact]
    public async Task TestFindSupperClubExists()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        int clubId = 5001;
        string name = "Find Me Club";
        string city = "Find City";
        int[] ratings = [4, 4, 4];

        await businessLogic.AddSupperClub(clubId, name, city, ratings);

        // Act
        var foundClub = await businessLogic.FindSupperClub(clubId);

        // Assert
        Assert.NotNull(foundClub);
        Assert.Equal(clubId, foundClub.ClubId);
        Assert.Equal(name, foundClub.Name);
        Assert.Equal(city, foundClub.City);
        Assert.Equal(ratings, foundClub.Ratings);
    }

    [Fact]
    public async Task TestFindSupperClubDoesNotExist()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        int nonexistentId = 9997;

        // Act
        var foundClub = await businessLogic.FindSupperClub(nonexistentId);

        // Assert
        Assert.Null(foundClub);
    }

    [Fact]
    public async Task TestCalculateStatistics()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        
        // Add clubs with known ratings for statistics calculation
        await businessLogic.AddSupperClub(6001, "Club 1", "City 1", [1, 1, 1]); // Average: 1
        await businessLogic.AddSupperClub(6002, "Club 2", "City 2", [2, 2, 2]); // Average: 2
        await businessLogic.AddSupperClub(6003, "Club 3", "City 3", [3, 3, 3]); // Average: 3
        await businessLogic.AddSupperClub(6004, "Club 4", "City 4", [4, 4, 4]); // Average: 4
        await businessLogic.AddSupperClub(6005, "Club 5", "City 5", [5, 5, 5]); // Average: 5

        // Act
        var statistics = await businessLogic.CalculateStatistics();

        // Assert
        Assert.NotNull(statistics);
        Assert.Equal(5, statistics.Length); // Should have 5 rating categories (1-5)
        Assert.Equal(1, statistics[0]); // 1 club with average rating 1
        Assert.Equal(1, statistics[1]); // 1 club with average rating 2
        Assert.Equal(1, statistics[2]); // 1 club with average rating 3
        Assert.Equal(1, statistics[3]); // 1 club with average rating 4
        Assert.Equal(1, statistics[4]); // 1 club with average rating 5
    }

    [Fact]
    public async Task TestGetSupperClubs()
    {
        // Arrange
        IBusinessLogic businessLogic = CreateBusinessLogic();
        await ClearAllSupperClubs(businessLogic);
        
        // Add some clubs with unique IDs
        await businessLogic.AddSupperClub(7001, "Get Club 1", "Get City 1", [4, 5, 3]);
        await businessLogic.AddSupperClub(7002, "Get Club 2", "Get City 2", [3, 4, 5]);

        // Act
        var clubs = await businessLogic.GetSupperClubs();

        // Assert
        Assert.NotNull(clubs);
        Assert.True(clubs.Count >= 2, $"Expected at least 2 clubs, but found {clubs.Count}");
        Assert.Contains(clubs, c => c.ClubId == 7001);
        Assert.Contains(clubs, c => c.ClubId == 7002);
        
        // Clean up - remove the test clubs
        await businessLogic.DeleteSupperClub(7001);
        await businessLogic.DeleteSupperClub(7002);
    }

    #endregion
}