import json
from fpdf import FPDF

# Load the JSON data from file
with open('matchup_trends.json', 'r') as f:
    data = json.load(f)

# Access basic matchup information
upcoming_game = data["UpcomingGame"]
home_team = upcoming_game["HomeTeam"]
away_team = upcoming_game["AwayTeam"]
point_spread = upcoming_game["PointSpread"]

# Determine favorite and underdog based on the point spread
if point_spread > 0:
    favorite_team = away_team
    underdog_team = home_team
else:
    favorite_team = home_team
    underdog_team = away_team

# Scopes to retain based on the team's status
favorite_scopes = {
    "Last 3 Games as Favorite",
    "Last 5 Games as Favorite",
    "Last 10 Games as Favorite",
}
underdog_scopes = {
    "Last 3 Games as Underdog",
    "Last 5 Games as Underdog",
    "Last 10 Games as Underdog",
}

# Filter the team trends to exclude incorrect data
filtered_data = {"UpcomingGame": upcoming_game, "TeamTrends": []}

for team in data["TeamTrends"]:
    filtered_team = {"Team": team["Team"], "TeamGameTrends": []}
    for trend in team["TeamGameTrends"]:
        scope = trend["Scope"]

        # Determine if the trend aligns with the home/away team designation
        if ("Home" in scope and team["Team"] != home_team) or \
           ("Away" in scope and team["Team"] != away_team):
            continue

        # Determine if the trend aligns with the favorite/underdog designation
        if team["Team"] == favorite_team:
            valid_scopes = favorite_scopes
        elif team["Team"] == underdog_team:
            valid_scopes = underdog_scopes
        else:
            # Skip trends for teams not in the current matchup
            continue

        # Include trends only if they match the valid scopes
        if scope in valid_scopes:
            filtered_team["TeamGameTrends"].append(trend)
    
    filtered_data["TeamTrends"].append(filtered_team)

# Function to save filtered data to a PDF
def save_to_pdf(data, filename="cleaned_data.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, txt="Cleaned Matchup Trends Report", ln=True, align='C')
    pdf.ln(10)

    # Matchup Information
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(0, 10, txt="Upcoming Game", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Home Team: {home_team}", ln=True)
    pdf.cell(0, 10, txt=f"Away Team: {away_team}", ln=True)
    pdf.cell(0, 10, txt=f"Point Spread: {point_spread}", ln=True)
    pdf.ln(10)

    # Team Trends
    for team in data["TeamTrends"]:
        pdf.set_font("Arial", style='B', size=14)
        pdf.cell(0, 10, txt=f"Team: {team['Team']}", ln=True)
        pdf.set_font("Arial", size=12)
        
        if not team["TeamGameTrends"]:
            pdf.cell(0, 10, txt="No valid trends available.", ln=True)
        else:
            for trend in team["TeamGameTrends"]:
                pdf.cell(0, 10, txt=f"Scope: {trend['Scope']}", ln=True)
                pdf.cell(0, 10, txt=f"  Average Score: {trend['AverageScore']}", ln=True)
                pdf.ln(5)

        pdf.ln(10)

    # Save PDF
    pdf.output(filename)
    print(f"PDF saved as {filename}")

# Save the cleaned data to a PDF
save_to_pdf(filtered_data, filename="cleaned_data.pdf")
