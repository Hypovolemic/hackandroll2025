import streamlit as st

# Class to manage daily calorie intake
class DailyCalorieTracker:
    def __init__(self, date):
        self.date = date
        self.calories = 0

    def add_calories(self, amount):
        self.calories += amount

    def get_calories(self):
        return self.calories

# Class to manage weekly calorie intake
class WeeklyCalorieTracker:
    def __init__(self):
        self.daily_trackers = {}  # Dictionary to store daily trackers by date

    def add_daily_calories(self, date, amount):
        if date not in self.daily_trackers:
            self.daily_trackers[date] = DailyCalorieTracker(date)
        self.daily_trackers[date].add_calories(amount)

    def get_weekly_calories(self):
        return sum(tracker.get_calories() for tracker in self.daily_trackers.values())

    def get_average_daily_calories(self):
        if not self.daily_trackers:
            return 0
        return self.get_weekly_calories() / len(self.daily_trackers)

# Streamlit application
def main():
    st.title("Calorie Tracker")
    st.subheader("Track your daily and weekly calorie intake")

    # Initialize weekly tracker
    if "weekly_tracker" not in st.session_state:
        st.session_state.weekly_tracker = WeeklyCalorieTracker()

    # Input for date and calories
    date = st.date_input("Select Date")
    calorie_input = st.number_input("Enter Calories Consumed", min_value=0, step=1)

    if st.button("Add Calories"):
        st.session_state.weekly_tracker.add_daily_calories(date, calorie_input)
        st.success(f"Added {calorie_input} calories for {date}!")

    # Display daily and weekly stats
    st.subheader("Weekly Statistics")
    total_weekly_calories = st.session_state.weekly_tracker.get_weekly_calories()
    avg_daily_calories = st.session_state.weekly_tracker.get_average_daily_calories()

    st.write(f"Total Calories Consumed This Week: {total_weekly_calories}")
    st.write(f"Average Daily Calorie Intake: {avg_daily_calories:.2f}")

    # Option to display daily breakdown
    if st.checkbox("Show Daily Breakdown"):
        for date, tracker in st.session_state.weekly_tracker.daily_trackers.items():
            st.write(f"{date}: {tracker.get_calories()} calories")

if __name__ == "__main__":
    main()
