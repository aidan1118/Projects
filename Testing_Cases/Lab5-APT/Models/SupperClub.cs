using System;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;
using Newtonsoft.Json;

namespace Lab3SuperSupperClub.Models
{
    [Table("supper_clubs")]
    public class SupperClub : ObservableBaseModel, IEquatable<SupperClub>
    {
        // Backing fields
        int _clubId = -1;
        string _name = "";
        string _city = "";
        int[] _ratings = new int[] { 0, 0, 0 };

        [PrimaryKey("club_id", shouldInsert: true)]
        public int ClubId
        {
            get => _clubId;
            set => SetProperty(ref _clubId, value);
        }

        [Column("name")]
        public string Name
        {
            get => _name;
            set => SetProperty(ref _name, value ?? "");
        }

        [Column("city")]
        public string City
        {
            get => _city;
            set => SetProperty(ref _city, value ?? "");
        }

        [Column("ratings")]
        public int[] Ratings
        {
            get => _ratings;
            set
            {
                // Normalize null or wrong length to three slots
                var normalized = (value is { Length: 3 }) ? value : new int[] { 0, 0, 0 };
                if (SetProperty(ref _ratings, normalized))
                {
                    // Also notify computed properties that depend on Ratings
                    OnPropertyChanged(nameof(RatingsString));
                    OnPropertyChanged(nameof(AverageRating));
                }
            }
        }

        public SupperClub() { }

        public SupperClub(int clubId, string name, string city, int[] ratings)
        {
            ClubId = clubId;
            Name = name;
            City = city;
            Ratings = ratings;
        //   UserId = userId;
        }

        // Computed properties
        [Column("ratings_string")]
        public string RatingsString
        {
            get
            {
                // Safe indexing in case something external mutates array length
                var a = (Ratings.Length > 0) ? Ratings[0] : 0;
                var b = (Ratings.Length > 1) ? Ratings[1] : 0;
                var c = (Ratings.Length > 2) ? Ratings[2] : 0;
                return $"{a}/{b}/{c}";
            }
        }

        [Column("average_rating")]
        public double AverageRating
        {
            get
            {
                if (Ratings.Length == 0) return 0.0;
                double total = 0.0;
                foreach (var r in Ratings) total += r;
                return total / Ratings.Length;
            }
        }

        public override string ToString()
            => $"ID: {ClubId}, Name: {Name}, City: {City}, Ratings: {RatingsString}";

        // Equality aligned with Movie: identity by primary key
        public override bool Equals(object? obj)
            => obj is SupperClub other && ClubId == other.ClubId;

        public bool Equals(SupperClub? other)
            => other is not null && ClubId == other.ClubId;

        public override int GetHashCode()
            => ClubId.GetHashCode();
    }
}