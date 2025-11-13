using System.Collections.ObjectModel;
using System.IO;
using System.Text.Json;

namespace Lab3SuperSupperClub.Models;

public interface IDatabase
{
    public ObservableCollection<SupperClub> SupperClubs { get; }
    public Task<SupperClub?> SelectSupperClub(int clubId);
    public Task<ObservableCollection<SupperClub>> SelectAllSupperClubs();

    public Task<SupperClubError> InsertSupperClub(SupperClub supperClub);
    public Task<SupperClubError> DeleteSupperClub(SupperClub supperClubToDelete);
    public Task<SupperClubError> UpdateSupperClub(SupperClub supperClubToUpdate, string name, string city, int[] ratings);
}