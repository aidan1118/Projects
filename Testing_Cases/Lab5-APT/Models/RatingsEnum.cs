namespace Lab3SuperSupperClub.Models;
    public enum RatingsEnum
    {
        Ambiance = 0,
        Staff = 1,
        Food = 2,
    }

    public enum SupperClubError {
        None,
        InvalidClubId,
        DuplicateSupperClubId,
        SupperClubIdNotFound,
        NameTooShort,
        CityTooShort,
        InvalidRatings,
        InsertionError,
        UpdateError,
        DeleteError
    }

