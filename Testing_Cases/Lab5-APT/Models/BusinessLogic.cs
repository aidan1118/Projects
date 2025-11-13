using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Threading.Tasks;
using Lab3SuperSupperClub.Models;

namespace Lab3SuperSupperClub.Models;

public class BusinessLogic : IBusinessLogic
{
    private readonly IDatabase _database;
    public ObservableCollection<SupperClub> SupperClubs { get; set; }


    public BusinessLogic()
    {
        _database = new Database();
        SupperClubs = new ObservableCollection<SupperClub>();
        _ = LoadSupperClubsAsync(); // Fire and forget for constructor
    }


    private async Task LoadSupperClubsAsync()
    {
        await _database.SelectAllSupperClubs();
        SupperClubs.Clear();
        foreach (var supperClub in _database.SupperClubs)
        {
            SupperClubs.Add(supperClub);
        }
    }

    public async Task<ObservableCollection<SupperClub>> GetSupperClubs()
    {
        return await _database.SelectAllSupperClubs();
    }


    public async Task<SupperClubError> AddSupperClub(int clubId, string name, string city, int[] ratings)
    {
        // Validate inputs
        var validationError = ValidateSupperClubData(clubId, name, city, ratings);
        if (validationError != SupperClubError.None)
        {
            return validationError;
        }

        SupperClub? existingSupperClub = await _database.SelectSupperClub(clubId);
        if (existingSupperClub != null)
        {
            return SupperClubError.DuplicateSupperClubId;
        }

        var newSupperClub = new SupperClub
        {
            ClubId = clubId,
            Name = name,
            City = city,
            Ratings = ratings
        };
        var result = await _database.InsertSupperClub(newSupperClub);
        if (result == SupperClubError.None)
        {
            SupperClubs.Add(newSupperClub);
        }
        return result;

    }


    public async Task<SupperClubError> DeleteSupperClub(int clubId)
    {
        // Validate club ID
        if (clubId <= 0)
        {
            return SupperClubError.InvalidClubId;
        }

        var supperClub = SupperClubs.FirstOrDefault(sc => sc.ClubId == clubId);
        if (supperClub == null)
        {
            return SupperClubError.SupperClubIdNotFound;
        }

        var result = await _database.DeleteSupperClub(supperClub);
        if (result == SupperClubError.None)
        {
            SupperClubs.Remove(supperClub);
        }
        return result;
    }

    public async Task<SupperClubError> EditSupperClub(int clubId, string name, string city, int[] ratings)
    {
        // Validate inputs (but allow existing clubId)
        var validationError = ValidateSupperClubData(clubId, name, city, ratings, skipClubIdValidation: true);
        if (validationError != SupperClubError.None)
        {
            return validationError;
        }

        var supperClub = SupperClubs.FirstOrDefault(sc => sc.ClubId == clubId);
        if (supperClub == null)
        {
            return SupperClubError.SupperClubIdNotFound;
        }

        return await _database.UpdateSupperClub(supperClub, name, city, ratings);
    }


    public async Task<SupperClub?> FindSupperClub(int clubId)
    {
        SupperClub? sc = await _database.SelectSupperClub(clubId);

        return sc;
    }

    public Task<int[]> CalculateStatistics()
    {
        var ratingsCount = new int[5];
        foreach (var supperClub in SupperClubs)
        {
            var averageRating = supperClub.Ratings.Average();
            ratingsCount[(int)averageRating - 1]++;
        }

        return Task.FromResult(ratingsCount);
    }

    // Validation methods extracted from MainPage.xaml.cs
    private SupperClubError ValidateSupperClubData(int clubId, string name, string city, int[] ratings, bool skipClubIdValidation = false)
    {
        // Validate Club ID
        if (!skipClubIdValidation && clubId <= 0)
        {
            return SupperClubError.InvalidClubId;
        }

        // Validate Name
        if (string.IsNullOrWhiteSpace(name))
        {
            return SupperClubError.NameTooShort;
        }

        // Validate City
        if (string.IsNullOrWhiteSpace(city))
        {
            return SupperClubError.CityTooShort;
        }

        // Validate Ratings
        if (ratings == null || ratings.Length != 3)
        {
            return SupperClubError.InvalidRatings;
        }

        // Validate rating values are in range 1-5
        for (int i = 0; i < ratings.Length; i++)
        {
            if (ratings[i] < 1 || ratings[i] > 5)
            {
                return SupperClubError.InvalidRatings;
            }
        }

        return SupperClubError.None;
    }

    // Helper method for parsing ratings string (like in MainPage.xaml.cs)
    public static bool TryParseRatings(string str, out int[]? ratings)
    {
        ratings = null;
        if (str == null)
        {
            return false;
        }
        
        string[] pieces = str.Split(); // splitting string of the form (we hope) a s f
        if (pieces.Length < 3)
        { // should be 3 ratings
            return false;
        }
        
        try
        {
            ratings = new int[] { int.Parse(pieces[0]), int.Parse(pieces[1]), int.Parse(pieces[2]) };
        }
        catch
        {
            return false;
        }

        return true;
    }

}
