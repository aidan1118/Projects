using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Supabase;
using Lab3SuperSupperClub.Models;
using Supabase.Postgrest.Models;
using Supabase.Postgrest.Attributes;
using Supabase.Gotrue;
using System.Collections.ObjectModel;
using System.ComponentModel.DataAnnotations;

namespace Lab3SuperSupperClub.Models;

public class Database : IDatabase
{
    private static string url = "https://joubdumfrcsyymzvnldd.supabase.co";
    private static string key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpvdWJkdW1mcmNzeXltenZubGRkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI5ODkzMDUsImV4cCI6MjA3ODU2NTMwNX0.gdJf2EzsmMRwLqL_7F0KrdEKYaYTNAyniR4JHiKpg8c";
    private Supabase.Client client;
    public ObservableCollection<SupperClub> SupperClubs { get; private set; } = new();

    public Database()
    {
        client = new Supabase.Client(url, key);
    }

    public async Task<ObservableCollection<SupperClub>> SelectAllSupperClubs()
    {
        try
        {
            var response = await client.From<SupperClub>().Get();
            SupperClubs.Clear();

            foreach (var supperClub in response.Models)
            {
                SupperClubs.Add(supperClub);
            }
        }
        catch (Exception)
        {
            // Log error if needed in production
        }
        return SupperClubs;
    }

    public async Task<SupperClub?> SelectSupperClub(int clubId)
    {
        var response = await client.From<SupperClub>().Where(supperClub => supperClub.ClubId == clubId).Get();
        if (response != null)
        {
            return response!.Models.FirstOrDefault();
        }
        return null;
    }


    public async Task<SupperClubError> InsertSupperClub(SupperClub supperClub)
    {
        try
        {
            var response = await client.From<SupperClub>().Insert(supperClub);
            if (response.Models.Any())
            {
                SupperClubs.Add(response.Models.First());
            }
            else
            {
                return SupperClubError.DuplicateSupperClubId;
            }
        }
        catch (Exception ex)
        {
            return ex.Message.Contains("already exists") ? SupperClubError.DuplicateSupperClubId : SupperClubError.InsertionError;
        }
        return SupperClubError.None;
    }

    public async Task<SupperClubError> UpdateSupperClub(SupperClub supperClubToUpdate, string name, string city, int[] ratings)
    {
        try
        {
            supperClubToUpdate.Name = name;
            supperClubToUpdate.City = city;
            supperClubToUpdate.Ratings = ratings;
            var response = await client.From<SupperClub>().Update(supperClubToUpdate);
            if (response.Models.Any())
            {
                var updatedSupperClub = response.Models.First();
                var index = SupperClubs.IndexOf(supperClubToUpdate);
                if (index >= 0)
                {
                    SupperClubs[index] = updatedSupperClub;
                }
            }
            else
            {
                return SupperClubError.SupperClubIdNotFound;
            }
        }
        catch (Exception)
        {
            return SupperClubError.UpdateError;
        }
        return SupperClubError.None;
    }

    public async Task<SupperClubError> DeleteSupperClub(SupperClub supperClubToDelete)
    {
        try
        {
            var response = await client.From<SupperClub>().Delete(supperClubToDelete);
            if (response.Models.Any())
            {
                SupperClubs.Remove(supperClubToDelete);
            }
            else
            {
                return SupperClubError.SupperClubIdNotFound;
            }
        }
        catch (Exception)
        {
            return SupperClubError.DeleteError;
        }
        return SupperClubError.None;
    }

}


