using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Threading.Tasks;

namespace Lab3SuperSupperClub.Models;

public interface IBusinessLogic
{
    Task<SupperClubError> AddSupperClub(int clubId, string name, string city, int[] ratings);
    Task<SupperClubError> DeleteSupperClub(int clubId);
    Task<SupperClubError> EditSupperClub(int clubId, string name, string city, int[] ratings);
    Task<SupperClub?> FindSupperClub(int clubId);
    Task<int[]> CalculateStatistics();
    Task<ObservableCollection<SupperClub>> GetSupperClubs();
}
